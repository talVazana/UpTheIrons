/**
 * Domain TypeScript types synchronized with backend Pydantic models.
 */

export type ContentType =
  | "guide"
  | "article"
  | "material"
  | "video"
  | "product"
  | "project"
  | "workshop_tip"
  | "rule";

export type ContentStatus =
  | "draft"
  | "published"
  | "featured"
  | "pinned"
  | "verified"
  | "needs_review"
  | "archived"
  | "hidden";

export type TrustLabel =
  | "fact"
  | "source_backed_recommendation"
  | "craft_practice"
  | "personal_experience"
  | "historical_interpretation"
  | "ai_summary"
  | "opinion";


export type DifficultyLevel = "beginner" | "intermediate" | "advanced";

export type SourceType =
  | "youtube_channel"
  | "rss_feed"
  | "product_api"
  | "manual";

export interface SourceProvenance {
  source_type: SourceType;
  source_id: string;
  source_name: string;
  source_url: string;
  retrieved_at: string;
  source_updated_at?: string | null;
}

export interface ContentEnvelope<T = Record<string, unknown>> {
  id: string;
  type: ContentType;
  title: string;
  slug: string;
  summary: string;
  category: string;
  tags: string[];
  difficulty?: DifficultyLevel | null;
  source?: SourceProvenance | null;
  image_url?: string | null;
  status: ContentStatus;
  published_at?: string | null;
  created_at: string;
  updated_at: string;
  metadata: T;
}

export interface HeatTreatmentRecipe {
  normalizing_temp_f?: number | null;
  annealing_temp_f?: number | null;
  hardening_temp_f?: number | null;
  quench_medium?: string | null;
  tempering_range_f?: string | null;
  target_hardness_hrc?: string | null;
  notes?: string | null;
}

export interface MaterialMetadata {
  classification: string;
  carbon_pct: number;
  alloying_elements: Record<string, number>;
  forging_temp_range_f?: string | null;
  heat_treatment?: HeatTreatmentRecipe | null;
  beginner_suitability: boolean;
  common_applications: string[];
  common_mistakes: string[];
  source_reference?: string | null;
}

export interface VideoMetadata {
  youtube_video_id: string;
  channel_id: string;
  channel_name: string;
  duration_seconds: number;
  view_count?: number | null;
}

export interface ProjectMetadata {
  level: number;
  estimated_time_minutes: number;
  required_tools: string[];
  required_materials: string[];
  skills_learned: string[];
  steps: string[];
  safety_warnings: string[];
}

export interface SourceReference {
  title: string;
  author?: string | null;
  publication?: string | null;
  year?: number | null;
  url?: string | null;
  trust_label?: TrustLabel | null;
  citation_key?: string | null;
}

export interface SafetyPrecaution {
  level: "critical" | "warning" | "caution" | "mandatory_ppe" | string;
  hazard: string;
  mitigation: string;
  ppe: string[];
}

export interface RelatedContentLink {
  content_id: string;
  title: string;
  type: ContentType;
  slug: string;
  relationship: string;
}

export interface GuideMetadata {
  reading_time_minutes: number;
  trust_label: TrustLabel;
  author: string;
  version: string;
  content_markdown: string;
  source_references: SourceReference[];
  safety_precautions: SafetyPrecaution[];
  related_content: RelatedContentLink[];
  table_of_contents?: Array<{ id: string; title: string }>;
}

