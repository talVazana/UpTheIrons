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
