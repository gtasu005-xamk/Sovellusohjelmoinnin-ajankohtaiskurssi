import {useState, type FormEvent} from "react";
import {Link, useNavigate, useParams} from "react-router-dom";
import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {ApiError, attachSession, deletePlan, detachSession, failureMessage, getPlan, listSessions, updatePlan,
    type PlanDetail,
    type Session,
} from "../api/client.ts";
import {queryKeys} from "../api/queryKeys.ts";
import {formatSessionDate} from "../sessions/display.ts";
import {ErrorBanner} from "../components/StatusMessage.tsx";

function errorMessage(error: Error, notFoundText: string): string {
    if (error instanceof ApiError && error.status === 404) {
        return notFoundText;
    }
    return failureMessage(error);
}

function PlanEditForm({plan}: {plan: PlanDetail}) {
    const queryClient = useQueryClient();
    const [name, setName] = useState(plan.name);
    const [startDate, setStartDate] = useState(plan.start_date ?? "");
    const [lengthWeeks, setLengthWeeks] = useState(plan.length_weeks !== null ? String(plan.length_weeks) : "");
    const [notes, setNotes] = useState(plan.notes ?? "");
    const [formError, setFormError] = useState<string | null>(null);
    const [saved, setSaved] = useState(false);

    const updateMutation = useMutation({
        mutationFn: () => updatePlan(plan.id, {
            name: name.trim(),
            notes: notes.trim() ? notes.trim() : null,
            start_date: startDate ? startDate : null,
            length_weeks: lengthWeeks ? Number(lengthWeeks) : null,
        }),
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ["plans"]});
            setSaved(true);
        },
    });

    function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        if (!name.trim()) {
            setFormError("Nimi on pakollinen");
            return;
        }
        if (lengthWeeks && Number(lengthWeeks) < 1) {
            setFormError("Pituuden pitää olla vähintään 1 viikko");
            return;
        }
        setFormError(null);
        setSaved(false);
        updateMutation.mutate();
    }

    return (
    <form onSubmit={handleSubmit}>
        <label>
            Nimi
            <input value={name} onChange={(e) => setName(e.target.value)} />
        </label>
        <label>
            Aloituspäivä
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </label>
        <label>
            Pituus (viikkoa)
            <input type="number" min={1} value={lengthWeeks} onChange={(e) => setLengthWeeks(e.target.value)} />
        </label>
        <label>
            Muistiinpanot
            <textarea value={notes} onChange={(e) => setNotes(e.target.value)} />
        </label>
        <button type="submit" disabled={updateMutation.isPending}>Tallenna</button>

        {formError && <p>{formError}</p>}
        {updateMutation.isError && <ErrorBanner message={errorMessage(updateMutation.error, "Plan not found.")} />}
        {saved && <p>Tallennettu.</p>}
    </form>
    );
}

function sessionOptionLabel(session: Session): string {
    let label = session.name;
    if (session.session_at === null) {
        label += " (unscheduled)";
    } else {
        label += " " + formatSessionDate(session.session_at);
    }
    if (session.plan_id !== null) {
        label += " (moves from another plan)";
    }
    return label;
}

function PlanDetailPage() {
    const {planId} = useParams();
    const id = Number(planId);
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [selectedSessionId, setSelectedSessionId] = useState("");
    const [confirmDelete, setConfirmDelete] = useState(false);

    const plan = useQuery({queryKey: queryKeys.plan(id), queryFn: () => getPlan(id)});
    const sessions = useQuery({queryKey: queryKeys.sessions({}), queryFn: () => listSessions({})});

    function refreshAll() {
        queryClient.invalidateQueries({queryKey: ["plans"]});
        queryClient.invalidateQueries({queryKey: ["sessions"]});
        queryClient.invalidateQueries({queryKey: ["calendar"]});
    }

    const attachMutation = useMutation({
        mutationFn: (sessionId: number) => attachSession(id, sessionId),
        onSuccess: () => {
            setSelectedSessionId("");
            refreshAll();
        },
    });

    const detachMutation = useMutation({
        mutationFn: (sessionId: number) => detachSession(id, sessionId),
        onSuccess: refreshAll,
    });

    const deleteMutation = useMutation({
        mutationFn: () => deletePlan(id),
        onSuccess: () => {
            navigate("/plans");
            queryClient.removeQueries({queryKey: queryKeys.plan(id)});
            refreshAll();
        },
    });

    if (plan.isLoading) {
        return <p>Ladataan</p>;
    }

    if (plan.isError) {
        if (plan.error instanceof ApiError && plan.error.status === 404) {
            return <p>Plan not found.</p>;
        }
        return <ErrorBanner message={failureMessage(plan.error)} />;
    }

    if (!plan.data) {
        return <p>Plan not found.</p>;
    }

    const dated = plan.data.sessions.filter((s) => s.session_at !== null);
    const unscheduled = plan.data.sessions.filter((s) => s.session_at === null);
    const attachable = (sessions.data ?? []).filter((s) => s.plan_id !== id);
    const busy = attachMutation.isPending || detachMutation.isPending || deleteMutation.isPending;

    function handleAttach(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        if (selectedSessionId === "") {
            return;
        }
        attachMutation.mutate(Number(selectedSessionId));
    }

    function renderRows(list: Session[]) {
        return (
        <ul>
            {list.map((session) => (
            <li key={session.id}>
                <Link to={`/sessions/${session.id}`}>{session.name}</Link>
                {" "}{formatSessionDate(session.session_at)}{" "}
                <button type="button" onClick={() => detachMutation.mutate(session.id)} disabled={busy}>
                    Irrota
                </button>
            </li>
            ))}
        </ul>
        );
    }

    return (
        <div>
            <h1>{plan.data.name}</h1>
            <Link to="/plans">Takaisin planeihin</Link>

            <h2>Tiedot</h2>
            <PlanEditForm key={plan.data.id} plan={plan.data} />

            <h2>Päivätyt sessiot</h2>
            {dated.length === 0 ? <p>Ei päivättyjä sessioita.</p> : renderRows(dated)}

            <h2>Ajastamattomat sessiot</h2>
            {unscheduled.length === 0 ? <p>Ei ajastamattomia sessioita.</p> : renderRows(unscheduled)}

            {detachMutation.isError && <ErrorBanner message={errorMessage(detachMutation.error, "Session not found.")} />}

            <h2>Liitä sessio</h2>
            <form onSubmit={handleAttach}>
                <select value={selectedSessionId} onChange={(e) => setSelectedSessionId(e.target.value)}>
                    <option value="">Valitse sessio</option>
                    {attachable.map((session) => (
                        <option key={session.id} value={session.id}>{sessionOptionLabel(session)}</option>
                    ))}
                </select>
                <button type="submit" disabled={busy || selectedSessionId === ""}>Liitä</button>
            </form>
            {sessions.isError && <ErrorBanner message={failureMessage(sessions.error)} />}
            {attachMutation.isError && <ErrorBanner message={errorMessage(attachMutation.error, "Session not found.")} />}

            <h2>Poista plan</h2>
            <p>Sessiot säilyvät lokissa.</p>
            {!confirmDelete && (
                <button type="button" onClick={() => setConfirmDelete(true)} disabled={busy}>Poista plan</button>
            )}
            {confirmDelete && (
                <div>
                    <p>Haluatko varmasti poistaa planin?</p>
                    <button type="button" onClick={() => deleteMutation.mutate()} disabled={busy}>Kyllä, poista</button>
                    <button type="button" onClick={() => setConfirmDelete(false)} disabled={busy}>Peruuta</button>
                </div>
            )}
            {deleteMutation.isError && <ErrorBanner message={errorMessage(deleteMutation.error, "Plan not found.")} />}
        </div>
    );
}

export default PlanDetailPage;
