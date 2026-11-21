import { createHmac, timingSafeEqual } from "node:crypto";
import { Injectable } from "@nestjs/common";

export type WebhookRecord = {
  id: string;
  provider: string;
  signatureValid: boolean;
  payload: unknown;
  rawBody: string;
  status: "rejected" | "pending" | "processed" | "failed";
  error?: string;
  attempts: number;
};

@Injectable()
export class WebhookService {
  private seq = 0;
  private readonly rows = new Map<string, WebhookRecord>();
  private readonly secret = process.env.WEBHOOK_SECRET ?? "dev-webhook-secret";

  sign(raw: string): string {
    return createHmac("sha256", this.secret).update(raw).digest("hex");
  }

  verify(raw: string, signature: string): boolean {
    const expected = this.sign(raw);
    const left = Buffer.from(expected);
    const right = Buffer.from(signature);
    if (left.length !== right.length) return false;
    return timingSafeEqual(left, right);
  }

  accept(provider: string, rawBody: string, signature: string): WebhookRecord {
    this.seq += 1;
    let payload: unknown = {};
    try {
      payload = JSON.parse(rawBody) as unknown;
    } catch {
      payload = { raw: rawBody };
    }
    const signatureValid = this.verify(rawBody, signature);
    const record: WebhookRecord = {
      id: `wh_${this.seq}`,
      provider,
      signatureValid,
      payload,
      rawBody,
      status: signatureValid ? "pending" : "rejected",
      attempts: 0,
    };
    this.rows.set(record.id, record);
    return record;
  }

  get(id: string): WebhookRecord | undefined {
    return this.rows.get(id);
  }

  /** Re-runs processing. Invalid signatures stay rejected. */
  reprocess(id: string): WebhookRecord {
    const record = this.rows.get(id);
    if (!record) {
      throw new Error("Webhook not found");
    }
    return this.process(record);
  }

  process(record: WebhookRecord): WebhookRecord {
    if (!record.signatureValid) {
      record.status = "rejected";
      return record;
    }
    const failOnce =
      typeof record.payload === "object" &&
      record.payload !== null &&
      "failOnce" in record.payload &&
      (record.payload as { failOnce?: boolean }).failOnce === true;
    if (failOnce && record.attempts === 0) {
      record.attempts = 1;
      record.status = "failed";
      record.error = "downstream";
      return record;
    }
    record.status = "processed";
    record.attempts += 1;
    return record;
  }
}
