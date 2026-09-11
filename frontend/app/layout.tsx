import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/navigation/Navbar";
import { Footer } from "@/components/navigation/Footer";

export const metadata: Metadata = {
  title: "Kiko's BlackSmith Heaven",
  description:
    "A personal, amateur-friendly digital home for blacksmithing, bladesmithing, metallurgy, heat treatment, and practical workshop knowledge.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-[#121212] text-[#ededed] antialiased">
        {/* Accessible skip link */}
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-[#FF5722] focus:text-white focus:font-bold focus:rounded-md shadow-lg"
        >
          Skip to main content
        </a>

        <Navbar />

        <main id="main-content" tabIndex={-1} className="flex-1 outline-none">
          {children}
        </main>

        <Footer />
      </body>
    </html>
  );
}
