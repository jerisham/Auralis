import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { renderCss, renderRn, renderTs, type TokenMap } from "./index";

const root = join(__dirname, "..");
const tokens = JSON.parse(readFileSync(join(__dirname, "../src/tokens.json"), "utf8")) as TokenMap;
const out = join(root, "dist");
mkdirSync(out, { recursive: true });
writeFileSync(join(out, "tokens.css"), renderCss(tokens));
writeFileSync(join(out, "tokens.ts"), renderTs(tokens));
writeFileSync(join(out, "theme.ts"), renderRn(tokens));
