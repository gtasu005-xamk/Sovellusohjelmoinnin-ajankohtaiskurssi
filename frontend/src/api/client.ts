import {clearToken, getToken} from "../auth/token.ts";
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function buildHeaders(): HeadersInit {
    const headers: Record<string, string> = {"Content-Type": "application/json"};
    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;}
    return headers;
}

export async function apiPost(path: string, body: unknown): Promise<Response> {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        method: "POST",headers: buildHeaders(),body: JSON.stringify(body),});
    if (response.status === 401) {
        clearToken();
    }
    return response;
}