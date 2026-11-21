import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

const publicDir = join(__dirname, "..", "public");

describe("PWA shell", () => {
  it("has a standalone manifest, an offline page, and a service worker that serves it", () => {
    const manifest = JSON.parse(readFileSync(join(publicDir, "manifest.webmanifest"), "utf8")) as {
      name: string;
      display: string;
      start_url: string;
    };
    expect(manifest.name).toBe("Auralis");
    expect(manifest.display).toBe("standalone");
    expect(manifest.start_url).toBe("/");
    const worker = readFileSync(join(publicDir, "sw.js"), "utf8");
    expect(worker).toContain("/offline.html");
    const offline = readFileSync(join(publicDir, "offline.html"), "utf8");
    expect(offline).toContain("You are offline");
  });
});
