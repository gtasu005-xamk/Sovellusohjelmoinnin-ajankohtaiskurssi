export type SessionFilters = {
    from?: string;
    to?: string;
    status?: string;
    activityTypeId?: number;
    unscheduled?: boolean;
    planId?: number;
    page?: number;
    limit?: number;
}

export const queryKeys = {
    me: (token: string | null) => ["me", token],
    sessions: (filters: SessionFilters) => ["sessions", filters],
    session: (id: number) => ["sessions", "detail", id],
    plans: ["plans"],
    plan: (id: number) => ["plans", id],
    calendar: (from: string, to: string, planId?: number) => ["calendar", from, to, planId],
    activityTypes: ["activity-types"],
    goals: (active?: boolean) => ["goals", active],
};
