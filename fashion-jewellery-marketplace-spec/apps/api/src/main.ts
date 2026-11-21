import "reflect-metadata";
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";
import { ProblemFilter } from "./problem";

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule.register(), { rawBody: true });
  app.useGlobalFilters(new ProblemFilter());
  const port = Number(process.env.PORT ?? 3001);
  await app.listen(port);
}

void bootstrap();
