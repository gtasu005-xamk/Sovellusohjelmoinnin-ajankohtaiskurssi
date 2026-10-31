import type {StatsSummary} from "../api/client.ts";

function formatDuration(minutes: number): string {
    const rounded = Math.round(minutes);
    const hours = Math.floor(rounded / 60);
    const rest = rounded % 60;
    if (hours === 0) {
        return `${rest} min`;
    }
    return `${hours}h ${rest}m`;
}

function StatWidgets({summary}: {summary: StatsSummary}) {
    return (
        <div className="stat-widgets">
            <div className="stat-widget">
                <strong>{summary.session_count}</strong>
                Sessiot
            </div>
            <div className="stat-widget">
                <strong>{formatDuration(summary.total_duration_min)}</strong>
                Kesto yhteensä
            </div>
            <div className="stat-widget">
                <strong>{summary.total_distance_km.toFixed(1)} km</strong>
                Matka yhteensä
            </div>
            <div className="stat-widget">
                <strong>{summary.avg_intensity === null ? "-" : summary.avg_intensity.toFixed(1)}</strong>
                Keskim. intensiteetti
            </div>
        </div>
    );
}

export default StatWidgets;
