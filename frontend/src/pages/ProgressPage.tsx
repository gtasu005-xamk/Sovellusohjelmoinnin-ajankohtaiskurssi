import {useState} from "react";
import {useQuery} from "@tanstack/react-query";
import {failureMessage, getProgress, getStatsSummary, listActivityTypes} from "../api/client.ts";
import {queryKeys, type ProgressFilters} from "../api/queryKeys.ts";
import ProgressChart from "../components/charts/ProgressChart.tsx";
import ActivityChart from "../components/charts/ActivityChart.tsx";
import {EmptyState, ErrorBanner} from "../components/StatusMessage.tsx";

function defaultFilters(): ProgressFilters {
    const to = new Date();
    const from = new Date();
    from.setDate(from.getDate() - 12 * 7);
    return {
        from: from.toISOString(),
        to: to.toISOString(),
        metric: "sessions",
        granularity: "week",
    };
}

function ProgressPage() {
    const [filters] = useState<ProgressFilters>(defaultFilters);

    const progress = useQuery({
        queryKey: queryKeys.progress(filters),
        queryFn: () => getProgress(filters),
    });
    const summary = useQuery({
        queryKey: queryKeys.statsSummary(filters.from, filters.to),
        queryFn: () => getStatsSummary(filters.from, filters.to),
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
    if (progress.isLoading) {
        sessionsContent = <p>Ladataan</p>;
    } else if (progress.isError) {
        sessionsContent = <ErrorBanner message={failureMessage(progress.error)} />;
    } else if (!progress.data || progress.data.length === 0) {
        sessionsContent = <EmptyState title="Ei sessioita tällä aikavälillä." linkTo="/sessions/new" linkText="Lisää sessio" />;
    } else {
        sessionsContent = <ProgressChart data={progress.data} valueName="Sessiot" />;
    }

    let activityContent;
    if (summary.isLoading) {
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
            <p>Viimeiset 12 viikkoa</p>

            <h2>Sessiot viikoittain</h2>
            {sessionsContent}

            <h2>Matka ja kesto harjoituksittain</h2>
            {activityContent}
        </div>
    );
}

export default ProgressPage;
