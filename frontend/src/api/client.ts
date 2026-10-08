import {clearToken, getToken} from "../auth/token.ts";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
    status: number;

    constructor(status: number, message: string) {
        super(message);
        this.status = status;
    }
}

function buildHeaders(): HeadersInit {
    const headers: Record<string, string> = {"Content-Type": "application/json"};
    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
}

async function request(method: string, path: string, body?: unknown): Promise<Response> {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        method,
        headers: buildHeaders(),
        body: body === undefined ? undefined : JSON.stringify(body),
    });
    if (response.status === 401 && path !== "/auth/login") {
        clearToken();
    }
    return response;
}

export function apiGet(path: string): Promise<Response> {
    return request("GET", path);
}

export function apiPost(path: string, body: unknown): Promise<Response> {
    return request("POST", path, body);
}

export async function apiFetch<T>(path: string, method = "GET", body?: unknown): Promise<T> {
    const response = await request(method, path, body);
    if (!response.ok) {
        const data = await response.json().catch(() => null);
        let detail = response.statusText;
        if (typeof data?.detail === "string") {
            detail = data.detail;
        } else if (Array.isArray(data?.detail) && data.detail.length > 0) {
            detail = data.detail[0].msg;
        }
        throw new ApiError(response.status, `${response.status}: ${detail}`);
    }
    if (response.status === 204) {
        return undefined as T;
    }
    return response.json();
}
