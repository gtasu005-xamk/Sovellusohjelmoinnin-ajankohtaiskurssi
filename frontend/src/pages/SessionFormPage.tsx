import {useState, type FormEvent} from "react";
import {useNavigate, useParams, useLocation} from "react-router-dom";
import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {ApiError,createSession, getSession, listActivityTypes, listPlans, updateSession, cloneSession, deleteSession,
        type ActivityType, type Plan, type SessionWrite, type Session} from "../api/client.ts";
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

function errorMessage(error: Error): string {
    if (error instanceof ApiError && error.status === 404) {
        return "Session not found.";
    }
    if (error instanceof ApiError && error.status === 403) {
        return "Et voi muuttaa tätä sessiota.";
    }
    return error.message;
}


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
            {mutation.isError && <p>{errorMessage(mutation.error)}</p>}
            {saved && <p>Tallennettu.</p>}

            <button type="submit" disabled={mutation.isPending}>
                {mutation.isPending ? "Tallennetaan..." : "Tallenna"}
            </button>
        </form>
    );
}

function SessionActions({session}: {session: Session}) {
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [cloneName, setCloneName] = useState(session.name);
    const [cloneDate, setCloneDate] = useState("");
    const [confirmDelete, setConfirmDelete] = useState(false);

    const cloneMutation = useMutation({
        mutationFn: () => cloneSession(session.id, {
            name: cloneName.trim() ? cloneName.trim() : session.name,
            session_at: cloneDate ? new Date(cloneDate).toISOString() : null,
        }),
        onSuccess: (copy) => {
            queryClient.invalidateQueries({queryKey: ["sessions"]});
            queryClient.invalidateQueries({queryKey: ["calendar"]});
            navigate(`/sessions/${copy.id}`, {state: {cloned: true}});
        },
    });

    const deleteMutation = useMutation({
        mutationFn: () => deleteSession(session.id),
        onSuccess: () => {
            navigate("/sessions");
            queryClient.removeQueries({queryKey: queryKeys.session(session.id)});
            queryClient.invalidateQueries({queryKey: ["sessions"]});
            queryClient.invalidateQueries({queryKey: ["calendar"]});
        },
    });

    const busy = cloneMutation.isPending || deleteMutation.isPending;

    return (
    <div>
        <h2>Kloonaa</h2>
        <p>Kopio säilyttää planned-arvot, tyhjentää actual-arvot eikä kuulu mihinkään planiin.</p>
        <label>
            Kopion nimi
            <input value={cloneName} onChange={(e) => setCloneName(e.target.value)} />
        </label>
        <label>
            Kopion aika (tyhjä = ajastamaton)
            <input type="datetime-local" value={cloneDate} onChange={(e) => setCloneDate(e.target.value)} />
        </label>
        <button type="button" onClick={() => cloneMutation.mutate()} disabled={busy}>
            {cloneMutation.isPending ? "Kloonataan..." : "Kloonaa"}
        </button>
        {cloneMutation.isError && <p>{errorMessage(cloneMutation.error)}</p>}

        <h2>Poista</h2>
        {!confirmDelete && (
            <button type="button" onClick={() => setConfirmDelete(true)} disabled={busy}>Poista sessio</button>)}
        {confirmDelete && (
            <div>
                <p>Haluatko varmasti poistaa session?</p>
                <button type="button" onClick={() => deleteMutation.mutate()} disabled={busy}>
                    {deleteMutation.isPending ? "Poistetaan..." : "Kyllä, poista"}
                </button>
                <button type="button" onClick={() => setConfirmDelete(false)} disabled={busy}>Peruuta</button>
            </div>
        )}
        {deleteMutation.isError && <p>{errorMessage(deleteMutation.error)}</p>}
    </div>
    );
}


function SessionFormPage() {
    const {sessionId} = useParams();
    const location = useLocation();
    const id = sessionId ? Number(sessionId) : null;
    const cloned = location.state?.cloned === true;

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
            {cloned && <p>Sessio kloonattu: planned-arvot säilyivät, actual-arvot tyhjennettiin, plania ei kopioitu.</p>}
            <SessionForm
                key={sessionId ?? "new"}
                sessionId={id}
                initialDraft={initialDraft}
                activityTypes={activityList}
                plans={planList}
            />
            {session.data && <SessionActions key={session.data.id} session={session.data} />}
        </div>
    );
}

export default SessionFormPage;
