import sharp from "sharp";
import { describe, expect, it } from "vitest";
import { processImage } from "../src/index";

async function jpeg(width: number, height: number, withExif = false): Promise<Buffer> {
  let image = sharp({
    create: {
      width,
      height,
      channels: 3,
      background: { r: 212, g: 175, b: 106 },
    },
  }).jpeg();
  if (withExif) {
    image = image.withMetadata({
      exif: {
        IFD0: {
          ImageDescription: "gps-probe",
        },
      },
    });
  }
  return image.toBuffer();
}

describe("processImage", () => {
  it("rejects an 800×800 upload with a clear error", async () => {
    const input = await jpeg(800, 800);
    await expect(processImage(input)).rejects.toThrow(/1200×1200/);
  });

  it("rejects a file over 15 MB", async () => {
    const input = Buffer.alloc(15 * 1024 * 1024 + 1, 1);
    await expect(processImage(input)).rejects.toThrow(/15 MB/);
  });

  it("writes 8 renditions and strips metadata", async () => {
    const input = await jpeg(1200, 1200, true);
    const before = await sharp(input).metadata();
    expect(before.exif).toBeTruthy();
    const started = Date.now();
    const { renditions } = await processImage(input);
    expect(Date.now() - started).toBeLessThan(30_000);
    expect(Object.keys(renditions).sort()).toEqual([
      "1200.avif",
      "1200.webp",
      "200.avif",
      "200.webp",
      "400.avif",
      "400.webp",
      "800.avif",
      "800.webp",
    ]);
    const after = await sharp(renditions["800.webp"]!).metadata();
    expect(after.exif).toBeUndefined();
    expect(after.width).toBe(800);
    expect(after.height).toBe(800);
  });
});
