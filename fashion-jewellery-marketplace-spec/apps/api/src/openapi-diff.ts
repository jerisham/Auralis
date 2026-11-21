type Schema = { properties?: Record<string, unknown> };
type Response = { content?: Record<string, { schema?: Schema }> };
type Operation = { responses?: Record<string, Response> };
export type OpenApiDoc = { paths?: Record<string, Record<string, Operation>> };

export function breakingChanges(baseline: OpenApiDoc, next: OpenApiDoc): string[] {
  const problems: string[] = [];
  for (const [path, methods] of Object.entries(baseline.paths ?? {})) {
    const nextMethods = next.paths?.[path];
    if (!nextMethods) {
      problems.push(`removed path ${path}`);
      continue;
    }
    for (const [method, operation] of Object.entries(methods)) {
      const nextOperation = nextMethods[method];
      if (!nextOperation) {
        problems.push(`removed ${method.toUpperCase()} ${path}`);
        continue;
      }
      for (const [status, response] of Object.entries(operation.responses ?? {})) {
        const before = response.content?.["application/json"]?.schema?.properties;
        const after = nextOperation.responses?.[status]?.content?.["application/json"]?.schema?.properties;
        if (!before || !after) continue;
        for (const property of Object.keys(before)) {
          if (!(property in after)) {
            problems.push(`removed property ${property} on ${method.toUpperCase()} ${path} response ${status}`);
          }
        }
      }
    }
  }
  return problems;
}
