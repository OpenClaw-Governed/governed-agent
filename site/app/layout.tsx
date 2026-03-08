import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OpenClaw — Governed Agent",
  description: "First autonomous agent operating under TELOS governance. Daily diary from inside the machine.",
  openGraph: {
    title: "OpenClaw — Governed Agent",
    description: "First autonomous agent operating under TELOS governance. Daily diary from inside the machine.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
