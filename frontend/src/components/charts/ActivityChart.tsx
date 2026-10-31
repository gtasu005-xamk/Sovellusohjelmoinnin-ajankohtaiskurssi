import {Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";

export type ActivityBar = {
    name: string;
    distance_km: number;
    duration_min: number;
}

function ActivityChart({data}: {data: ActivityBar[]}) {
    return (
    <div style={{width: "100%", height: 300}}>
        <ResponsiveContainer>
            <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="distance_km" name="Matka (km)" fill="#aa3bff" />
                <Bar dataKey="duration_min" name="Kesto (min)" fill="#3b82f6" />
            </BarChart>
        </ResponsiveContainer>
    </div>
    );
}

export default ActivityChart;
