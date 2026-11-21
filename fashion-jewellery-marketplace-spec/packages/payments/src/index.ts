export type Tranche = "T1" | "T2";

export type CreateOrderInput = {
  amountPaise: number;
  currency: "INR";
  receipt: string;
};

export type HeldTransferInput = {
  vendorOrderId: string;
  tranche: Tranche;
  amountPaise: number;
};

export interface PaymentProvider {
  createOrder(input: CreateOrderInput): Promise<{ gatewayOrderId: string }>;
  createHeldTransfer(input: HeldTransferInput): Promise<{ transferId: string; status: "held" }>;
  releaseTransfer(transferId: string): Promise<{ status: "released" }>;
  reverseTransfer(transferId: string): Promise<{ status: "reversed" }>;
  refund(input: { paymentId: string; amountPaise: number }): Promise<{ refundId: string; status: "processed" }>;
  fetchSettlements(): Promise<Array<{ id: string; amountPaise: number }>>;
}

type Transfer = HeldTransferInput & { transferId: string; status: "held" | "released" | "reversed" };

function assertPaise(amount: number): void {
  if (!Number.isInteger(amount) || amount < 0) {
    throw new Error("Money must be a non-negative integer number of paise");
  }
}

/** In-memory gateway used by every test that is not hitting Razorpay sandbox. */
export class FakePaymentProvider implements PaymentProvider {
  private orders = 0;
  private transfers = 0;
  private refunds = 0;
  private readonly held = new Map<string, Transfer>();

  async createOrder(input: CreateOrderInput): Promise<{ gatewayOrderId: string }> {
    assertPaise(input.amountPaise);
    if (input.currency !== "INR") throw new Error("Only INR is supported");
    this.orders += 1;
    return { gatewayOrderId: `order_fake_${this.orders}` };
  }

  async createHeldTransfer(input: HeldTransferInput): Promise<{ transferId: string; status: "held" }> {
    assertPaise(input.amountPaise);
    this.transfers += 1;
    const transferId = `tr_fake_${this.transfers}`;
    this.held.set(transferId, { ...input, transferId, status: "held" });
    return { transferId, status: "held" };
  }

  async releaseTransfer(transferId: string): Promise<{ status: "released" }> {
    const transfer = this.require(transferId);
    if (transfer.status !== "held") throw new Error(`Cannot release a ${transfer.status} transfer`);
    transfer.status = "released";
    return { status: "released" };
  }

  async reverseTransfer(transferId: string): Promise<{ status: "reversed" }> {
    const transfer = this.require(transferId);
    if (transfer.status === "reversed") return { status: "reversed" };
    transfer.status = "reversed";
    return { status: "reversed" };
  }

  async refund(input: { paymentId: string; amountPaise: number }): Promise<{ refundId: string; status: "processed" }> {
    assertPaise(input.amountPaise);
    this.refunds += 1;
    return { refundId: `rf_fake_${this.refunds}`, status: "processed" };
  }

  async fetchSettlements(): Promise<Array<{ id: string; amountPaise: number }>> {
    return [...this.held.values()]
      .filter((transfer) => transfer.status === "released")
      .map((transfer) => ({ id: transfer.transferId, amountPaise: transfer.amountPaise }));
  }

  private require(transferId: string): Transfer {
    const transfer = this.held.get(transferId);
    if (!transfer) throw new Error(`Unknown transfer ${transferId}`);
    return transfer;
  }
}

export async function runPaymentContract(provider: PaymentProvider): Promise<void> {
  const order = await provider.createOrder({ amountPaise: 50000, currency: "INR", receipt: "ORD-2611-000001" });
  if (!order.gatewayOrderId) throw new Error("missing gateway order id");
  const t1 = await provider.createHeldTransfer({
    vendorOrderId: "vo_1",
    tranche: "T1",
    amountPaise: 31875,
  });
  const t2 = await provider.createHeldTransfer({
    vendorOrderId: "vo_1",
    tranche: "T2",
    amountPaise: 10625,
  });
  if (t1.status !== "held" || t2.status !== "held") throw new Error("transfers must be created on hold");
  await provider.releaseTransfer(t1.transferId);
  const settlements = await provider.fetchSettlements();
  if (!settlements.some((row) => row.id === t1.transferId && row.amountPaise === 31875)) {
    throw new Error("released T1 missing from settlements");
  }
  await provider.reverseTransfer(t2.transferId);
  const refund = await provider.refund({ paymentId: "pay_1", amountPaise: 10625 });
  if (refund.status !== "processed") throw new Error("refund was not processed");
}
