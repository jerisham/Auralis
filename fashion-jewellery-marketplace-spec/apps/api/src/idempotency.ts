import { CallHandler, ExecutionContext, Injectable, NestInterceptor } from "@nestjs/common";
import { createHash, randomUUID } from "node:crypto";
import type { Request, Response } from "express";
import { Observable, of } from "rxjs";
import { map } from "rxjs/operators";
import type { AuthUser } from "./auth";
import { ProblemError } from "./problem";

type Stored = { hash: string; status: number; body: unknown };

@Injectable()
export class IdempotencyStore {
  private readonly rows = new Map<string, Stored>();

  get(scope: string): Stored | undefined {
    return this.rows.get(scope);
  }

  set(scope: string, value: Stored): void {
    this.rows.set(scope, value);
  }
}

@Injectable()
export class IdempotencyInterceptor implements NestInterceptor {
  constructor(private readonly store: IdempotencyStore) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<unknown> {
    const http = context.switchToHttp();
    const request = http.getRequest<Request & { user?: AuthUser }>();
    const response = http.getResponse<Response>();
    if (request.method !== "POST") return next.handle();
    const key = request.header("idempotency-key");
    if (!key) {
      throw new ProblemError(400, "IDEMPOTENCY_KEY_REQUIRED", "Bad Request", "Idempotency-Key header is required");
    }
    const hash = createHash("sha256").update(JSON.stringify(request.body ?? {})).digest("hex");
    const scope = `${request.user?.sub ?? "anon"}:${request.method}:${request.path}:${key}`;
    const existing = this.store.get(scope);
    if (existing) {
      if (existing.hash !== hash) {
        throw new ProblemError(409, "IDEMPOTENCY_KEY_REUSED", "Conflict", "This Idempotency-Key was used with a different request");
      }
      response.status(existing.status);
      return of(existing.body);
    }
    return next.handle().pipe(
      map((body) => {
        const status = response.statusCode || 200;
        this.store.set(scope, { hash, status, body });
        return body;
      }),
    );
  }
}

export function newNonce(): string {
  return randomUUID();
}
