import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = { title: "Auralis admin" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, background: "#F7F3EC", color: "#1A1A1E" }}>{children}</body>
    </html>
  );
}
