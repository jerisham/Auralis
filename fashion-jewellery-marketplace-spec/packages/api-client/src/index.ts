export type Problem = {
  type: string;
  title: string;
  status: number;
  detail: string;
  code: string;
  errors: unknown[];
};

export type Health = { status: "ok"; service: string };

export class ApiClient {
  constructor(private readonly baseUrl: string) {}

  async health(): Promise<Health> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) throw new Error(`health ${response.status}`);
    return (await response.json()) as Health;
  }
}
