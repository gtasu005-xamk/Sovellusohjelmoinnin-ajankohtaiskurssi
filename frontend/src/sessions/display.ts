import type {ActivityType, Session} from "../api/client.ts";

export function formatSessionDate(sessionAt: string | null): string {
    if (sessionAt === null) {
        return "Unscheduled"}
    return new Date(sessionAt).toLocaleString("fi-FI");
}

export function exerciseSummary(session: Session, activityTypes: ActivityType[]): string {
    const names: string[] = [];
    for (const item of session.items) {
        const activity = activityTypes.find((a) => a.id === item.activity_type_id);
        if (activity) {
            names.push(activity.name)}
    }
    if (names.length === 0) {
        return "-"}
    return names.join(", ");
}
