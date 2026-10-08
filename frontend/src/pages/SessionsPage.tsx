import {useState, type FormEvent} from "react";
import {Link} from "react-router-dom";
import {useQuery} from "@tanstack/react-query";
import {listActivityTypes, listPlans, listSessions} from "../api/client.ts";
import {queryKeys, type SessionFilters} from "../api/queryKeys.ts";
import {exerciseSummary, formatSessionDate} from "../sessions/display.ts";

type Draft = {
    from: string;
    to: string;
    status: string;
    schedule: string;
    planId: string;
    activityTypeId: string;
}


const emptyDraft: Draft = {
    from: "",
    to: "",
    status: "",
    schedule: "all",
    planId: "",
    activityTypeId: ""
}


function toFilters(draft: Draft): SessionFilters {
    const filters: SessionFilters = {};
    if (draft.schedule==="unscheduled") {
        filters.unscheduled = true;
    } else {
        if (draft.schedule === "dated") {
            filters.unscheduled = false;
        }
        if (draft.from) {
            filters.from = draft.from;
        }
        if (draft.to) {
            filters.to = draft.to;
        }
    }
    if (draft.status) {
        filters.status = draft.status}
    if (draft.planId) {
        filters.planId = Number(draft.planId)}
    if (draft.activityTypeId) {
        filters.activityTypeId = Number(draft.activityTypeId)}
    return filters;
}

function SessionsPage() {
    const [draft, setDraft] = useState<Draft>(emptyDraft);
    const [applied, setApplied] = useState<SessionFilters>({});
    const [formError, setFormError] = useState<string | null>(null);

    const sessions = useQuery({
        queryKey: queryKeys.sessions(applied),
        queryFn: () => listSessions(applied),
    });

    const plans = useQuery({queryKey: queryKeys.plans, queryFn: listPlans});
    const activityTypes = useQuery({queryKey: queryKeys.activityTypes, queryFn: listActivityTypes});

    function handleApply(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        if (draft.schedule !== "unscheduled" && draft.from && draft.to && draft.from > draft.to) {
            setFormError("Alkupäivä ei voi olla loppupäivän jälkeen");
            return;
        }
        setFormError(null);
        setApplied(toFilters(draft));
    }

    function handleClear() {
        setDraft(emptyDraft);
        setApplied({});
        setFormError(null)}

    const unscheduled = draft.schedule === "unscheduled";
    const hasFilters = Object.keys(applied).length > 0;

    return (
        <div>
            <h1>Sessiot</h1>

            <form onSubmit={handleApply}>
                <label>Alkaen <input type="date" value={draft.from} disabled={unscheduled}
                    onChange={(e) => setDraft({...draft, from: e.target.value})} />
                </label>

                <label>Asti<input type="date" value={draft.to} disabled={unscheduled}
                    onChange={(e) => setDraft({...draft, to: e.target.value})} />
                </label>

                <label>
                    Tila <select value={draft.status} onChange={(e) => setDraft({...draft, status: e.target.value})}>
                        <option value="">Kaikki</option> 
                        <option value="planned">planned</option>
                        <option value="in_progress">in_progress</option>
                        <option value="completed">completed</option>
                        </select>
                </label>

                <label> 
                    Ajoitus <select value={draft.schedule} onChange={(e) => setDraft({...draft, schedule: e.target.value})}>
                        <option value="all">Kaikki</option>
                        <option value="dated">Päivätyt</option>
                        <option value="unscheduled">Unscheduled</option>
                        </select>
                </label>

                <label>
                    Plan
                    <select value={draft.planId} onChange={(e) => setDraft({...draft, planId: e.target.value})}>
                        <option value="">Kaikki</option>
                        {plans.data?.map((plan) => (
                            <option key={plan.id} value={plan.id}>{plan.name}</option>
                        ))}
                    </select>
                </label>


                <label>
                    Aktiviteetti <select value={draft.activityTypeId}
                        onChange={(e) => setDraft({...draft, activityTypeId: e.target.value})}>
                            <option value="">Kaikki</option>
                            {activityTypes.data?.map((activity) => (
                            <option key={activity.id} value={activity.id}>{activity.name}</option>
                    ))}
                    </select>
                    </label>
                <button type="submit">Käytä</button>
                <button type="button" onClick={handleClear}>Tyhjennä</button>
            </form>

            {formError && <p role="alert">{formError}</p>}

            {sessions.isLoading && <p>Ladataan</p>}
            {sessions.isError && <p role="alert">{sessions.error.message}</p>}

            {sessions.data && sessions.data.length === 0 && (
                hasFilters
                    ? <p>Mikään sessio ei vastaa suodattimia.</p>
                    : <p>Ei vielä sessioita. Luo ensimmäinen sessiosi.</p>
            )}

            {sessions.data && sessions.data.length > 0 && (
                <table>
                    <thead>
                        <tr>
                            <th>Nimi</th>
                            <th>Aika</th>
                            <th>Tila</th>
                            <th>Harjoitukset</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sessions.data.map((session) => (
                            <tr key={session.id}>
                                <td><Link to={`/sessions/${session.id}`}>{session.name}</Link></td>
                                <td>{formatSessionDate(session.session_at)}</td>
                                <td>{session.status}</td>
                                <td>{exerciseSummary(session, activityTypes.data ?? [])}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default SessionsPage;
