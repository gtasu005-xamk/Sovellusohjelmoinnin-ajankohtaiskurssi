import {CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";

export type ChartPoint = {
    period_label: string;
    value: number;
}

type ProgressChartProps = {
    data: ChartPoint[];
    valueName: string};

function ProgressChart({data, valueName}: ProgressChartProps) {
    return (
    <div style={{width: "100%", height: 300}}>
        <ResponsiveContainer>
            <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="period_label" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Line type="monotone" dataKey="value" name={valueName} stroke="#aa3bff" strokeWidth={2} />
            </LineChart>
        </ResponsiveContainer>
    </div>
    );
}

export default ProgressChart;
