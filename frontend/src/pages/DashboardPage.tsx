import {Link} from "react-router-dom";
import {useQuery} from "@tanstack/react-query";
import {listActivityTypes, listSessions} from "../api/client.ts";
import {queryKeys} from "../api/queryKeys.ts";
import {exerciseSummary, formatSessionDate} from "../sessions/display.ts";

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
        return <p>Sessioiden haku epäonnistui: {sessions.error.message}</p> }

    const recent = [...(sessions.data ?? [])];
    recent.sort((a, b) => new Date(b.session_at ?? 0).getTime() - new Date(a.session_at ?? 0).getTime());
    const latest = recent.slice(0, 8);

    return (
    <div>
        <h1>Etusivu</h1>
        <h2>Viimeisimmät sessiot</h2>

        {latest.length === 0 && (
            <p>
                Ei vielä päivättyjä sessioita. <Link to="/sessions/new">Create your first session</Link>
            </p>
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
