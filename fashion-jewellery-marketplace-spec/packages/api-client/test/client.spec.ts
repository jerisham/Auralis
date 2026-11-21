import { describe, expect, it } from "vitest";
import { ApiClient } from "../src/index";

describe("ApiClient", () => {
  it("builds a health request against the given origin", () => {
    const client = new ApiClient("http://localhost:3001");
    expect(client).toBeInstanceOf(ApiClient);
  });
});
