import type {ActivityType, Measurement, Session, SessionItem, SessionWrite} from "../api/client.ts";

export type MeasurementDraft = {
    unitTypeId: number;
    setIndex: number | null;
    planned: string;
    actual: string;
}

export type ItemDraft = {
    key: number;
    activityTypeId: number;
    notes: string;
    measurements: MeasurementDraft[];
}

export type SessionDraft = {
    name: string;
    sessionAt: string;
    status: string;
    planId: string;
    intensity: string;
    notes: string;
    items: ItemDraft[];
}

let nextKey = 1

export function emptyDraft(): SessionDraft {
    return {
        name: "",
        sessionAt: "",
        status: "planned",
        planId: "",
        intensity: "",
        notes: "",
        items: []
    }
}

export function emptyMeasurements(activity: ActivityType): MeasurementDraft[] {
    const measurements: MeasurementDraft[] = [];
    for (const link of activity.unit_links) {
        measurements.push({
            unitTypeId: link.unit_type_id,
            setIndex: link.per_set ? 0 : null,
            planned: "",
            actual: "",
        })
    }
    return measurements;
}

export function newItem(activity: ActivityType): ItemDraft {
    return {
        key: nextKey++,
        activityTypeId: activity.id,
        notes: "",
        measurements: emptyMeasurements(activity),
    }
}

function valueToText(value: number | null): string {
    if (value === null) {
        return ""}
    return String(value);
}

function measurementToDraft(measurement: Measurement): MeasurementDraft {
    return {
        unitTypeId: measurement.unit_type_id,
            setIndex: measurement.set_index,
        planned: valueToText(measurement.planned_value),
        actual: valueToText(measurement.actual_value),
    };
}

function itemMeasurements(item: SessionItem, activity: ActivityType | undefined): MeasurementDraft[] {
    if (!activity) {
        return item.measurements.map(measurementToDraft)}

    const result: MeasurementDraft[] = [];
    for (const link of activity.unit_links) {
        const rows = item.measurements.filter((m) => m.unit_type_id === link.unit_type_id);
        rows.sort((a, b) => (a.set_index ?? 0) - (b.set_index ?? 0));

        if (rows.length === 0) {
            result.push({
            unitTypeId: link.unit_type_id,
            setIndex: link.per_set ? 0 : null,
            planned: "",
            actual: "",
            });
        }
        for (const row of rows) {
            result.push(measurementToDraft(row));
        }
    }
    return result;
}

function padNumber(value: number): string {
    return String(value).padStart(2, "0")}

function toLocalInput(iso: string): string {
    const date = new Date(iso);
    return `${date.getFullYear()}-${padNumber(date.getMonth() + 1)}-${padNumber(date.getDate())}`
        + `T${padNumber(date.getHours())}:${padNumber(date.getMinutes())}`
}

export function draftFromSession(session: Session, activityTypes: ActivityType[]): SessionDraft {
    const items: ItemDraft[] = [];
    for (const item of session.items) {
        const activity = activityTypes.find((a) => a.id === item.activity_type_id);
        items.push({
            key: nextKey++,
            activityTypeId: item.activity_type_id,
            notes: item.notes ?? "",
            measurements: itemMeasurements(item, activity),
        });
    }

    return {
        name: session.name,
        sessionAt: session.session_at ? toLocalInput(session.session_at) : "",
        status: session.status,
        planId: session.plan_id ? String(session.plan_id) : "",
        intensity: session.intensity ? String(session.intensity) : "",
        notes: session.notes ?? "",
        items: items,
    };
}

function textToValue(text: string): number | null {
    if (text.trim() === "") {
        return null;
    }
    return Number(text);
}

export function toSessionWrite(draft: SessionDraft): SessionWrite {
    const body: SessionWrite = {
        name: draft.name.trim(),
        session_at: draft.sessionAt ? new Date(draft.sessionAt).toISOString() : null,
        status: draft.status,
        notes: draft.notes.trim() ? draft.notes.trim() : null,
        intensity: draft.intensity ? Number(draft.intensity) : null,
        items: [],
    };

    if (draft.planId) {
        body.plan_id = Number(draft.planId);
    }

    draft.items.forEach((item, index) => {
        const measurements = [];
        for (const m of item.measurements) {
            const planned = textToValue(m.planned);
            const actual = textToValue(m.actual);
            if (planned === null && actual === null) {
                continue;
            }
            measurements.push({
                unit_type_id: m.unitTypeId,
                planned_value: planned,
                actual_value: actual,
                set_index: m.setIndex,
            });
        }

        body.items.push({
            activity_type_id: item.activityTypeId,
            sort_order: index,
            notes: item.notes.trim() ? item.notes.trim() : null,
            measurements: measurements,
        });
    });

    return body;
}
