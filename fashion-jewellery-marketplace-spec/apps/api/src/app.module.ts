import { Module, type DynamicModule } from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import { JwtAuthGuard, JWT_SECRET, RolesGuard } from "./auth";
import { RuntimeConfig } from "./config-cache";
import { FoundationController, HealthController, WebhookAdminController, WebhookController } from "./controllers";
import { IdempotencyInterceptor, IdempotencyStore } from "./idempotency";
import { RATE_LIMIT_OPTIONS, RateLimitGuard, type RateLimitOptions } from "./rate-limit";
import { WebhookService } from "./webhooks";

@Module({})
export class AppModule {
  static register(options?: Partial<RateLimitOptions>): DynamicModule {
    const rateLimit: RateLimitOptions = {
      limit: options?.limit ?? Number(process.env.RATE_LIMIT_MAX ?? 100),
      windowMs: options?.windowMs ?? Number(process.env.RATE_LIMIT_WINDOW_MS ?? 60_000),
    };
    return {
      module: AppModule,
      controllers: [HealthController, FoundationController, WebhookController, WebhookAdminController],
      providers: [
        Reflector,
        { provide: JWT_SECRET, useValue: process.env.JWT_SECRET ?? "test-secret" },
        { provide: RATE_LIMIT_OPTIONS, useValue: rateLimit },
        IdempotencyStore,
        IdempotencyInterceptor,
        RateLimitGuard,
        JwtAuthGuard,
        RolesGuard,
        WebhookService,
        RuntimeConfig,
      ],
    };
  }
}
