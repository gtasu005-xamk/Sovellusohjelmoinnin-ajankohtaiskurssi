import {useState, type FormEvent} from "react";
import {useNavigate, useParams} from "react-router-dom";
import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {ApiError,createSession, getSession, listActivityTypes, listPlans, updateSession,
        type ActivityType, type Plan, type SessionWrite,} from "../api/client.ts";
import {queryKeys} from "../api/queryKeys.ts";
import {draftFromSession, emptyDraft, emptyMeasurements, newItem, toSessionWrite,
        type ItemDraft, type SessionDraft} from "../sessions/draft.ts";
import MeasurementEditor from "../components/MeasurementEditor.tsx";

type SessionFormProps = {
    sessionId: number | null;
    initialDraft: SessionDraft;
    activityTypes: ActivityType[];
    plans: Plan[];
};

function SessionForm({sessionId, initialDraft, activityTypes, plans}: SessionFormProps) {
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [draft, setDraft] = useState<SessionDraft>(initialDraft);
    const [newActivityId, setNewActivityId] = useState("");
    const [formError, setFormError] = useState<string | null>(null);
    const [saved, setSaved] = useState(false);

    const mutation = useMutation({
        mutationFn: (body: SessionWrite) => {
            if (sessionId === null) {
                return createSession(body);
            }
            return updateSession(sessionId, body);
        },
        onSuccess: (session) => {
            queryClient.invalidateQueries({queryKey: ["sessions"]});
            queryClient.invalidateQueries({queryKey: ["calendar"]});
            if (sessionId === null) {
                navigate(`/sessions/${session.id}`);
            } else {
                setSaved(true);
            }
        },
    });

    function findActivity(id: number): ActivityType | undefined {
        return activityTypes.find((a) => a.id === id);
    }

    function updateItem(index: number, item: ItemDraft) {
        const items = [...draft.items];
        items[index] = item;
        setDraft({...draft, items: items});
        setSaved(false);
    }

    function addItem() {
        const activity = findActivity(Number(newActivityId));
        if (!activity) {
            return;
        }
        setDraft({...draft, items: [...draft.items, newItem(activity)]});
        setNewActivityId("");
        setSaved(false);
    }

    function removeItem(index: number) {
        setDraft({...draft, items: draft.items.filter((_, i) => i !== index)});
        setSaved(false);
    }

    function moveItem(index: number, direction: number) {
        const target = index + direction;
        if (target < 0 || target >= draft.items.length) {
            return;
        }
        const items = [...draft.items];
        const temp = items[index];
        items[index] = items[target];
        items[target] = temp;
        setDraft({...draft, items: items});
        setSaved(false);
    }

    function changeActivity(index: number, activityId: number) {
        const activity = findActivity(activityId);
        if (!activity) {
            return;
        }
        updateItem(index, {
            ...draft.items[index],
            activityTypeId: activity.id,
            measurements: emptyMeasurements(activity),
        });
    }

    function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        if (!draft.name.trim()) {
            setFormError("Nimi on pakollinen");
            return;
        }
        setFormError(null);
        mutation.mutate(toSessionWrite(draft));
    }

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Nimi
                <input
                    value={draft.name}
                    onChange={(e) => { setDraft({...draft, name: e.target.value}); setSaved(false); }}
                />
            </label>

            <label>
                Aika
                <input
                    type="datetime-local"
                    value={draft.sessionAt}
                    onChange={(e) => { setDraft({...draft, sessionAt: e.target.value}); setSaved(false); }}
                />
            </label>

            <label>
                Tila
                <select
                    value={draft.status}
                    onChange={(e) => { setDraft({...draft, status: e.target.value}); setSaved(false); }}
                >
                    <option value="planned">Suunniteltu</option>
                    <option value="in_progress">Käynnissä</option>
                    <option value="completed">Valmis</option>
                </select>
            </label>

            <label>
                Plan
                <select
                    value={draft.planId}
                    onChange={(e) => { setDraft({...draft, planId: e.target.value}); setSaved(false); }}
                >
                    <option value="">Ei plania</option>
                    {plans.map((plan) => (
                        <option key={plan.id} value={plan.id}>{plan.name}</option>
                    ))}
                </select>
            </label>

            <label>
                Intensiteetti (1-10)
                <input
                    type="number"
                    min={1}
                    max={10}
                    value={draft.intensity}
                    onChange={(e) => { setDraft({...draft, intensity: e.target.value}); setSaved(false); }}
                />
            </label>

            <label>
                Muistiinpanot
                <textarea
                    value={draft.notes}
                    onChange={(e) => { setDraft({...draft, notes: e.target.value}); setSaved(false); }}
                />
            </label>

            <h2>Harjoitukset</h2>

            {draft.items.map((item, index) => {
                const activity = findActivity(item.activityTypeId);
                return (
                    <fieldset key={item.key}>
                        <select
                            value={item.activityTypeId}
                            onChange={(e) => changeActivity(index, Number(e.target.value))}
                        >
                            {activityTypes.map((a) => (
                                <option key={a.id} value={a.id}>{a.name}</option>
                            ))}
                        </select>
                        <button type="button" onClick={() => moveItem(index, -1)} disabled={index === 0}>Ylös</button>
                        <button type="button" onClick={() => moveItem(index, 1)}
                                disabled={index === draft.items.length - 1}>Alas</button>
                        <button type="button" onClick={() => removeItem(index)}>Poista</button>

                        <label>
                            Muistiinpanot
                            <input
                                value={item.notes}
                                onChange={(e) => updateItem(index, {...item, notes: e.target.value})}
                            />
                        </label>

                        {activity && (
                            <MeasurementEditor
                                activity={activity}
                                measurements={item.measurements}
                                onChange={(measurements) => updateItem(index, {...item, measurements: measurements})}
                            />
                        )}
                    </fieldset>
                );
            })}

            <div>
                <select value={newActivityId} onChange={(e) => setNewActivityId(e.target.value)}>
                    <option value="">Valitse harjoitus</option>
                    {activityTypes.map((a) => (
                        <option key={a.id} value={a.id}>{a.name}</option>
                    ))}
                </select>
                <button type="button" onClick={addItem} disabled={newActivityId === ""}>Lisää harjoitus</button>
            </div>

            {formError && <p>{formError}</p>}
            {mutation.isError && <p>{mutation.error.message}</p>}
            {saved && <p>Tallennettu.</p>}

            <button type="submit" disabled={mutation.isPending}>
                {mutation.isPending ? "Tallennetaan..." : "Tallenna"}
            </button>
        </form>
    );
}

function SessionFormPage() {
    const {sessionId} = useParams();
    const id = sessionId ? Number(sessionId) : null;

    const activityTypes = useQuery({queryKey: queryKeys.activityTypes, queryFn: listActivityTypes});
    const plans = useQuery({queryKey: queryKeys.plans, queryFn: listPlans});
    const session = useQuery({
        queryKey: queryKeys.session(id ?? 0),
        queryFn: () => getSession(id ?? 0),
        enabled: id !== null,
    });

    if (activityTypes.isLoading || plans.isLoading || session.isLoading) {
        return <p>Ladataan</p>;
    }

    if (session.isError) {
        if (session.error instanceof ApiError && session.error.status === 404) {
            return <p>Session not found.</p>;
        }
        return <p>{session.error.message}</p>;
    }

    if (activityTypes.isError) {
        return <p>{activityTypes.error.message}</p>;
    }

    const activityList = activityTypes.data ?? [];
    const planList = plans.data ?? [];

    let initialDraft = emptyDraft();
    if (session.data) {
        initialDraft = draftFromSession(session.data, activityList);
    }

    return (
        <div>
            <h1>{id === null ? "Uusi sessio" : "Muokkaa sessiota"}</h1>
            <SessionForm
                key={sessionId ?? "new"}
                sessionId={id}
                initialDraft={initialDraft}
                activityTypes={activityList}
                plans={planList}
            />
        </div>
    );
}

export default SessionFormPage;
