import Link from "next/link";
import Image from "next/image";

export function Footer() {
  return (
    <footer className="w-full border-t border-neutral-800 bg-[#0e0e0e] text-neutral-400 py-12 mt-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-3 text-white font-bold text-base mb-2">
              <div className="relative w-8 h-8">
                <Image src="/kiko.png" alt="Blacksmith Knight Logo" fill className="object-contain" />
              </div>
              <span>Blacksmith Knight &mdash; Forging Heaven</span>
            </div>
            <p className="text-sm text-neutral-400 max-w-md leading-relaxed mb-4">
              A digital blacksmith&apos;s workshop, knowledge vault, and technical reference for
              amateur makers, hobbyists, and craftspeople.
            </p>
            <div className="text-xs text-neutral-500">
              Personal-use first &bull; Non-commercial &bull; Local first
            </div>
          </div>

          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-200 mb-3">
              Knowledge
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/materials" className="hover:text-[#FF5722] transition-colors">
                  Materials &amp; Steel
                </Link>
              </li>
              <li>
                <Link href="/guides" className="hover:text-[#FF5722] transition-colors">
                  Technical Guides
                </Link>
              </li>
              <li>
                <Link href="/projects" className="hover:text-[#FF5722] transition-colors">
                  Apprentice Projects
                </Link>
              </li>
              <li>
                <Link href="/workshop" className="hover:text-[#FF5722] transition-colors">
                  Workshop &amp; Equipment
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-200 mb-3">
              Forge Library
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/videos" className="hover:text-[#FF5722] transition-colors">
                  Curated Videos
                </Link>
              </li>
              <li>
                <Link href="/sources" className="hover:text-[#FF5722] transition-colors">
                  Source Registry
                </Link>
              </li>
              <li>
                <Link href="/tools" className="hover:text-[#FF5722] transition-colors">
                  Tools &amp; Anvils
                </Link>
              </li>
              <li>
                <Link href="/rules" className="hover:text-[#FF5722] transition-colors">
                  Rules &amp; Safety Policy
                </Link>
              </li>
              <li>
                <Link href="/search" className="hover:text-[#FF5722] transition-colors">
                  Search Vault
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-neutral-800/80 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-neutral-500">
          <p>
            &copy; {new Date().getFullYear()} Blacksmith Knight. Knowledge shared for the love of the craft.
          </p>
          <div className="flex items-center gap-2 text-neutral-400 text-xs">
            <span className="inline-block w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>Local Architecture Baseline</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
