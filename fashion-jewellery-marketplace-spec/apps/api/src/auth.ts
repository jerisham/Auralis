import { CanActivate, ExecutionContext, Inject, Injectable, SetMetadata } from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import type { Request } from "express";
import jwt from "jsonwebtoken";
import { ProblemError } from "./problem";

export const JWT_SECRET = "JWT_SECRET";
export const ROLES_KEY = "roles";

export type AuthUser = {
  sub: string;
  roles: string[];
  vendor_id?: string;
  admin_role?: string;
};

export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);

export function signUser(user: AuthUser, secret: string): string {
  return jwt.sign(user, secret, { expiresIn: "15m" });
}

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(@Inject(JWT_SECRET) private readonly secret: string) {}

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest<Request & { user?: AuthUser }>();
    const header = request.header("authorization") ?? "";
    const token = header.startsWith("Bearer ") ? header.slice(7) : "";
    if (!token) {
      throw new ProblemError(401, "UNAUTHENTICATED", "Unauthorized", "Missing bearer token");
    }
    try {
      const payload = jwt.verify(token, this.secret) as AuthUser;
      request.user = {
        sub: payload.sub,
        roles: payload.roles ?? [],
        vendor_id: payload.vendor_id,
        admin_role: payload.admin_role,
      };
      return true;
    } catch {
      throw new ProblemError(401, "UNAUTHENTICATED", "Unauthorized", "Invalid or expired token");
    }
  }
}

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const roles = this.reflector.getAllAndOverride<string[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!roles || roles.length === 0) return true;
    const request = context.switchToHttp().getRequest<Request & { user?: AuthUser }>();
    const have = request.user?.roles ?? [];
    if (roles.some((role) => have.includes(role))) return true;
    throw new ProblemError(403, "FORBIDDEN", "Forbidden", "This action is not allowed for your role");
  }
}
