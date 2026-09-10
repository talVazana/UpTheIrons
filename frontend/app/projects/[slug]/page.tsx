import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getProject } from "@/lib/api";

interface ProjectPageProps {
  params: {
    slug: string;
  };
}

export async function generateMetadata({ params }: ProjectPageProps): Promise<Metadata> {
  try {
    const project = await getProject(params.slug);
    return {
      title: `${project.title} ?" Blacksmith Knight`,
      description: project.summary,
    };
  } catch {
    return {
      title: "Project Not Found",
    };
  }
}

export default async function ProjectDetailPage({ params }: ProjectPageProps) {
  try {
    const project = await getProject(params.slug);
    const meta = project.metadata;

    return (
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-10">
        {/* Navigation */}
        <div className="mb-8">
          <Link
            href="/projects"
            className="text-sm font-mono text-neutral-400 hover:text-[#FF5722] transition-colors"
          >
            &larr; Back to Projects Library
          </Link>
        </div>

        {/* Header */}
        <div className="border-b border-neutral-800 pb-8 mb-8">
          <div className="flex items-center gap-3 mb-4">
            <span className="inline-block px-3 py-1 rounded-full text-xs font-mono font-bold uppercase tracking-wider bg-neutral-800 text-neutral-300 border border-neutral-700">
              {meta.difficulty_level}
            </span>
            <span className="text-sm font-mono text-neutral-400">
              ~{meta.estimated_time_minutes} minutes
            </span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight mb-4">
            {project.title}
          </h1>
          <p className="text-lg text-neutral-300 leading-relaxed max-w-3xl">
            {project.summary}
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content (Steps) */}
          <div className="lg:col-span-2 space-y-8">
            {/* Steps */}
            <section>
              <h2 className="text-2xl font-bold text-white mb-6 border-b border-neutral-800 pb-2">
                Forging Steps
              </h2>
              <div className="space-y-6">
                {meta.steps.map((step, idx) => (
                  <div key={idx} className="flex gap-4">
                    <div className="shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-neutral-800 border border-neutral-700 text-sm font-bold text-neutral-300 font-mono">
                      {idx + 1}
                    </div>
                    <div className="bg-[#1a1a1a] border border-neutral-800 rounded-xl p-5 flex-1">
                      <h3 className="text-lg font-bold text-white mb-2">{step.title}</h3>
                      <p className="text-sm text-neutral-300 leading-relaxed">{step.description}</p>
                      {(step.duration_minutes || step.warning) && (
                        <div className="mt-4 pt-4 border-t border-neutral-800/60 flex flex-wrap gap-4 text-xs font-mono">
                          {step.duration_minutes && (
                            <span className="text-neutral-400">Time: ~{step.duration_minutes} min</span>
                          )}
                          {step.warning && (
                            <span className="text-amber-400 flex items-center gap-1">
                              ⚠️ {step.warning}
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </section>
            
            {/* Troubleshooting & Variations */}
            {(meta.troubleshooting?.length > 0 || meta.variations?.length > 0) && (
              <section className="bg-neutral-900/50 border border-neutral-800 rounded-xl p-6">
                {meta.troubleshooting?.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
                      <span className="text-amber-500">?"?</span> Troubleshooting
                    </h3>
                    <ul className="list-disc list-inside space-y-2 text-sm text-neutral-300">
                      {meta.troubleshooting.map((item, i) => (
                        <li key={i}>{item}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {meta.variations?.length > 0 && (
                  <div>
                    <h3 className="text-lg font-bold text-white mb-3">Project Variations</h3>
                    <ul className="list-disc list-inside space-y-2 text-sm text-neutral-300">
                      {meta.variations.map((item, i) => (
                        <li key={i}>{item}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </section>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Required Tools */}
            <div className="bg-[#161616] border border-neutral-800 rounded-xl p-5">
              <h3 className="text-sm font-bold uppercase tracking-wider text-neutral-500 font-mono mb-4">Required Tools</h3>
              <ul className="space-y-2">
                {meta.required_tools.map((tool, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-neutral-300">
                    <span className="text-[#FF5722] mt-0.5">&bull;</span>
                    {tool}
                  </li>
                ))}
              </ul>
            </div>

            {/* Required Materials */}
            <div className="bg-[#161616] border border-neutral-800 rounded-xl p-5">
              <h3 className="text-sm font-bold uppercase tracking-wider text-neutral-500 font-mono mb-4">Required Material</h3>
              <ul className="space-y-2">
                {meta.required_materials.map((mat, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-neutral-300">
                    <span className="text-amber-400 mt-0.5">&bull;</span>
                    {mat}
                  </li>
                ))}
              </ul>
            </div>

            {/* Skills Learned */}
            <div className="bg-[#161616] border border-neutral-800 rounded-xl p-5">
              <h3 className="text-sm font-bold uppercase tracking-wider text-neutral-500 font-mono mb-4">Skills Learned</h3>
              <div className="flex flex-wrap gap-2">
                {meta.skills_learned.map((skill, i) => (
                  <span key={i} className="px-2 py-1 bg-neutral-800/80 rounded border border-neutral-700 text-xs text-neutral-300">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Safety */}
            {meta.safety_precautions && meta.safety_precautions.length > 0 && (
              <div className="bg-rose-950/20 border border-rose-900/30 rounded-xl p-5">
                <h3 className="text-sm font-bold uppercase tracking-wider text-rose-500 font-mono mb-4 flex items-center gap-2">
                  <span>⚠️</span> Safety First
                </h3>
                <div className="space-y-4">
                  {meta.safety_precautions.map((precaution, i) => (
                    <div key={i} className="text-sm">
                      <p className="font-bold text-white mb-1">{precaution.hazard}</p>
                      <p className="text-neutral-300 mb-2">{precaution.mitigation}</p>
                      {precaution.ppe && precaution.ppe.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 mt-2">
                          {precaution.ppe.map((item, j) => (
                            <span key={j} className="text-[10px] font-mono bg-rose-900/40 text-rose-300 px-1.5 py-0.5 rounded">
                              + {item}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  } catch (error) {
    notFound();
  }
}
