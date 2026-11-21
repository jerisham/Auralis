import "reflect-metadata";
import { INestApplication } from "@nestjs/common";
import { Test } from "@nestjs/testing";
import request from "supertest";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { AppModule } from "../src/app.module";
import { signUser } from "../src/auth";
import { ProblemFilter } from "../src/problem";
import { WebhookService } from "../src/webhooks";

const secret = "test-secret";

async function boot(limit: number): Promise<INestApplication> {
  const moduleRef = await Test.createTestingModule({
    imports: [AppModule.register({ limit, windowMs: 60_000 })],
  }).compile();
  const app = moduleRef.createNestApplication({ rawBody: true });
  app.useGlobalFilters(new ProblemFilter());
  await app.init();
  return app;
}

describe("API foundation", () => {
  let app: INestApplication;

  beforeAll(async () => {
    app = await boot(30);
  });

  afterAll(async () => {
    await app?.close();
  });

  it("returns health without authentication", async () => {
    const response = await request(app.getHttpServer()).get("/health");
    expect(response.status).toBe(200);
    expect(response.body).toEqual({ status: "ok", service: "auralis-api" });
  });

  it("returns 401 problem+json when the token is missing", async () => {
    const response = await request(app.getHttpServer()).get("/v1/me");
    expect(response.status).toBe(401);
    expect(response.headers["content-type"]).toContain("application/problem+json");
    expect(response.body.code).toBe("UNAUTHENTICATED");
    expect(response.body.status).toBe(401);
  });

  it("returns 403 when the role is wrong", async () => {
    const token = signUser({ sub: "customer-1", roles: ["customer"] }, secret);
    const response = await request(app.getHttpServer()).get("/v1/admin/ping").set("Authorization", `Bearer ${token}`);
    expect(response.status).toBe(403);
    expect(response.body.code).toBe("FORBIDDEN");
  });

  it("replays the same body for a duplicate Idempotency-Key", async () => {
    const token = signUser({ sub: "customer-2", roles: ["customer"] }, secret);
    const first = await request(app.getHttpServer())
      .post("/v1/echo")
      .set("Authorization", `Bearer ${token}`)
      .set("Idempotency-Key", "key-1")
      .send({ note: "a" });
    const second = await request(app.getHttpServer())
      .post("/v1/echo")
      .set("Authorization", `Bearer ${token}`)
      .set("Idempotency-Key", "key-1")
      .send({ note: "a" });
    expect(first.status).toBe(201);
    expect(second.status).toBe(201);
    expect(second.body).toEqual(first.body);
    expect(first.body.nonce).toEqual(expect.any(String));
  });

  it("rejects a reused Idempotency-Key with a different body", async () => {
    const token = signUser({ sub: "customer-3", roles: ["customer"] }, secret);
    await request(app.getHttpServer())
      .post("/v1/echo")
      .set("Authorization", `Bearer ${token}`)
      .set("Idempotency-Key", "key-2")
      .send({ note: "a" });
    const response = await request(app.getHttpServer())
      .post("/v1/echo")
      .set("Authorization", `Bearer ${token}`)
      .set("Idempotency-Key", "key-2")
      .send({ note: "b" });
    expect(response.status).toBe(409);
    expect(response.body.code).toBe("IDEMPOTENCY_KEY_REUSED");
  });

  it("stores an invalid webhook signature as rejected", async () => {
    const response = await request(app.getHttpServer())
      .post("/webhooks/razorpay")
      .set("x-signature", "not-a-real-signature")
      .set("content-type", "application/json")
      .send({ event: "payment.captured" });
    expect(response.status).toBe(401);
    expect(response.body.code).toBe("INVALID_SIGNATURE");
    const id = (response.body.errors as Array<{ id: string }>)[0]?.id;
    const admin = signUser({ sub: "admin-1", roles: ["admin"] }, secret);
    const stored = await request(app.getHttpServer()).get(`/v1/admin/webhooks/${id}`).set("Authorization", `Bearer ${admin}`);
    expect(stored.body.status).toBe("rejected");
    expect(stored.body.signatureValid).toBe(false);
  });

  it("reprocesses a webhook that failed once", async () => {
    const webhooks = app.get(WebhookService);
    const raw = JSON.stringify({ failOnce: true });
    const response = await request(app.getHttpServer())
      .post("/webhooks/razorpay")
      .set("x-signature", webhooks.sign(raw))
      .set("content-type", "application/json")
      .send(raw);
    expect(response.status).toBe(202);
    expect(response.body.status).toBe("failed");
    const admin = signUser({ sub: "admin-1", roles: ["admin"] }, secret);
    const again = await request(app.getHttpServer())
      .post(`/v1/admin/webhooks/${response.body.id}/reprocess`)
      .set("Authorization", `Bearer ${admin}`);
    expect(again.status).toBe(201);
    expect(again.body.status).toBe("processed");
  });

  it("lets a super admin change runtime config", async () => {
    const token = signUser({ sub: "super-1", roles: ["super_admin"] }, secret);
    const response = await request(app.getHttpServer())
      .patch("/v1/admin/config/return_window_hours")
      .set("Authorization", `Bearer ${token}`)
      .send({ value: 48 });
    expect(response.status).toBe(200);
    expect(response.body.value).toBe(48);
  });
});

describe("rate limit", () => {
  let app: INestApplication;

  beforeAll(async () => {
    app = await boot(2);
  });

  afterAll(async () => {
    await app?.close();
  });

  it("returns 429 with Retry-After after the limit", async () => {
    const token = signUser({ sub: "customer-rate", roles: ["customer"] }, secret);
    const server = app.getHttpServer();
    const first = await request(server).get("/v1/me").set("Authorization", `Bearer ${token}`);
    const second = await request(server).get("/v1/me").set("Authorization", `Bearer ${token}`);
    const third = await request(server).get("/v1/me").set("Authorization", `Bearer ${token}`);
    expect(first.status).toBe(200);
    expect(second.status).toBe(200);
    expect(third.status).toBe(429);
    expect(third.headers["retry-after"]).toBeDefined();
    expect(third.body.code).toBe("RATE_LIMITED");
  });
});
