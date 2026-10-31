import ProgressChart, {type ChartPoint} from "../components/charts/ProgressChart.tsx";

const sampleData: ChartPoint[] = [
    {period_label: "2026-W38", value: 2},
    {period_label: "2026-W39", value: 3},
    {period_label: "2026-W40", value: 1},
    {period_label: "2026-W41", value: 4},
    {period_label: "2026-W42", value: 3},
    {period_label: "2026-W43", value: 5},
];

function ProgressPage() {
    return (
        <div>
            <h1>Edistyminen</h1>
            <h2>Sessiot viikoittain</h2>
            <p>Mockdata.</p>
            <ProgressChart data={sampleData} valueName="Sessiot" />
        </div>
    );
}

export default ProgressPage;
