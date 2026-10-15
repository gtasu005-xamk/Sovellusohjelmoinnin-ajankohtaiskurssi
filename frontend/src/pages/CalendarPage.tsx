import {useState} from "react";
import {Link} from "react-router-dom";
import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {cloneSession, getCalendar, listPlans, type CalendarEntry, type Session} from "../api/client.ts";
import {queryKeys} from "../api/queryKeys.ts";
import {dateKey, moveCursor, rangeFor, sameDay, visibleDays, type CalendarView} from "../calendar/range.ts";

const weekdays = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"];

function CalendarPage() {
    const queryClient = useQueryClient();
    const [view, setView] = useState<CalendarView>("month");
    const [cursor, setCursor] = useState(new Date());
    const [planId, setPlanId] = useState("");
    const [cloneSource, setCloneSource] = useState<CalendarEntry | null>(null);
    const [cloneName, setCloneName] = useState("");
    const [cloneDate, setCloneDate] = useState("");
    const [cloneError, setCloneError] = useState<string | null>(null);
    const [lastClone, setLastClone] = useState<Session | null>(null);

    const days = visibleDays(view, cursor);
    const range = rangeFor(days);
    const selectedPlan = planId ? Number(planId) : undefined;

    const calendar = useQuery({
        queryKey: queryKeys.calendar(range.from, range.to, selectedPlan),
        queryFn: () => getCalendar(range.from, range.to, selectedPlan),
    });
    const plans = useQuery({queryKey: queryKeys.plans, queryFn: listPlans});

    const cloneMutation = useMutation({
        mutationFn: (sessionAt: Date) => {
            if (cloneSource === null) {
                throw new Error("Valitse kloonattava sessio");
            }
            return cloneSession(cloneSource.id, {
                name: cloneName.trim() ? cloneName.trim() : cloneSource.name,
                session_at: sessionAt.toISOString(),
            });
        },
        onSuccess: (copy) => {
            queryClient.invalidateQueries({queryKey: ["calendar"]});
            queryClient.invalidateQueries({queryKey: ["sessions"]});
            if (copy.session_at) {
                setCursor(new Date(copy.session_at));
            }
            setLastClone(copy);
            setCloneSource(null);
        },
    });

    function openClone(entry: CalendarEntry) {
        setCloneSource(entry);
        setCloneName(entry.name);
        setCloneDate("");
        setCloneError(null);
    }

    function confirmClone() {
        if (cloneSource === null) {
            return;
        }
        if (!cloneDate) {
            setCloneError("Choose a date.");
            return;
        }
        setCloneError(null);
        const original = new Date(cloneSource.session_at);
        const parts = cloneDate.split("-");
        const sessionAt = new Date(
            Number(parts[0]),
            Number(parts[1]) - 1,
            Number(parts[2]),
            original.getHours(),
            original.getMinutes(),
        );
        cloneMutation.mutate(sessionAt);
    }

    const sessionsByDay: Record<string, CalendarEntry[]> = {};
    for (const entry of calendar.data ?? []) {
        const key = dateKey(new Date(entry.session_at));
        if (!sessionsByDay[key]) {
            sessionsByDay[key] = [];
        }
        sessionsByDay[key].push(entry);
    }

    const today = new Date();
    let title = cursor.toLocaleDateString("fi-FI", {month: "long", year: "numeric"});
    if (view === "week") {
        title = days[0].toLocaleDateString("fi-FI") + " – " + days[6].toLocaleDateString("fi-FI");
    }

    return (
    <div>
        <h1>Kalenteri</h1>

        <div className="calendar-toolbar">
            <button type="button" onClick={() => setCursor(moveCursor(view, cursor, -1))}>Edellinen</button>
            <button type="button" onClick={() => setCursor(new Date())}>Tänään</button>
            <button type="button" onClick={() => setCursor(moveCursor(view, cursor, 1))}>Seuraava</button>
            <button type="button" onClick={() => setView("month")} disabled={view === "month"}>Kuukausi</button>
            <button type="button" onClick={() => setView("week")} disabled={view === "week"}>Viikko</button>
            <select value={planId} onChange={(e) => setPlanId(e.target.value)}>
                <option value="">All plans</option>
                {plans.data?.map((plan) => (
                    <option key={plan.id} value={plan.id}>{plan.name}</option>
                ))}
            </select>
        </div>

        <h2>{title}</h2>

        {lastClone && (
            <p>
                Sessio kloonattu: <Link to={`/sessions/${lastClone.id}`}>{lastClone.name}</Link>
            </p>
        )}

        {calendar.isLoading && <p>Ladataan</p>}
        {calendar.isError && <p>{calendar.error.message}</p>}
        {calendar.data && calendar.data.length === 0 && (
            <p>
                {planId
                    ? "Valitulla planilla ei ole sessioita tällä aikavälillä."
                    : "Tällä aikavälillä ei ole sessioita."}
            </p>
        )}

        <div className="calendar-grid">
            {weekdays.map((weekday) => (
                <div key={weekday} className="calendar-weekday">{weekday}</div>
            ))}

            {days.map((day) => {
                let className = "calendar-day";
                if (view === "month" && day.getMonth() !== cursor.getMonth()) {
                    className += " outside";
                }
                if (sameDay(day, today)) {
                    className += " today";
                }

            return (
                <div key={dateKey(day)} className={className}>
                    <div>{day.getDate()}</div>
                    {(sessionsByDay[dateKey(day)] ?? []).map((entry) => (
                        <div key={entry.id} className={"calendar-chip status-" + entry.status}>
                            <Link to={`/sessions/${entry.id}`}>{entry.name}</Link>
                            <button type="button" onClick={() => openClone(entry)}>Kloonaa</button>

                            {cloneSource?.id === entry.id && (
                            <div className="calendar-clone">
                                <label>
                                    Nimi
                                    <input value={cloneName} onChange={(e) => setCloneName(e.target.value)} />
                                </label>
                                <label>
                                    Päivä
                                    <input type="date" value={cloneDate} onChange={(e) => setCloneDate(e.target.value)} />
                                </label>
                                <button type="button" onClick={confirmClone} disabled={cloneMutation.isPending}>
                                    Vahvista
                                </button>
                                <button type="button" onClick={() => setCloneSource(null)}>Peruuta</button>
                                {cloneError && <p>{cloneError}</p>}
                                {cloneMutation.isError && <p>{cloneMutation.error.message}</p>}
                            </div>
                            )}
                        </div>
                    ))}
                </div>
                );
            })}
        </div>
    </div>
    );
}

export default CalendarPage;
