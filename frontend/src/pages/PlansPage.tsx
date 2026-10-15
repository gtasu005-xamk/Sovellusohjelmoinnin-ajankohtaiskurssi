import {useState, type FormEvent} from "react";
import {Link, useNavigate} from "react-router-dom";
import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {createPlan, failureMessage, listPlans} from "../api/client.ts";
import {queryKeys} from "../api/queryKeys.ts";
import {EmptyState, ErrorBanner} from "../components/StatusMessage.tsx";

function PlansPage() {
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [name, setName] = useState("");
    const [startDate, setStartDate] = useState("");
    const [lengthWeeks, setLengthWeeks] = useState("");
    const [notes, setNotes] = useState("");
    const [formError, setFormError] = useState<string | null>(null);

    const plans = useQuery({queryKey: queryKeys.plans, queryFn: listPlans});

    const createMutation = useMutation({
        mutationFn: createPlan,
        onSuccess: (plan) => {
            queryClient.invalidateQueries({queryKey: queryKeys.plans});
            navigate(`/plans/${plan.id}`);
        },
    });

    function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        if (!name.trim()) {
            setFormError("Nimi on pakollinen");
            return;
        }
        if (lengthWeeks && Number(lengthWeeks) < 1) {
            setFormError("Pituuden pitää olla vähintään 1 viikko");
            return;
        }
        setFormError(null);
        createMutation.mutate({
            name: name.trim(),
            notes: notes.trim() ? notes.trim() : null,
            start_date: startDate ? startDate : null,
            length_weeks: lengthWeeks ? Number(lengthWeeks) : null,
        });
    }

    let content;
    if (plans.isLoading) {
        content = <p>Ladataan</p>;
    } else if (plans.isError) {
        content = <ErrorBanner message={failureMessage(plans.error)} />;
    } else if (!plans.data || plans.data.length === 0) {
        content = <EmptyState title="Ei vielä planeja." text="Luo ensimmäinen plan alla olevalla lomakkeella." />;
    } else {
        content = (
            <ul>
                {plans.data.map((plan) => (
                    <li key={plan.id}>
                        <Link to={`/plans/${plan.id}`}>{plan.name}</Link>
                        {plan.start_date !== null && <span> alkaa {plan.start_date}</span>}
                        {plan.length_weeks !== null && <span>, {plan.length_weeks} viikkoa</span>}
                    </li>
                ))}
            </ul>
        );
    }

    return (
        <div>
            <h1>Planit</h1>

            {content}

            <h2>Uusi plan</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Nimi
                    <input value={name} onChange={(e) => setName(e.target.value)} />
                </label>
                <label>
                    Aloituspäivä
                    <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
                </label>
                <label>
                    Pituus (viikkoa)
                    <input type="number" min={1} value={lengthWeeks} onChange={(e) => setLengthWeeks(e.target.value)} />
                </label>
                <label>
                    Muistiinpanot
                    <textarea value={notes} onChange={(e) => setNotes(e.target.value)} />
                </label>
                <button type="submit" disabled={createMutation.isPending}>Luo plan</button>
            </form>

            {formError && <p>{formError}</p>}
            {createMutation.isError && <ErrorBanner message={failureMessage(createMutation.error)} />}
        </div>
    );
}

export default PlansPage;
