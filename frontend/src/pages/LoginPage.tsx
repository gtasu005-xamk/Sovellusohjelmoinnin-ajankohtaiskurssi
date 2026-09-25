import {useState, type FormEvent} from "react";
import {useNavigate} from "react-router-dom";
import {apiPost} from "../api/client.ts";
import {setToken} from "../auth/token.ts";

type FieldName = "email" | "password";
type FieldErrors = Partial<Record<FieldName, string>>;

// Onnistuneen kirjautumisen jälkeen JWT tallennetaan localStorageen (vain token, ei salasanaa)
// ja käyttäjä ohjataan etusivulle. Suojattu reitti toteutetaan S2-16:ssa.
function LoginPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
    const [formError, setFormError] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setFormError(null);

        const errors: FieldErrors = {};
        if (!email.trim()) errors.email = "Sähköposti on pakollinen";
        if (!password) errors.password = "Salasana on pakollinen";
        setFieldErrors(errors);
        if (Object.keys(errors).length > 0) return;

        setSubmitting(true);
        try {
            const response = await apiPost("/auth/login", {
                email: email.trim(),
                password,
            });
            if (response.ok) {
                const data = await response.json();
                setToken(data.access_token);
                navigate("/");
                return;
            }
            if (response.status === 401) {
                setFormError("Väärä sähköposti tai salasana");
            } else if (response.status === 422) {
                setFormError("Tarkista sähköposti ja salasana");
            } else {
                setFormError(`Virhe (${response.status})`);
            }
        } catch {
            setFormError("Palvelimeen ei saatu yhteyttä");
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <div>
            <h1>Kirjaudu</h1>
            {formError && <p role="alert">{formError}</p>}
            <form onSubmit={handleSubmit} noValidate>
                <div>
                    <label htmlFor="email">Sähköposti</label>
                    <input id="email" type="email" value={email}
                           onChange={(e) => setEmail(e.target.value)} />
                    {fieldErrors.email && <p>{fieldErrors.email}</p>}
                </div>
                <div>
                    <label htmlFor="password">Salasana</label>
                    <input id="password" type="password" value={password}
                           onChange={(e) => setPassword(e.target.value)} />
                    {fieldErrors.password && <p>{fieldErrors.password}</p>}
                </div>
                <button type="submit" disabled={submitting}>
                    {submitting ? "Kirjaudutaan..." : "Kirjaudu"}
                </button>
            </form>
        </div>
    );
}

export default LoginPage;
