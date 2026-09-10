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
  | "rule"
  | "tool";

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

export interface TemperingPoint {
  temp_f: number;
  hrc: string;
  toughness: string;
  color: string;
}

export interface HeatTreatmentRecipe {
  normalizing_temp_f?: number | null;
  annealing_temp_f?: number | null;
  hardening_temp_f?: number | null;
  decalescence_temp_f?: number | null;
  soak_time_minutes?: number | null;
  quench_medium?: string | null;
  tempering_range_f?: string | null;
  target_hardness_hrc?: string | null;
  tempering_table?: TemperingPoint[] | null;
  notes?: string | null;
}

export interface MaterialMetadata {
  classification: string;
  carbon_pct: number;
  alloying_elements: Record<string, number>;
  steel_category?: string;
  forging_temp_range_f?: string | null;
  heat_treatment?: HeatTreatmentRecipe | null;
  spark_testing_profile?: string | null;
  grinding_characteristics?: string | null;
  weldability?: string | null;
  corrosion_resistance?: string | null;
  confidence_score?: number;
  confidence_level?: string;
  beginner_suitability: boolean;
  common_applications: string[];
  common_mistakes: string[];
  source_reference?: string | null;
  source_metadata?: Record<string, string>;
}

export interface MaterialItem extends ContentEnvelope<MaterialMetadata> {}

export interface MaterialListResponse {
  materials: MaterialItem[];
  total: number;
  limit: number;
  offset: number;
}

export interface MaterialComparisonItem {
  id: string;
  slug: string;
  title: string;
  classification: string;
  steel_category: string;
  carbon_pct: number;
  alloying_elements: Record<string, number>;
  forging_temp_range_f?: string | null;
  hardening_temp_f?: number | null;
  quench_medium?: string | null;
  target_hardness_hrc?: string | null;
  beginner_suitability: boolean;
  confidence_score: number;
  confidence_level: string;
  source_reference?: string | null;
}

export interface MaterialComparisonResponse {
  items: MaterialComparisonItem[];
  compared_elements: string[];
  toughness_rank: string[];
  edge_retention_rank: string[];
  quench_speed_summary: Record<string, string>;
}

export interface VideoMetadata {
  youtube_video_id: string;
  channel_id: string;
  channel_name: string;
  duration_seconds: number;
  view_count?: number | null;
}

export interface ProjectStep {
  title: string;
  description: string;
  duration_minutes?: number | null;
  warning?: string | null;
}

export interface ProjectMetadata {
  difficulty_level: DifficultyLevel;
  estimated_time_minutes: number;
  required_tools: string[];
  required_materials: string[];
  skills_learned: string[];
  steps: ProjectStep[];
  safety_precautions: SafetyPrecaution[];
  troubleshooting: string[];
  variations: string[];
  source_references: SourceReference[];
  related_content: RelatedContentLink[];
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

export type ToolCategory =
  | "forging"
  | "heating"
  | "grinding"
  | "finishing"
  | "infrastructure";

export interface ToolMetadata {
  tool_category: ToolCategory;
  primary_purpose: string;
  essential_for: string[];
  selection_criteria: string[];
  beginner_guidance: string;
  beginner_friendly: boolean;
  diy_buildable: boolean;
  diy_alternatives: string[];
  maintenance_protocols: string[];
  safety_precautions: SafetyPrecaution[];
  specifications: Record<string, any>;
  related_tools: RelatedContentLink[];
  source_references: SourceReference[];
}

export interface ToolItem extends ContentEnvelope<ToolMetadata> {}

export interface ToolListResponse {
  tools: ToolItem[];
  total: number;
  limit: number;
  offset: number;
}

