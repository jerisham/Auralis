import { CanActivate, ExecutionContext, Inject, Injectable } from "@nestjs/common";
import type { Request, Response } from "express";
import type { AuthUser } from "./auth";
import { ProblemError } from "./problem";

export const RATE_LIMIT_OPTIONS = "RATE_LIMIT_OPTIONS";

export type RateLimitOptions = { limit: number; windowMs: number };

export class RateLimiter {
  private readonly hits = new Map<string, { count: number; resetAt: number }>();

  constructor(private readonly options: RateLimitOptions) {}

  take(key: string, now = Date.now()): { ok: true } | { ok: false; retryAfterSeconds: number } {
    const current = this.hits.get(key);
    if (!current || now >= current.resetAt) {
      this.hits.set(key, { count: 1, resetAt: now + this.options.windowMs });
      return { ok: true };
    }
    if (current.count >= this.options.limit) {
      return { ok: false, retryAfterSeconds: Math.max(1, Math.ceil((current.resetAt - now) / 1000)) };
    }
    current.count += 1;
    return { ok: true };
  }
}

@Injectable()
export class RateLimitGuard implements CanActivate {
  constructor(@Inject(RATE_LIMIT_OPTIONS) options: RateLimitOptions) {
    this.limiter = new RateLimiter(options);
  }

  private readonly limiter: RateLimiter;

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest<Request & { user?: AuthUser }>();
    if (!request.path.startsWith("/v1")) return true;
    const key = request.user?.sub ?? request.ip ?? "anonymous";
    const result = this.limiter.take(key);
    if (result.ok) return true;
    const response = context.switchToHttp().getResponse<Response>();
    response.setHeader("Retry-After", String(result.retryAfterSeconds));
    throw new ProblemError(429, "RATE_LIMITED", "Too Many Requests", "Rate limit exceeded");
  }
}
