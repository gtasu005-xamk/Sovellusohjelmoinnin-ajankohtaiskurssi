const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export function apiPost(path: string, body: unknown): Promise<Response> {
    return fetch(`${API_BASE_URL}${path}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body),
    });
}
