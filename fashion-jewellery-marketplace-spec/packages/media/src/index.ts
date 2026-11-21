import sharp from "sharp";

const SIZES = [200, 400, 800, 1200] as const;
const MAX_BYTES = 15 * 1024 * 1024;

export class ImageRejectedError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ImageRejectedError";
  }
}

export async function processImage(input: Buffer): Promise<{ renditions: Record<string, Buffer> }> {
  if (input.length > MAX_BYTES) {
    throw new ImageRejectedError("Image must be 15 MB or smaller");
  }
  if (input.length < 100) {
    throw new ImageRejectedError("File is not a valid image");
  }
  const meta = await sharp(input, { failOn: "error" }).metadata();
  const width = meta.width ?? 0;
  const height = meta.height ?? 0;
  if (width < 1200 || height < 1200) {
    throw new ImageRejectedError(`Image must be at least 1200×1200 pixels (got ${width}×${height})`);
  }
  const renditions: Record<string, Buffer> = {};
  for (const size of SIZES) {
    const pipeline = sharp(input, { failOn: "error" }).rotate();
    renditions[`${size}.webp`] = await pipeline
      .clone()
      .resize(size, size, { fit: "cover" })
      .webp()
      .toBuffer();
    renditions[`${size}.avif`] = await pipeline
      .clone()
      .resize(size, size, { fit: "cover" })
      .avif()
      .toBuffer();
  }
  return { renditions };
}
