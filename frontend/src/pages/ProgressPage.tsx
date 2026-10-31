import {useState} from "react";
import {useQuery} from "@tanstack/react-query";
import {failureMessage, getProgress, getStatsSummary, listActivityTypes} from "../api/client.ts";
import {queryKeys, type ProgressFilters} from "../api/queryKeys.ts";
import {addDays, dateKey, startOfWeek} from "../calendar/range.ts";
import ProgressChart from "../components/charts/ProgressChart.tsx";
import ActivityChart from "../components/charts/ActivityChart.tsx";
import {EmptyState, ErrorBanner} from "../components/StatusMessage.tsx";

function ProgressPage() {
    const today = new Date();
    const [fromDate, setFromDate] = useState(dateKey(startOfWeek(addDays(today, -7 * 7))));
    const [toDate, setToDate] = useState(dateKey(today));
    const [granularity, setGranularity] = useState("week");

    const validRange = fromDate !== "" && toDate !== "" && fromDate <= toDate;

    const filters: ProgressFilters = {
        from: validRange ? new Date(`${fromDate}T00:00:00`).toISOString() : "",
        to: validRange ? new Date(`${toDate}T23:59:59.999`).toISOString() : "",
        metric: "sessions",
        granularity: granularity,
    };

    const progress = useQuery({
        queryKey: queryKeys.progress(filters),
        queryFn: () => getProgress(filters),
        enabled: validRange,
    });
    const summary = useQuery({
        queryKey: queryKeys.statsSummary(filters.from, filters.to),
        queryFn: () => getStatsSummary(filters.from, filters.to),
        enabled: validRange,
    });
    const activityTypes = useQuery({queryKey: queryKeys.activityTypes, queryFn: listActivityTypes});

    function activityName(slug: string): string {
        const activity = (activityTypes.data ?? []).find((a) => a.slug === slug);
        if (!activity) {
            return slug;
        }
        return activity.name;
    }

    let sessionsContent;
    if (!validRange) {
        sessionsContent = null;
    } else if (progress.isLoading) {
        sessionsContent = <p>Ladataan</p>;
    } else if (progress.isError) {
        sessionsContent = <ErrorBanner message={failureMessage(progress.error)} />;
    } else if (!progress.data || progress.data.length === 0) {
        sessionsContent = <EmptyState title="Ei sessioita tällä aikavälillä." linkTo="/sessions/new" linkText="Lisää sessio" />;
    } else {
        sessionsContent = <ProgressChart data={progress.data} valueName="Sessiot" />;
    }

    let activityContent;
    if (!validRange) {
        activityContent = null;
    } else if (summary.isLoading) {
        activityContent = <p>Ladataan</p>;
    } else if (summary.isError) {
        activityContent = <ErrorBanner message={failureMessage(summary.error)} />;
    } else {
        const bars = (summary.data?.by_activity ?? [])
            .filter((row) => row.distance_km > 0 || row.duration_min > 0)
            .map((row) => ({
                name: activityName(row.activity_slug),
                distance_km: row.distance_km,
                duration_min: row.duration_min,
            }));
        if (bars.length === 0) {
            activityContent = <EmptyState title="Ei mittauksia tällä aikavälillä." text="Kirjaa sessioihin matka tai kesto." />;
        } else {
            activityContent = <ActivityChart data={bars} />;
        }
    }

    return (
        <div>
            <h1>Edistyminen</h1>
            <div>
            <label>Alkaen <input type="date" value={fromDate} onChange={(e) => setFromDate(e.target.value)} /></label>
            <label>Asti <input type="date" value={toDate} onChange={(e) => setToDate(e.target.value)} /></label>
            <label>Jakso
                <select value={granularity} onChange={(e) => setGranularity(e.target.value)}>
                    <option value="week">Viikko</option>
                    <option value="month">Kuukausi</option>
                </select>
            </label>
            </div>
            {!validRange && <ErrorBanner message="Alkupäivän pitää olla ennen loppupäivää." />}

            <h2>{granularity === "week" ? "Sessiot viikoittain" : "Sessiot kuukausittain"}</h2>
            {sessionsContent}

            <h2>Matka ja kesto harjoituksittain</h2>
            {activityContent}
        </div>
    );
}

export default ProgressPage;
