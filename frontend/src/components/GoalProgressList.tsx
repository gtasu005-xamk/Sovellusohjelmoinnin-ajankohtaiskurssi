import type {GoalProgress} from "../api/client.ts";

function GoalProgressList({goals}: {goals: GoalProgress[]}) {
    return (
    <ul>
    {goals.map((goal) => (
        <li key={goal.goal_id}>
            <div>
                {goal.unit_name} ({goal.activity_name ?? "kaikki harjoitukset"}) / {goal.period === "week" ? "tämä viikko" : "tämä kuukausi"}
            </div>
            <progress value={Math.min(goal.percent, 100)} max={100} />
            {" "}{goal.total} / {goal.target_value} ({goal.percent} %)
        </li>
    ))}
</ul>
    );
}

export default GoalProgressList;
