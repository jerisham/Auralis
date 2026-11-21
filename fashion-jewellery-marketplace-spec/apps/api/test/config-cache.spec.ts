import { describe, expect, it } from "vitest";
import { ConfigCache } from "../src/config-cache";

describe("ConfigCache", () => {
  it("serves the new value once the ttl has elapsed", async () => {
    let stored = 48;
    const cache = new ConfigCache(60_000, async () => stored);
    expect(await cache.get("return_window_hours", 0)).toBe(48);
    stored = 24;
    expect(await cache.get("return_window_hours", 30_000)).toBe(48);
    expect(await cache.get("return_window_hours", 60_000)).toBe(24);
  });
});
