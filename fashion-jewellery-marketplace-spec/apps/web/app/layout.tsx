import type { Metadata } from "next";
import type { ReactNode } from "react";
import { RegisterSw } from "./register-sw";

export const metadata: Metadata = {
  title: "Auralis",
  description: "Fashion jewellery from independent sellers.",
  manifest: "/manifest.webmanifest",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, background: "#0E0D10", color: "#F7F3EC" }}>
        <RegisterSw />
        {children}
      </body>
    </html>
  );
}
