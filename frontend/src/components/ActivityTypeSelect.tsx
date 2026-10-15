import type {ActivityType} from "../api/client.ts";



type ActivityTypeSelectProps = {
    activities: ActivityType[];
    value: number | null;
    onChange: (id: number | null) => void;
    allowEmpty?: boolean;
    emptyLabel?: string;
};



function unitSummary(activity: ActivityType): string {
    const links = [...activity.unit_links];
    links.sort((a, b) => a.sort_order - b.sort_order);

    const names: string[] = [];
    let perSet = false;
    for (const link of links) {
        names.push(link.unit_type.name);
        if (link.per_set) {perSet = true;}}

    let summary = names.join(", ");
    if (perSet) {
        summary += " (sarjoittain)";}
    return summary;
}

function ActivityTypeSelect({activities, value, onChange, allowEmpty = false, emptyLabel = "Valitse"}: ActivityTypeSelectProps) {
    const systemActivities = activities.filter((a) => a.is_system);
    const ownActivities = activities.filter((a) => !a.is_system);
    const selected = activities.find((a) => a.id === value);

    let helperText = "";
    if (value !== null) {
        if (selected) {
            helperText = "Yksiköt: " + unitSummary(selected);
        } else {
            helperText = "Unknown exercise";
        }
    }

    return (
    <span>
        <select
            value={value === null ? "" : String(value)}
            onChange={(e) => onChange(e.target.value === "" ? null : Number(e.target.value))}
        >
            {allowEmpty && <option value="">{emptyLabel}</option>}
            <optgroup label="Exercises">
                {systemActivities.map((a) => (
                    <option key={a.id} value={a.id}>{a.name} — {unitSummary(a)}</option>
                ))}
            </optgroup>

            {ownActivities.length > 0 && (
                <optgroup label="Your exercises">
                    {ownActivities.map((a) => (
                        <option key={a.id} value={a.id}>{a.name} — {unitSummary(a)}</option>
                    ))}
                </optgroup>
            )}
        </select>
        {helperText && <small>{helperText}</small>}
    </span>
    );
}

export default ActivityTypeSelect;
