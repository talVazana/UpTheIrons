"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { ProjectItem, fetchProjects } from "@/lib/api";
import { ProjectCard } from "@/components/projects/ProjectCard";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<ProjectItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedDifficulty, setSelectedDifficulty] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    async function loadProjects() {
      try {
        setLoading(true);
        const diff = selectedDifficulty !== "all" ? selectedDifficulty : undefined;
        const res = await fetchProjects({ difficulty: diff, q: searchQuery });
        setProjects(res.projects);
        setError(null);
      } catch (err: any) {
        setError(err.message || "Failed to load projects");
      } finally {
        setLoading(false);
      }
    }

    const timer = setTimeout(() => {
      loadProjects();
    }, 300);

    return () => clearTimeout(timer);
  }, [selectedDifficulty, searchQuery]);

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Header Banner */}
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3 border border-[#FF5722]/20 font-mono">
          Apprentice Path
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Projects Library
        </h1>
        <p className="text-neutral-400 mt-2 max-w-2xl text-sm sm:text-base leading-relaxed">
          Practical workshop builds designed to build muscle memory, hammer control, and forging discipline.
        </p>
      </div>

      {/* Filters */}
      <div className="mb-8 space-y-4 rounded-xl border border-neutral-800 bg-[#161616] p-4 sm:p-5">
        <div className="flex flex-col md:flex-row items-stretch md:items-center gap-3">
          <div className="relative flex-1">
            <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-neutral-500 text-sm">?"?</span>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search skills, tools, or topics..."
              className="w-full rounded-lg border border-neutral-700 bg-neutral-900/90 py-2.5 pl-10 pr-4 text-sm text-white placeholder-neutral-500 focus:border-[#FF5722] focus:outline-hidden focus:ring-1 focus:ring-[#FF5722]"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500 hover:text-white text-xs font-mono"
              >
                Clear
              </button>
            )}
          </div>
          
          <div className="flex items-center gap-2">
             <select
               value={selectedDifficulty}
               onChange={(e) => setSelectedDifficulty(e.target.value)}
               className="rounded-lg border border-neutral-700 bg-neutral-900/90 py-2.5 px-3 text-sm text-white focus:border-[#FF5722] focus:outline-hidden focus:ring-1 focus:ring-[#FF5722]"
             >
               <option value="all">All Difficulties</option>
               <option value="beginner">Beginner</option>
               <option value="intermediate">Intermediate</option>
               <option value="advanced">Advanced</option>
             </select>
          </div>
        </div>
      </div>

      {/* Grid */}
      {loading ? (
        <div className="py-20 text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-neutral-700 border-t-[#FF5722]" />
          <p className="mt-4 text-xs font-mono text-neutral-400">Loading projects...</p>
        </div>
      ) : error ? (
        <div className="rounded-xl border border-rose-500/30 bg-rose-950/20 p-6 text-center text-rose-300">
          <p className="text-sm font-semibold">{error}</p>
        </div>
      ) : projects.length === 0 ? (
        <div className="rounded-xl border border-neutral-800 bg-[#161616] p-12 text-center">
          <span className="text-3xl">?"?</span>
          <h3 className="mt-2 text-base font-bold text-white">No Projects Found</h3>
          <p className="mt-1 text-xs text-neutral-400">Try adjusting your filters.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((proj) => (
            <ProjectCard key={proj.id} project={proj} />
          ))}
        </div>
      )}
    </div>
  );
}
