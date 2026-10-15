import {useState, type FormEvent} from "react";
import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {createGoal, failureMessage, listActivityTypes, listGoals, setGoalActive, type ActivityType} from "../api/client.ts";
import {queryKeys} from "../api/queryKeys.ts";
import ActivityTypeSelect from "../components/ActivityTypeSelect.tsx";
import {EmptyState, ErrorBanner} from "../components/StatusMessage.tsx";

type Unit = {
    id: number;
    name: string;}

function uniqueUnits(activityTypes: ActivityType[]): Unit[] {
    const units: Unit[] = [];
    for (const activity of activityTypes) {
        for (const link of activity.unit_links) {
            const exists = units.find((u) => u.id === link.unit_type.id);
            if (!exists) {
                units.push({id: link.unit_type.id, name: link.unit_type.name});
            }
        }
    }
    return units;
}

function GoalsPage() {
    const queryClient = useQueryClient();
    const [show, setShow] = useState("all");
    const [unitId, setUnitId] = useState("");
    const [period, setPeriod] = useState("week");
    const [target, setTarget] = useState("");
    const [activityId, setActivityId] = useState<number | null>(null);
    const [formError, setFormError] = useState<string | null>(null);

    let activeFilter: boolean | undefined = undefined;
    if (show === "active") {
        activeFilter = true;
    } else if (show === "inactive") {
        activeFilter = false;
    }

    const activityTypes = useQuery({queryKey: queryKeys.activityTypes, queryFn: listActivityTypes});
    const goals = useQuery({
        queryKey: queryKeys.goals(activeFilter),
        queryFn: () => listGoals(activeFilter),
    });

    const createMutation = useMutation({
        mutationFn: createGoal,
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ["goals"]});
            setTarget("");
        },
    });

    const toggleMutation = useMutation({
        mutationFn: (goal: {id: number; active: boolean}) => setGoalActive(goal.id, goal.active),
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ["goals"]});
        },
    });

    const activityList = activityTypes.data ?? [];
    const units = uniqueUnits(activityList);

    function unitName(id: number): string {
        const unit = units.find((u) => u.id === id);
        if (!unit) {
            return "Tuntematon yksikkö";
        }
        return unit.name;
    }

    function activityName(id: number | null): string {
        if (id === null) {
            return "kaikki harjoitukset";
        }
        const activity = activityList.find((a) => a.id === id);
        if (!activity) {
            return "Unknown exercise";
        }
        return activity.name;
    }

    function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        if (!unitId) {
            setFormError("Valitse yksikkö");
            return;
        }
        if (!target || Number(target) <= 0) {
            setFormError("Tavoitteen pitää olla suurempi kuin 0");
            return;
        }
        setFormError(null);
        createMutation.mutate({
            unit_type_id: Number(unitId),
            activity_type_id: activityId,
            target_value: Number(target),
            period: period,
        });
    }

    let content;
    if (goals.isLoading) {
        content = <p>Ladataan</p>;
    } else if (goals.isError) {
        content = <ErrorBanner message={failureMessage(goals.error)} />;
    } else if (!goals.data || goals.data.length === 0) {
        content = <EmptyState title="Ei tavoitteita." text="Luo ensimmäinen tavoite yllä olevalla lomakkeella." />;
    } else {
        content = (
        <ul>
            {goals.data.map((goal) => (
                <li key={goal.id}>
                    {goal.target_value} {unitName(goal.unit_type_id)} / {goal.period === "week" ? "viikko" : "kuukausi"}
                    {" "}({activityName(goal.activity_type_id)})
                    {" "}<strong>{goal.active ? "Active" : "Inactive"}</strong>
                    {" "}
                    <button
                        type="button"
                        onClick={() => toggleMutation.mutate({id: goal.id, active: !goal.active})}
                        disabled={toggleMutation.isPending}
                    >
                        {goal.active ? "Deaktivoi" : "Aktivoi"}
                    </button>
                </li>
            ))}
        </ul>
        );
    }

    return (
        <div>
        <h1>Tavoitteet</h1>

        <h2>Uusi tavoite</h2>
        <form onSubmit={handleSubmit}>
            <label>
                Yksikkö
                <select value={unitId} onChange={(e) => setUnitId(e.target.value)}>
                    <option value="">Valitse yksikkö</option>
                    {units.map((unit) => (
                        <option key={unit.id} value={unit.id}>{unit.name}</option>
                    ))}
                </select>
            </label>
            <label>
                Jakso
                <select value={period} onChange={(e) => setPeriod(e.target.value)}>
                    <option value="week">Viikko</option>
                    <option value="month">Kuukausi</option>
                </select>
            </label>
            <label>
                Tavoite
                <input type="number" min={0} step="any" value={target} onChange={(e) => setTarget(e.target.value)} />
            </label>
            <label>
                Harjoitus
                <ActivityTypeSelect
                    activities={activityList}
                    value={activityId}
                    onChange={setActivityId}
                    allowEmpty
                    emptyLabel="Any exercise"
                />
            </label>
            <button type="submit" disabled={createMutation.isPending}>Luo tavoite</button>
        </form>

        {formError && <p>{formError}</p>}
        {createMutation.isError && <ErrorBanner message={failureMessage(createMutation.error)} />}
        {toggleMutation.isError && <ErrorBanner message={failureMessage(toggleMutation.error)} />}

        <h2>Tavoitteet</h2>
        <label>
            Näytä
            <select value={show} onChange={(e) => setShow(e.target.value)}>
                <option value="all">Kaikki</option>
                <option value="active">Aktiiviset</option>
                <option value="inactive">Ei-aktiiviset</option>
            </select>
        </label>

        {content}
    </div>
    );
}

export default GoalsPage;
