import { describe, expect, it } from "vitest";
import { createWorkerQueue } from "../src/main";

describe("worker", () => {
  it("starts a queue that can publish", async () => {
    const queue = createWorkerQueue();
    await queue.publish({ id: "boot", type: "worker.ready", payload: {} });
    const seen: string[] = [];
    await queue.drain(async (job) => {
      seen.push(job.type);
    });
    expect(seen).toEqual(["worker.ready"]);
  });
});
