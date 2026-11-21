export type TokenMap = Record<string, string>;

export function renderCss(tokens: TokenMap): string {
  const lines = Object.entries(tokens).map(([name, value]) => `  --${name}: ${value};`);
  return `:root {\n${lines.join("\n")}\n}\n`;
}

export function renderTs(tokens: TokenMap): string {
  return `export const tokens = ${JSON.stringify(tokens, null, 2)} as const;\n`;
}

export function renderRn(tokens: TokenMap): string {
  const body = Object.entries(tokens)
    .map(([name, value]) => `  "${name}": "${value}"`)
    .join(",\n");
  return `export const theme = {\n${body}\n} as const;\n`;
}
