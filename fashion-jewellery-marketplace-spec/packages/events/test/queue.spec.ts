import { describe, expect, it } from "vitest";
import { InMemoryQueue } from "../src/index";

describe("in-memory queue", () => {
  it("retries a job killed mid-processing and does not lose it", async () => {
    const queue = new InMemoryQueue(3);
    let runs = 0;
    await queue.publish({ id: "evt-1", type: "order.paid", payload: { n: 1 } });
    await queue.drain(async () => {
      runs += 1;
      if (runs === 1) throw new Error("worker killed");
    });
    expect(runs).toBe(2);
    expect(queue.dead).toHaveLength(0);
  });

  it("does not apply a side-effect twice for the same job id", async () => {
    const queue = new InMemoryQueue();
    const seen: string[] = [];
    await queue.publish({ id: "evt-2", type: "order.paid", payload: {} });
    await queue.publish({ id: "evt-2", type: "order.paid", payload: {} });
    await queue.drain(async (job) => {
      seen.push(job.id);
    });
    expect(seen).toEqual(["evt-2"]);
  });

  it("sends a poison message to the dead-letter queue and alerts", async () => {
    const queue = new InMemoryQueue(3);
    await queue.publish({ id: "bad", type: "order.paid", payload: {} });
    await queue.publish({ id: "good", type: "order.paid", payload: {} });
    const applied: string[] = [];
    await queue.drain(async (job) => {
      if (job.id === "bad") throw new Error("poison");
      applied.push(job.id);
    });
    expect(applied).toEqual(["good"]);
    expect(queue.dead.map((job) => job.id)).toEqual(["bad"]);
    expect(queue.alerts).toHaveLength(1);
    expect(queue.alerts[0]?.error).toBe("poison");
  });
});
