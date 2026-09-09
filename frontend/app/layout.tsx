import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Blacksmith Knight — Forging Heaven",
  description: "A digital workshop, forge library, and technical vault for amateur blacksmithing and bladesmithing.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#121212] text-[#e0e0e0] antialiased">
        {children}
      </body>
    </html>
  );
}
