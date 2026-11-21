export class ConfigCache {
  private readonly entries = new Map<string, { value: unknown; at: number }>();

  constructor(
    private readonly ttlMs: number,
    private readonly read: (key: string) => Promise<unknown>,
  ) {}

  async get(key: string, now = Date.now()): Promise<unknown> {
    const hit = this.entries.get(key);
    if (hit && now - hit.at < this.ttlMs) return hit.value;
    const value = await this.read(key);
    this.entries.set(key, { value, at: now });
    return value;
  }

  invalidate(key: string): void {
    this.entries.delete(key);
  }
}

export class RuntimeConfig {
  private readonly values = new Map<string, unknown>([
    ["return_window_hours", 48],
    ["accept_sla_hours", 24],
    ["dispatch_sla_hours", 72],
    ["t1_percent", 75],
    ["commission_rate_bps", 1500],
  ]);
  private readonly cache = new ConfigCache(60_000, async (key) => this.values.get(key));

  get(key: string): Promise<unknown> {
    return this.cache.get(key);
  }

  set(key: string, value: unknown): void {
    this.values.set(key, value);
    this.cache.invalidate(key);
  }
}
