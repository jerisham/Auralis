import { ArgumentsHost, Catch, ExceptionFilter, HttpException } from "@nestjs/common";
import type { Response } from "express";

export class ProblemError extends Error {
  constructor(
    readonly status: number,
    readonly code: string,
    readonly title: string,
    readonly detail: string,
    readonly errors: unknown[] = [],
  ) {
    super(detail);
  }
}

export type ProblemBody = {
  type: string;
  title: string;
  status: number;
  detail: string;
  code: string;
  errors: unknown[];
};

export function problemBody(status: number, code: string, title: string, detail: string, errors: unknown[] = []): ProblemBody {
  return {
    type: `https://auralis.local/problems/${code.toLowerCase()}`,
    title,
    status,
    detail,
    code,
    errors,
  };
}

@Catch()
export class ProblemFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost): void {
    const response = host.switchToHttp().getResponse<Response>();
    if (exception instanceof ProblemError) {
      response
        .status(exception.status)
        .type("application/problem+json")
        .json(problemBody(exception.status, exception.code, exception.title, exception.detail, exception.errors));
      return;
    }
    if (exception instanceof HttpException) {
      const status = exception.getStatus();
      const raw = exception.getResponse();
      const detail = typeof raw === "string" ? raw : JSON.stringify(raw);
      const code = status === 401 ? "UNAUTHENTICATED" : status === 403 ? "FORBIDDEN" : "HTTP_ERROR";
      response
        .status(status)
        .type("application/problem+json")
        .json(problemBody(status, code, exception.name, detail));
      return;
    }
    response
      .status(500)
      .type("application/problem+json")
      .json(problemBody(500, "INTERNAL", "Internal Server Error", "Unexpected error"));
  }
}
