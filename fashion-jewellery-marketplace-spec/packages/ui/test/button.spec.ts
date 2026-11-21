import { describe, expect, it } from "vitest";
import { Button } from "../src/index";

describe("Button", () => {
  it("is a function component", () => {
    expect(typeof Button).toBe("function");
  });
});
