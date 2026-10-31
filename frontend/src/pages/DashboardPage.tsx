import {useState} from "react";
import {Link} from "react-router-dom";
import {useQuery} from "@tanstack/react-query";
import {failureMessage, getStatsSummary, listActivityTypes, listSessions} from "../api/client.ts";
import {queryKeys} from "../api/queryKeys.ts";
import {exerciseSummary, formatSessionDate} from "../sessions/display.ts";
import {addDays, startOfWeek} from "../calendar/range.ts";
import {EmptyState, ErrorBanner} from "../components/StatusMessage.tsx";
import StatWidgets from "../components/StatWidgets.tsx";

function periodRange(period: string): {from: string; to: string} {
    const today = new Date();
    let start: Date;
    if (period === "month") {
        start = new Date(today.getFullYear(), today.getMonth(), 1);
    } else if (period === "30days") {
        start = addDays(today, -29);
    } else {
        start = startOfWeek(today);
    }
    const end = addDays(today, 1);
    end.setMilliseconds(-1);
    return {from: start.toISOString(), to: end.toISOString()};
}

function DashboardPage() {
    const [period, setPeriod] = useState("week");
    const range = periodRange(period);

    const summary = useQuery({
        queryKey: queryKeys.statsSummary(range.from, range.to),
        queryFn: () => getStatsSummary(range.from, range.to),
    });
    const sessions = useQuery({
        queryKey: queryKeys.sessions({unscheduled: false}),
        queryFn: () => listSessions({unscheduled: false}),
    });
    const activityTypes = useQuery({queryKey: queryKeys.activityTypes, queryFn: listActivityTypes});

    let widgets;
    if (summary.isLoading) {
        widgets = <p>Ladataan tilastoja</p>;
    } else if (summary.isError) {
        widgets = <ErrorBanner message={failureMessage(summary.error)} />;
    } else if (summary.data) {
        widgets = <StatWidgets summary={summary.data} />;
    }

    let recentContent;
    if (sessions.isLoading) {
        recentContent = <p>Ladataan</p>;
    } else if (sessions.isError) {
        recentContent = <ErrorBanner message={failureMessage(sessions.error)} />;
    } else {
        const recent = [...(sessions.data?.items ?? [])];
        recent.sort((a, b) => new Date(b.session_at ?? 0).getTime() - new Date(a.session_at ?? 0).getTime());
        const latest = recent.slice(0, 8);

        if (latest.length === 0) {
            recentContent = (
                <EmptyState
                    title="Ei vielä päivättyjä sessioita."
                    linkTo="/sessions/new"
                    linkText="Create your first session"
                />
            );
        } else {
            recentContent = (
                <ul>
                    {latest.map((session) => (
                        <li key={session.id}>
                            <Link to={`/sessions/${session.id}`}>{session.name}</Link>
                            <div>{formatSessionDate(session.session_at)} - {session.status}</div>
                            <div>{exerciseSummary(session, activityTypes.data ?? [])}</div>
                        </li>
                    ))}
                </ul>
            );
        }
    }

    return (
    <div>
        <h1>Etusivu</h1>

        <h2>Tilastot</h2>
        <label>
            Jakso
            <select value={period} onChange={(e) => setPeriod(e.target.value)}>
                <option value="week">Tämä viikko</option>
                <option value="month">Tämä kuukausi</option>
                <option value="30days">Viimeiset 30 päivää</option>
            </select>
        </label>
        {widgets}

        <h2>Viimeisimmät sessiot</h2>
        {recentContent}
    </div>
    );
}

export default DashboardPage;
