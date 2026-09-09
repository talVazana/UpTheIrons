/**
 * API client for Blacksmith Knight backend.
 */

export const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  environment: string;
  diagnostics?: {
    firestore_emulator?: {
      host: string;
      project_id: string;
      reachable: boolean;
    };
  };
}

export interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
}

export class ApiError extends Error {
  code: string;
  status: number;
  details?: unknown;

  constructor(status: number, code: string, message: string, details?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

/**
 * Generic fetch wrapper with typed error envelopes.
 */
export async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${BACKEND_URL}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      let errorData: ApiErrorResponse | null = null;
      try {
        errorData = await response.json();
      } catch {
        // Response wasn't JSON
      }

      throw new ApiError(
        response.status,
        errorData?.error?.code || `HTTP_${response.status}`,
        errorData?.error?.message || `Request failed with status ${response.status}`,
        errorData?.error?.details
      );
    }

    return (await response.json()) as T;
  } catch (err: unknown) {
    if (err instanceof ApiError) {
      throw err;
    }
    const message = err instanceof Error ? err.message : "Network error";
    throw new ApiError(0, "NETWORK_ERROR", message);
  }
}

/**
 * Safe health check that never throws, returning status payload or error string.
 */
export async function checkBackendHealth(): Promise<{
  ok: boolean;
  data?: HealthResponse;
  error?: string;
}> {
  try {
    const data = await fetchApi<HealthResponse>("/api/health", {
      cache: "no-store",
    });
    return { ok: true, data };
  } catch (err: unknown) {
    const errorMsg =
      err instanceof ApiError
        ? `${err.code}: ${err.message}`
        : err instanceof Error
        ? err.message
        : "Backend unreachable";
    return { ok: false, error: errorMsg };
  }
}

export interface SourceItem {
  id: string;
  name: string;
  type: "youtube_channel" | "rss_feed" | "product_api" | "manual";
  platform: string;
  url: string;
  enabled: boolean;
  priority: number;
  categories: string[];
  status: "configured" | "healthy" | "warning" | "failed" | "disabled";
  last_synced_at?: string | null;
  last_error?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateSourceInput {
  name: string;
  type: string;
  platform: string;
  url: string;
  priority?: number;
  categories?: string[];
  enabled?: boolean;
}

export async function fetchSources(params?: {
  type?: string;
  enabled?: boolean;
}): Promise<SourceItem[]> {
  const query = new URLSearchParams();
  if (params?.type) query.set("type", params.type);
  if (params?.enabled !== undefined) query.set("enabled", String(params.enabled));
  const qs = query.toString() ? `?${query.toString()}` : "";
  return fetchApi<SourceItem[]>(`/api/sources${qs}`, { cache: "no-store" });
}

export async function createSource(input: CreateSourceInput): Promise<SourceItem> {
  return fetchApi<SourceItem>("/api/sources", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateSource(
  id: string,
  input: Partial<CreateSourceInput> & { status?: string }
): Promise<SourceItem> {
  return fetchApi<SourceItem>(`/api/sources/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function deleteSource(id: string): Promise<boolean> {
  await fetchApi<{ deleted: boolean }>(`/api/sources/${id}`, {
    method: "DELETE",
  });
  return true;
}

export async function testSourceConnection(id: string): Promise<{
  source_id: string;
  reachable: boolean;
  status: string;
  details: string;
}> {
  return fetchApi(`/api/sources/${id}/test`, {
    method: "POST",
  });
}

export interface YouTubeChannelItem {
  id: string;
  name: string;
  type: "youtube_channel";
  platform: string;
  url: string;
  youtube_channel_id: string;
  handle?: string | null;
  thumbnail_url?: string | null;
  video_count: number;
  enabled: boolean;
  priority: number;
  categories: string[];
  status: "configured" | "healthy" | "warning" | "failed" | "disabled";
  last_synced_at?: string | null;
  last_error?: string | null;
  created_at: string;
  updated_at: string;
}

export interface YouTubeChannelListResponse {
  channels: YouTubeChannelItem[];
  total: number;
}

export interface CreateYouTubeChannelInput {
  url_or_handle: string;
  name?: string;
  priority?: number;
  categories?: string[];
  thumbnail_url?: string;
}

export interface ResolveChannelResult {
  youtube_channel_id: string;
  handle: string | null;
  canonical_url: string;
  name: string;
  thumbnail_url: string;
  video_count: number;
  resolved_via_api: boolean;
}

export async function fetchYouTubeChannels(params?: {
  enabled?: boolean;
  category?: string;
}): Promise<YouTubeChannelListResponse> {
  const query = new URLSearchParams();
  if (params?.enabled !== undefined) query.set("enabled", String(params.enabled));
  if (params?.category) query.set("category", params.category);
  const qs = query.toString() ? `?${query.toString()}` : "";
  return fetchApi<YouTubeChannelListResponse>(`/api/youtube/channels${qs}`, {
    cache: "no-store",
  });
}

export async function resolveYouTubeChannel(query: string): Promise<ResolveChannelResult> {
  return fetchApi<ResolveChannelResult>("/api/youtube/resolve", {
    method: "POST",
    body: JSON.stringify({ query }),
  });
}

export async function createYouTubeChannel(
  input: CreateYouTubeChannelInput
): Promise<YouTubeChannelItem> {
  return fetchApi<YouTubeChannelItem>("/api/youtube/channels", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateYouTubeChannel(
  id: string,
  input: Partial<CreateYouTubeChannelInput> & { enabled?: boolean; status?: string }
): Promise<YouTubeChannelItem> {
  return fetchApi<YouTubeChannelItem>(`/api/youtube/channels/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function deleteYouTubeChannel(id: string): Promise<boolean> {
  await fetchApi<{ deleted: boolean }>(`/api/youtube/channels/${id}`, {
    method: "DELETE",
  });
  return true;
}

export interface VideoItem {
  id: string;
  type: string;
  title: string;
  slug: string;
  summary: string;
  category: string;
  tags: string[];
  difficulty?: string;
  image_url?: string;
  published_at?: string;
  created_at: string;
  source?: {
    source_type: string;
    source_id: string;
    source_name: string;
    source_url: string;
  };
  metadata?: {
    youtube_video_id?: string;
    channel_id?: string;
    channel_name?: string;
    duration_seconds?: number;
    embed_url?: string;
  };
}

export interface VideoListResponse {
  videos: VideoItem[];
  total: number;
  limit: number;
  offset: number;
}

export interface SyncSummaryItem {
  channel_id: string;
  channel_name: string;
  discovered: number;
  new_items: number;
  duplicates: number;
  errors: string[];
  started_at: string;
  completed_at?: string;
  status: string;
}

export interface ApiKeysStatus {
  youtube_api_key_configured: boolean;
  youtube_api_key_masked: string | null;
  ai_api_key_configured: boolean;
  ai_api_key_masked: string | null;
}

export async function syncYouTubeChannel(id: string): Promise<SyncSummaryItem> {
  return fetchApi<SyncSummaryItem>(`/api/youtube/channels/${id}/sync`, {
    method: "POST",
  });
}

export async function syncAllYouTubeChannels(): Promise<SyncSummaryItem[]> {
  return fetchApi<SyncSummaryItem[]>("/api/youtube/sync", {
    method: "POST",
  });
}

export async function fetchVideos(params?: {
  category?: string;
  tag?: string;
  channel_id?: string;
  limit?: number;
  offset?: number;
}): Promise<VideoListResponse> {
  const query = new URLSearchParams();
  if (params?.category) query.set("category", params.category);
  if (params?.tag) query.set("tag", params.tag);
  if (params?.channel_id) query.set("channel_id", params.channel_id);
  if (params?.limit) query.set("limit", String(params.limit));
  if (params?.offset) query.set("offset", String(params.offset));
  const qs = query.toString() ? `?${query.toString()}` : "";
  return fetchApi<VideoListResponse>(`/api/v1/videos${qs}`, {
    cache: "no-store",
  });
}

export async function fetchVideo(id: string): Promise<VideoItem> {
  return fetchApi<VideoItem>(`/api/v1/videos/${id}`, {
    cache: "no-store",
  });
}

export async function fetchApiKeysStatus(): Promise<ApiKeysStatus> {
  return fetchApi<ApiKeysStatus>("/api/v1/settings/keys", {
    cache: "no-store",
  });
}

export async function updateApiKeys(keys: {
  youtube_api_key?: string;
  ai_api_key?: string;
}): Promise<ApiKeysStatus> {
  return fetchApi<ApiKeysStatus>("/api/v1/settings/keys", {
    method: "POST",
    body: JSON.stringify(keys),
  });
}

export async function fetchSyncLogs(): Promise<{ logs: SyncSummaryItem[]; total: number }> {
  return fetchApi<{ logs: SyncSummaryItem[]; total: number }>("/api/youtube/sync-logs", {
    cache: "no-store",
  });
}

export interface RSSFeedItem {
  id: string;
  name: string;
  type: string;
  platform: string;
  url: string;
  feed_url: string;
  site_url?: string;
  feed_format?: string;
  enabled: boolean;
  priority: number;
  categories: string[];
  status: "configured" | "healthy" | "warning" | "failed" | "disabled";
  article_count: number;
  last_synced_at?: string | null;
  last_error?: string | null;
  created_at: string;
  updated_at: string;
}

export interface RSSSyncSummaryItem {
  feed_id: string;
  feed_name: string;
  discovered: number;
  new_items: number;
  duplicates: number;
  errors: string[];
  started_at: string;
  completed_at?: string;
  status: string;
}

export interface ArticleItem {
  id: string;
  type: string;
  title: string;
  slug: string;
  summary: string;
  category: string;
  tags: string[];
  difficulty?: string;
  image_url?: string;
  published_at?: string;
  created_at: string;
  source?: {
    source_type: string;
    source_id: string;
    source_name: string;
    source_url: string;
  };
  metadata?: {
    article_url?: string;
    author?: string;
    feed_id?: string;
    feed_name?: string;
  };
}

export interface ArticleListResponse {
  articles: ArticleItem[];
  total: number;
  limit: number;
  offset: number;
}

export async function fetchRSSFeeds(params?: {
  enabled?: boolean;
  category?: string;
}): Promise<{ feeds: RSSFeedItem[]; total: number }> {
  const query = new URLSearchParams();
  if (params?.enabled !== undefined) query.set("enabled", String(params.enabled));
  if (params?.category) query.set("category", params.category);
  const qs = query.toString() ? `?${query.toString()}` : "";
  return fetchApi<{ feeds: RSSFeedItem[]; total: number }>(`/api/v1/rss/feeds${qs}`, {
    cache: "no-store",
  });
}

export async function createRSSFeed(input: {
  url: string;
  name?: string;
  priority?: number;
  categories?: string[];
}): Promise<RSSFeedItem> {
  return fetchApi<RSSFeedItem>("/api/v1/rss/feeds", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateRSSFeed(
  id: string,
  input: Partial<{ name: string; enabled: boolean; priority: number; categories: string[]; status: string }>
): Promise<RSSFeedItem> {
  return fetchApi<RSSFeedItem>(`/api/v1/rss/feeds/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function deleteRSSFeed(id: string): Promise<boolean> {
  await fetchApi(`/api/v1/rss/feeds/${id}`, {
    method: "DELETE",
  });
  return true;
}

export async function syncRSSFeed(id: string): Promise<RSSSyncSummaryItem> {
  return fetchApi<RSSSyncSummaryItem>(`/api/v1/rss/feeds/${id}/sync`, {
    method: "POST",
  });
}

export async function syncAllRSSFeeds(): Promise<RSSSyncSummaryItem[]> {
  return fetchApi<RSSSyncSummaryItem[]>("/api/v1/rss/sync", {
    method: "POST",
  });
}

export async function fetchArticles(params?: {
  category?: string;
  tag?: string;
  feed_id?: string;
  limit?: number;
  offset?: number;
}): Promise<ArticleListResponse> {
  const query = new URLSearchParams();
  if (params?.category) query.set("category", params.category);
  if (params?.tag) query.set("tag", params.tag);
  if (params?.feed_id) query.set("feed_id", params.feed_id);
  if (params?.limit) query.set("limit", String(params.limit));
  if (params?.offset) query.set("offset", String(params.offset));
  const qs = query.toString() ? `?${query.toString()}` : "";
  return fetchApi<ArticleListResponse>(`/api/v1/articles${qs}`, {
    cache: "no-store",
  });
}

export async function fetchArticle(id: string): Promise<ArticleItem> {
  return fetchApi<ArticleItem>(`/api/v1/articles/${id}`, {
    cache: "no-store",
  });
}

export interface ProductItem {
  id: string;
  type: string;
  title: string;
  slug: string;
  summary: string;
  category: string;
  tags: string[];
  difficulty?: string;
  image_url?: string;
  source?: {
    source_type: string;
    source_id: string;
    source_name: string;
    source_url: string;
  };
  metadata: {
    sku: string;
    platform: string;
    price: number;
    currency: string;
    price_updated_at?: string;
    purchase_url: string;
    pros: string[];
    cons: string[];
    beginner_suitable: boolean;
    alternatives: string[];
    affiliate: boolean;
  };
}

export interface ProductListResponse {
  products: ProductItem[];
  total: number;
  limit: number;
  offset: number;
}

export interface ProductSourceItem {
  id: string;
  name: string;
  type: string;
  platform: string;
  url: string;
  catalog_url: string;
  vendor_name?: string;
  enabled: boolean;
  priority: number;
  categories: string[];
  status: "configured" | "healthy" | "warning" | "failed" | "disabled";
  item_count: number;
  last_synced_at?: string | null;
  last_error?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProductSyncSummaryItem {
  source_id: string;
  vendor_name: string;
  discovered: number;
  new_items: number;
  duplicates: number;
  price_updates: number;
  errors: string[];
  started_at: string;
  completed_at?: string;
  status: string;
}

export async function fetchProducts(params?: {
  category?: string;
  tag?: string;
  beginner_only?: boolean;
  max_price?: number;
  limit?: number;
  offset?: number;
}): Promise<ProductListResponse> {
  const query = new URLSearchParams();
  if (params?.category) query.set("category", params.category);
  if (params?.tag) query.set("tag", params.tag);
  if (params?.beginner_only !== undefined) query.set("beginner_only", String(params.beginner_only));
  if (params?.max_price !== undefined) query.set("max_price", String(params.max_price));
  if (params?.limit) query.set("limit", String(params.limit));
  if (params?.offset) query.set("offset", String(params.offset));
  const qs = query.toString() ? `?${query.toString()}` : "";
  return fetchApi<ProductListResponse>(`/api/v1/products${qs}`, {
    cache: "no-store",
  });
}

export async function fetchProduct(id: string): Promise<ProductItem> {
  return fetchApi<ProductItem>(`/api/v1/products/${id}`, {
    cache: "no-store",
  });
}

export async function fetchProductSources(params?: {
  enabled?: boolean;
}): Promise<{ sources: ProductSourceItem[]; total: number }> {
  const query = new URLSearchParams();
  if (params?.enabled !== undefined) query.set("enabled", String(params.enabled));
  const qs = query.toString() ? `?${query.toString()}` : "";
  return fetchApi<{ sources: ProductSourceItem[]; total: number }>(`/api/v1/products/sources${qs}`, {
    cache: "no-store",
  });
}

export async function createProductSource(input: {
  catalog_url: string;
  name: string;
  platform?: string;
  priority?: number;
  categories?: string[];
}): Promise<ProductSourceItem> {
  return fetchApi<ProductSourceItem>("/api/v1/products/sources", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function syncProductSource(id: string): Promise<ProductSyncSummaryItem> {
  return fetchApi<ProductSyncSummaryItem>(`/api/v1/products/sources/${id}/sync`, {
    method: "POST",
  });
}

export async function syncAllProductSources(): Promise<ProductSyncSummaryItem[]> {
  return fetchApi<ProductSyncSummaryItem[]>("/api/v1/products/sync", {
    method: "POST",
  });
}


