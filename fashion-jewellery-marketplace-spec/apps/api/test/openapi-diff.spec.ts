import { describe, expect, it } from "vitest";
import { breakingChanges, type OpenApiDoc } from "../src/openapi-diff";

const baseline: OpenApiDoc = {
  paths: {
    "/v1/me": {
      get: {
        responses: {
          "200": {
            content: {
              "application/json": {
                schema: { properties: { sub: { type: "string" }, roles: { type: "array" } } },
              },
            },
          },
        },
      },
    },
  },
};

describe("OpenAPI breaking-change check", () => {
  it("fails when a response field is removed", () => {
    const next: OpenApiDoc = {
      paths: {
        "/v1/me": {
          get: {
            responses: {
              "200": {
                content: {
                  "application/json": {
                    schema: { properties: { sub: { type: "string" } } },
                  },
                },
              },
            },
          },
        },
      },
    };
    expect(breakingChanges(baseline, next)).toContain(
      "removed property roles on GET /v1/me response 200",
    );
  });

  it("allows an added field", () => {
    const next: OpenApiDoc = structuredClone(baseline);
    next.paths!["/v1/me"]!.get!.responses!["200"]!.content!["application/json"]!.schema!.properties!.extra = {
      type: "string",
    };
    expect(breakingChanges(baseline, next)).toEqual([]);
  });
});
