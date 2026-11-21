import "reflect-metadata";
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { NestFactory } from "@nestjs/core";
import { DocumentBuilder, SwaggerModule } from "@nestjs/swagger";
import { AppModule } from "./app.module";
import { breakingChanges, type OpenApiDoc } from "./openapi-diff";

async function document(): Promise<OpenApiDoc> {
  const app = await NestFactory.create(AppModule.register(), { logger: false, rawBody: true });
  const config = new DocumentBuilder()
    .setTitle("Auralis API")
    .setVersion("0.0.1")
    .addBearerAuth()
    .build();
  const doc = SwaggerModule.createDocument(app, config) as unknown as OpenApiDoc;
  await app.close();
  return doc;
}

async function main(): Promise<void> {
  const check = process.argv.includes("--check");
  const doc = await document();
  const target = join(__dirname, "..", "openapi.json");
  if (!check) {
    writeFileSync(target, `${JSON.stringify(doc, null, 2)}\n`);
    return;
  }
  const baseline = JSON.parse(readFileSync(target, "utf8")) as OpenApiDoc;
  const removed = breakingChanges(baseline, doc);
  if (removed.length > 0) {
    console.error(removed.join("\n"));
    process.exit(1);
  }
}

void main();
