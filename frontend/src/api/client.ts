import {clearToken, getToken} from "../auth/token.ts";
import type {SessionFilters} from "./queryKeys.ts";


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
    status: number;

    constructor(status: number, message: string) {
        super(message);
        this.status = status;
    }
}

export function failureMessage(error: Error): string {
    if (error instanceof ApiError) {
        return error.message;
    }
    if (error instanceof TypeError) {
        return "Palvelimeen ei saatu yhteyttä.";
    }
    return error.message;
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



export type Measurement = {
    id: number;
    unit_type_id: number;
    planned_value: number | null;
    actual_value: number | null;
    set_index: number | null;
}

export type SessionItem = {
    id: number;
    activity_type_id: number;
    sort_order: number;
    notes: string | null;
    measurements: Measurement[];
}

export type Session = {
    id: number;
    user_id: number;
    name: string;
    session_at: string | null;
    status: string;
    notes: string | null;
    intensity: number | null;
    plan_id: number | null;
    source_session_id: number | null;
    items: SessionItem[];
}

export type Plan = {
    id: number;
    name: string;
    notes: string | null;
    start_date: string | null;
    length_weeks: number | null;
}

export type PlanDetail = Plan & {
    sessions: Session[];
}

export type PlanWrite = {
    name: string;
    notes: string | null;
    start_date: string | null;
    length_weeks: number | null;
}

export type UnitLink = {
    unit_type_id: number;
    sort_order: number;
    is_required: boolean;
    per_set: boolean;
    unit_type: {
        id: number;
        name: string;
        slug: string;
    };
}

export type ActivityType = {
    id: number;
    name: string;
    slug: string;
    unit_links: UnitLink[];
    is_system: boolean;
}

export type SessionWrite = {
    name: string;
    session_at: string | null;
    status: string;
    notes: string | null;
    intensity: number | null;
    plan_id?: number;
    items: {
        activity_type_id: number;
        sort_order: number;
        notes: string | null;
        measurements: {
            unit_type_id: number;
            planned_value: number | null;
            actual_value: number | null;
            set_index: number | null;
        }[];
    }[];
}


export function listSessions(filters: SessionFilters): Promise<Session[]> {
    const params = new URLSearchParams();
    if (filters.from) {
        params.set("from", new Date(`${filters.from}T00:00:00`).toISOString());
    }
    if (filters.to) {
        params.set("to", new Date(`${filters.to}T23:59:59.999`).toISOString());
    }
    if (filters.status) {
        params.set("status", filters.status);
    }
    if (filters.activityTypeId !== undefined) {
        params.set("activity_type_id", String(filters.activityTypeId));
    }
    if (filters.unscheduled !== undefined) {
        params.set("unscheduled", String(filters.unscheduled));
    }
    if (filters.planId !== undefined) {
        params.set("plan_id", String(filters.planId));
    }
    const query = params.toString();
    return apiFetch<Session[]>(query ? `/sessions?${query}` : "/sessions");
}

export function listPlans(): Promise<Plan[]> {
    return apiFetch<Plan[]>("/plans");
}

export function listActivityTypes(): Promise<ActivityType[]> {
    return apiFetch<ActivityType[]>("/activity-types");
}

export function getSession(id: number): Promise<Session> {
    return apiFetch<Session>(`/sessions/${id}`);
}

export function createSession(body: SessionWrite): Promise<Session> {
    return apiFetch<Session>("/sessions", "POST", body);
}

export function updateSession(id: number, body: SessionWrite): Promise<Session> {
    return apiFetch<Session>(`/sessions/${id}`, "PATCH", body);
}

export function cloneSession(id: number, body: {name: string; session_at: string | null}): Promise<Session> {
    return apiFetch<Session>(`/sessions/${id}/clone`, "POST", body);
}

export function deleteSession(id: number): Promise<void> {
    return apiFetch<void>(`/sessions/${id}`, "DELETE");
}

export type CalendarEntry = {
    id: number;
    name: string;
    session_at: string;
    status: string;
    plan_id: number | null;
    source_session_id: number | null;
}

export function getCalendar(from: string, to: string, planId?: number): Promise<CalendarEntry[]> {
    const params = new URLSearchParams();
    params.set("from", from);
    params.set("to", to);
    if (planId !== undefined) {
        params.set("plan_id", String(planId));
    }
    return apiFetch<CalendarEntry[]>(`/calendar?${params.toString()}`);
}

export function getPlan(id: number): Promise<PlanDetail> {
    return apiFetch<PlanDetail>(`/plans/${id}`);
}

export function createPlan(body: PlanWrite): Promise<Plan> {
    return apiFetch<Plan>("/plans", "POST", body);
}

export function updatePlan(id: number, body: PlanWrite): Promise<Plan> {
    return apiFetch<Plan>(`/plans/${id}`, "PATCH", body);
}

export function deletePlan(id: number): Promise<void> {
    return apiFetch<void>(`/plans/${id}`, "DELETE");
}

export function attachSession(planId: number, sessionId: number): Promise<PlanDetail> {
    return apiFetch<PlanDetail>(`/plans/${planId}/sessions/${sessionId}`, "POST");
}

export function detachSession(planId: number, sessionId: number): Promise<PlanDetail> {
    return apiFetch<PlanDetail>(`/plans/${planId}/sessions/${sessionId}`, "DELETE");
}

