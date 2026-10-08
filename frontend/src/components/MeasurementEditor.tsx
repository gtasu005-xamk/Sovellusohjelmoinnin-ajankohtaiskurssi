import type {ActivityType} from "../api/client.ts";
import type {MeasurementDraft} from "../sessions/draft.ts";

type MeasurementEditorProps = {
    activity: ActivityType;
    measurements: MeasurementDraft[];
    onChange: (measurements: MeasurementDraft[]) => void;
};

function MeasurementEditor({activity, measurements, onChange}: MeasurementEditorProps) {
    const singleLinks = activity.unit_links.filter((link) => !link.per_set);
    const setLinks = activity.unit_links.filter((link) => link.per_set);

    let setCount = 0;
    for (const m of measurements) {
        if (m.setIndex !== null && m.setIndex + 1 > setCount) {
            setCount = m.setIndex + 1;
        }
    }

    function findValue(unitTypeId: number, setIndex: number | null, field: "planned" | "actual"): string {
        const measurement = measurements.find((m) => m.unitTypeId === unitTypeId && m.setIndex === setIndex);
        if (!measurement) {
            return "";
        }
        return measurement[field];
    }

    function updateValue(unitTypeId: number, setIndex: number | null, field: "planned" | "actual", value: string) {
        let found = false;
        const updated = measurements.map((m) => {
            if (m.unitTypeId === unitTypeId && m.setIndex === setIndex) {
                found = true;
                return {...m, [field]: value};
            }
            return m;
        });

        if (!found) {
            const measurement: MeasurementDraft = {unitTypeId, setIndex, planned: "", actual: ""};
            measurement[field] = value;
            updated.push(measurement);
        }
        onChange(updated);
    }

    function addSet() {
        const updated = [...measurements];
        for (const link of setLinks) {
            updated.push({unitTypeId: link.unit_type_id, setIndex: setCount, planned: "", actual: ""});
        }
        onChange(updated);
    }

    function removeSet() {
        if (setCount <= 1) {
            return;
        }
        onChange(measurements.filter((m) => m.setIndex !== setCount - 1));
    }

    const setNumbers = [];
    for (let i = 0; i < setCount; i++) {
        setNumbers.push(i);
    }

    return (
        <div>
            {singleLinks.map((link) => (
                <div key={link.unit_type_id}>
                    <strong>{link.unit_type.name}</strong>
                    <label>
                        Planned
                        <input
                            type="number"
                            value={findValue(link.unit_type_id, null, "planned")}
                            onChange={(e) => updateValue(link.unit_type_id, null, "planned", e.target.value)}
                        />
                    </label>
                    <label>
                        Actual
                        <input
                            type="number"
                            value={findValue(link.unit_type_id, null, "actual")}
                            onChange={(e) => updateValue(link.unit_type_id, null, "actual", e.target.value)}
                        />
                    </label>
                </div>
            ))}

            {setLinks.length > 0 && (
                <div>
                    {setNumbers.map((setIndex) => (
                        <div key={setIndex}>
                            <strong>Set {setIndex + 1}</strong>
                            {setLinks.map((link) => (
                                <span key={link.unit_type_id}>
                                    <label>
                                        {link.unit_type.name} planned
                                        <input
                                            type="number"
                                            value={findValue(link.unit_type_id, setIndex, "planned")}
                                            onChange={(e) => updateValue(link.unit_type_id, setIndex, "planned", e.target.value)}
                                        />
                                    </label>
                                    <label>
                                        {link.unit_type.name} actual
                                        <input
                                            type="number"
                                            value={findValue(link.unit_type_id, setIndex, "actual")}
                                            onChange={(e) => updateValue(link.unit_type_id, setIndex, "actual", e.target.value)}
                                        />
                                    </label>
                                </span>
                            ))}
                        </div>
                    ))}
                    <button type="button" onClick={addSet}>Lisää sarja</button>
                    <button type="button" onClick={removeSet} disabled={setCount <= 1}>Poista sarja</button>
                </div>
            )}
        </div>
    );
}

export default MeasurementEditor;
