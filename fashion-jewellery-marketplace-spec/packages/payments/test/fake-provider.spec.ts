import { describe, expect, it } from "vitest";
import { FakePaymentProvider, runPaymentContract } from "../src/index";

describe("FakePaymentProvider", () => {
  it("passes the shared payment contract", async () => {
    await expect(runPaymentContract(new FakePaymentProvider())).resolves.toBeUndefined();
  });

  it("rejects floating money", async () => {
    const provider = new FakePaymentProvider();
    await expect(
      provider.createOrder({ amountPaise: 10.5, currency: "INR", receipt: "x" }),
    ).rejects.toThrow(/paise/);
  });
});
