import { InMemoryQueue } from "@auralis/events";

/** Local worker entry. BullMQ replaces the in-memory queue when REDIS_URL is set in a later slice. */
export function createWorkerQueue(): InMemoryQueue {
  return new InMemoryQueue();
}

if (require.main === module) {
  const queue = createWorkerQueue();
  console.log(`auralis worker ready (${queue.dead.length} dead letters)`);
}
