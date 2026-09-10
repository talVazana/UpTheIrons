import Link from "next/link";
import { ProjectItem } from "@/lib/api";

interface ProjectCardProps {
  project: ProjectItem;
}

export function ProjectCard({ project }: ProjectCardProps) {
  const meta = project.metadata;
  
  const difficultyColors = {
    beginner: "text-emerald-400 bg-emerald-400/10 border-emerald-400/20",
    intermediate: "text-amber-400 bg-amber-400/10 border-amber-400/20",
    advanced: "text-rose-400 bg-rose-400/10 border-rose-400/20",
  };

  const colorClass = difficultyColors[meta.difficulty_level] || "text-neutral-400 bg-neutral-800/50 border-neutral-700";

  return (
    <Link
      href={`/projects/${project.slug}`}
      className="group flex flex-col rounded-xl border border-neutral-800 bg-[#1a1a1a] p-5 hover:border-[#FF5722]/50 hover:bg-[#1f1f1f] transition-all"
    >
      <div className="flex items-center justify-between mb-3">
        <span className={`inline-block px-2.5 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider border ${colorClass}`}>
          {meta.difficulty_level}
        </span>
        <span className="text-xs text-neutral-500 font-mono">
          ~{meta.estimated_time_minutes} min
        </span>
      </div>

      <h3 className="text-lg font-bold text-white mb-2 group-hover:text-[#FF5722] transition-colors line-clamp-1">
        {project.title}
      </h3>

      <p className="text-sm text-neutral-400 mb-4 line-clamp-2 grow">
        {project.summary}
      </p>

      <div className="mt-auto space-y-3">
        {meta.skills_learned && meta.skills_learned.length > 0 && (
          <div>
            <span className="text-[10px] uppercase font-mono text-neutral-500 block mb-1">Skills Learned</span>
            <div className="flex flex-wrap gap-1.5">
              {meta.skills_learned.slice(0, 3).map((skill, i) => (
                <span key={i} className="px-1.5 py-0.5 bg-neutral-800/50 rounded text-xs text-neutral-300 truncate max-w-[120px]">
                  {skill}
                </span>
              ))}
              {meta.skills_learned.length > 3 && (
                <span className="px-1.5 py-0.5 bg-neutral-800/50 rounded text-xs text-neutral-500">
                  +{meta.skills_learned.length - 3}
                </span>
              )}
            </div>
          </div>
        )}

        <div className="border-t border-neutral-800/60 pt-3 flex items-center justify-between">
          <span className="text-[10px] uppercase font-mono text-neutral-500">
            {meta.steps.length} Steps
          </span>
          <span className="text-xs font-semibold text-neutral-400 group-hover:text-[#FF5722] transition-colors">
            View Project &rarr;
          </span>
        </div>
      </div>
    </Link>
  );
}
