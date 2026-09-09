"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

interface NavItem {
  name: string;
  href: string;
}

const navItems: NavItem[] = [
  { name: "Forge", href: "/" },
  { name: "Materials", href: "/materials" },
  { name: "Videos", href: "/videos" },
  { name: "Guides", href: "/guides" },
  { name: "Projects", href: "/projects" },
  { name: "Workshop", href: "/workshop" },
  { name: "Tools", href: "/tools" },
  { name: "Rules", href: "/rules" },
  { name: "Search", href: "/search" },
];

export function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-neutral-800 bg-[#121212]/95 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8 h-16">
        {/* Brand */}
        <Link
          href="/"
          className="flex items-center gap-3 rounded-md px-2 py-1 text-white hover:text-[#FF5722] transition-colors focus-visible:ring-2 focus-visible:ring-[#FF5722]"
        >
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-[#FF5722]/10 border border-[#FF5722]/30 text-[#FF5722] font-bold text-base">
            &#x2692;
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold tracking-tight text-sm sm:text-base leading-tight">
              Blacksmith Knight
            </span>
            <span className="text-[10px] tracking-widest uppercase text-neutral-400">
              Forging Heaven
            </span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden lg:flex items-center gap-1" aria-label="Main Navigation">
          {navItems.map((item) => {
            const isActive =
              item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors focus-visible:ring-2 focus-visible:ring-[#FF5722] ${
                  isActive
                    ? "bg-neutral-800 text-[#FF5722] font-semibold border-b-2 border-[#FF5722]"
                    : "text-neutral-300 hover:bg-neutral-850 hover:text-white"
                }`}
                aria-current={isActive ? "page" : undefined}
              >
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Mobile menu toggle */}
        <div className="flex lg:hidden">
          <button
            type="button"
            className="inline-flex items-center justify-center rounded-md p-2 text-neutral-400 hover:bg-neutral-800 hover:text-white focus-visible:ring-2 focus-visible:ring-[#FF5722]"
            aria-controls="mobile-menu"
            aria-expanded={mobileMenuOpen}
            aria-label="Toggle navigation menu"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <span className="sr-only">Toggle main menu</span>
            {mobileMenuOpen ? (
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Mobile menu drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-neutral-800 bg-[#171717]" id="mobile-menu">
          <nav className="space-y-1 px-4 pt-2 pb-4" aria-label="Mobile Navigation">
            {navItems.map((item) => {
              const isActive =
                item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`block rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-neutral-800 text-[#FF5722] font-semibold"
                      : "text-neutral-300 hover:bg-neutral-800 hover:text-white"
                  }`}
                  aria-current={isActive ? "page" : undefined}
                >
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
      )}
    </header>
  );
}
