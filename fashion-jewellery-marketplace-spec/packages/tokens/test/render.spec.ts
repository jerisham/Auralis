import { describe, expect, it } from "vitest";
import { renderCss, renderRn, renderTs } from "../src/index";

describe("token outputs", () => {
  it("keeps a changed gold token in CSS, TypeScript, and the React Native theme", () => {
    const tokens = { "gold-500": "#C9A227", "bg-base": "#0E0D10" };
    expect(renderCss(tokens)).toContain("--gold-500: #C9A227;");
    expect(renderTs(tokens)).toContain('"gold-500": "#C9A227"');
    expect(renderRn(tokens)).toContain('"gold-500": "#C9A227"');
  });
});
