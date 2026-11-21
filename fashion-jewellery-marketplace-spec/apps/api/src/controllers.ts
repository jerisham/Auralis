import {
  Body,
  Controller,
  Get,
  HttpCode,
  Param,
  Patch,
  Post,
  Req,
  UseGuards,
  UseInterceptors,
} from "@nestjs/common";
import { ApiBearerAuth, ApiHeader, ApiOkResponse, ApiTags } from "@nestjs/swagger";
import type { RawBodyRequest } from "@nestjs/common";
import type { Request } from "express";
import { JwtAuthGuard, Roles, RolesGuard, type AuthUser } from "./auth";
import { newNonce, IdempotencyInterceptor } from "./idempotency";
import { ProblemError } from "./problem";
import { RateLimitGuard } from "./rate-limit";
import { RuntimeConfig } from "./config-cache";
import { WebhookService } from "./webhooks";

type AuthedRequest = Request & { user: AuthUser };

@ApiTags("health")
@Controller()
export class HealthController {
  @Get("health")
  @ApiOkResponse({ schema: { properties: { status: { type: "string" }, service: { type: "string" } } } })
  health(): { status: "ok"; service: string } {
    return { status: "ok", service: "auralis-api" };
  }
}

@ApiTags("foundation")
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard, RateLimitGuard)
@Controller("v1")
export class FoundationController {
  constructor(private readonly config: RuntimeConfig) {}

  @Get("me")
  @ApiOkResponse({ schema: { properties: { sub: { type: "string" }, roles: { type: "array" } } } })
  me(@Req() request: AuthedRequest): { sub: string; roles: string[] } {
    return { sub: request.user.sub, roles: request.user.roles };
  }

  @Get("admin/ping")
  @Roles("admin", "super_admin")
  ping(): { ok: true } {
    return { ok: true };
  }

  @Post("echo")
  @HttpCode(201)
  @UseInterceptors(IdempotencyInterceptor)
  @ApiHeader({ name: "Idempotency-Key", required: true })
  echo(): { nonce: string } {
    return { nonce: newNonce() };
  }

  @Get("config/:key")
  @Roles("admin", "super_admin")
  async readConfig(@Param("key") key: string): Promise<{ key: string; value: unknown }> {
    return { key, value: await this.config.get(key) };
  }

  @Patch("admin/config/:key")
  @Roles("super_admin")
  async writeConfig(
    @Param("key") key: string,
    @Body() body: { value: unknown },
  ): Promise<{ key: string; value: unknown }> {
    this.config.set(key, body.value);
    return { key, value: await this.config.get(key) };
  }
}

@ApiTags("webhooks")
@Controller()
export class WebhookController {
  constructor(private readonly webhooks: WebhookService) {}

  @Post("webhooks/:provider")
  @HttpCode(202)
  receive(
    @Param("provider") provider: string,
    @Req() request: RawBodyRequest<Request>,
  ): { id: string; status: string } {
    const raw = request.rawBody?.toString("utf8") ?? "";
    const signature = request.header("x-signature") ?? "";
    const record = this.webhooks.accept(provider, raw, signature);
    if (!record.signatureValid) {
      throw new ProblemError(401, "INVALID_SIGNATURE", "Invalid signature", "Webhook signature did not match", [
        { id: record.id },
      ]);
    }
    const processed = this.webhooks.process(record);
    return { id: processed.id, status: processed.status };
  }
}

@ApiTags("webhooks")
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard, RateLimitGuard)
@Controller("v1/admin/webhooks")
export class WebhookAdminController {
  constructor(private readonly webhooks: WebhookService) {}

  @Get(":id")
  @Roles("admin", "super_admin")
  get(@Param("id") id: string) {
    const record = this.webhooks.get(id);
    if (!record) throw new ProblemError(404, "NOT_FOUND", "Not Found", "Webhook not found");
    return record;
  }

  @Post(":id/reprocess")
  @Roles("admin", "super_admin")
  reprocess(@Param("id") id: string) {
    try {
      return this.webhooks.reprocess(id);
    } catch {
      throw new ProblemError(404, "NOT_FOUND", "Not Found", "Webhook not found");
    }
  }
}
