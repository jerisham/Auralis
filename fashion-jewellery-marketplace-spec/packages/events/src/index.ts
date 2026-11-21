export type QueueJob = {
  id: string;
  type: string;
  payload: unknown;
  attempts: number;
};

export type DlqAlert = {
  job: QueueJob;
  error: string;
};

/**
 * Transport used by the outbox relay. Tests use the in-memory queue.
 * BullMQ is the deployed transport (ADR 0003) and must preserve this behaviour:
 * retry, dead-letter, and no duplicate side-effects for the same job id.
 */
export interface JobQueue {
  publish(job: Omit<QueueJob, "attempts">): Promise<void>;
  drain(handler: (job: QueueJob) => Promise<void>): Promise<void>;
}

export class InMemoryQueue implements JobQueue {
  private pending: QueueJob[] = [];
  readonly dead: QueueJob[] = [];
  readonly alerts: DlqAlert[] = [];
  private readonly done = new Set<string>();

  constructor(private readonly maxAttempts = 3) {}

  async publish(job: Omit<QueueJob, "attempts">): Promise<void> {
    this.pending.push({ ...job, attempts: 0 });
  }

  async drain(handler: (job: QueueJob) => Promise<void>): Promise<void> {
    let guard = 0;
    while (this.pending.length > 0) {
      if (guard++ > 10_000) {
        throw new Error("queue drain did not finish");
      }
      const job = this.pending.shift();
      if (!job) break;
      if (this.done.has(job.id)) continue;
      try {
        await handler(job);
        this.done.add(job.id);
      } catch (error) {
        job.attempts += 1;
        const message = error instanceof Error ? error.message : "unknown";
        if (job.attempts >= this.maxAttempts) {
          this.dead.push(job);
          this.alerts.push({ job, error: message });
        } else {
          this.pending.push(job);
        }
      }
    }
  }
}
