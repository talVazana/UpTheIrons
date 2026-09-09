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

export async function syncYouTubeChannel(id: string): Promise<{
  channel_id: string;
  name: string;
  status: string;
  last_synced_at: string;
  message: string;
}> {
  return fetchApi(`/api/youtube/channels/${id}/sync`, {
    method: "POST",
  });
}


