import {Link} from "react-router-dom";
import {useQuery} from "@tanstack/react-query";
import {failureMessage, listActivityTypes, listSessions} from "../api/client.ts";
import {queryKeys} from "../api/queryKeys.ts";
import {exerciseSummary, formatSessionDate} from "../sessions/display.ts";
import {EmptyState, ErrorBanner} from "../components/StatusMessage.tsx";

function DashboardPage() {
    const sessions = useQuery({
        queryKey: queryKeys.sessions({unscheduled: false}),
        queryFn: () => listSessions({unscheduled: false}),
    });
    const activityTypes = useQuery({queryKey: queryKeys.activityTypes, queryFn: listActivityTypes});

    if (sessions.isLoading) {
        return <p>Ladataan</p>;
    }

    if (sessions.isError) {
        return <ErrorBanner message={failureMessage(sessions.error)} />;
    }

    const recent = [...(sessions.data?.items ?? [])];
    recent.sort((a, b) => new Date(b.session_at ?? 0).getTime() - new Date(a.session_at ?? 0).getTime());
    const latest = recent.slice(0, 8);

    return (
    <div>
        <h1>Etusivu</h1>
        <h2>Viimeisimmät sessiot</h2>

        {latest.length === 0 && (
            <EmptyState
                title="Ei vielä päivättyjä sessioita."
                linkTo="/sessions/new"
                linkText="Create your first session"
            />
        )}
        <ul>
            {latest.map((session) => (
                <li key={session.id}>
                    <Link to={`/sessions/${session.id}`}>{session.name}</Link>
                    <div>{formatSessionDate(session.session_at)} - {session.status}</div>
                    <div>{exerciseSummary(session, activityTypes.data ?? [])}</div>
                </li>
            ))}
        </ul>
    </div>
    );
}

export default DashboardPage;
