import {useState, type FormEvent} from "react";
import {useNavigate} from "react-router-dom";
import {apiPost} from "../api/client.ts";


type FieldName = "email" | "password" | "display_name";
type FieldErrors = Partial<Record<FieldName, string>>;
type ValidationError = {loc: (string | number)[]; msg: string};

function mapValidationErrors(detail: ValidationError[]): FieldErrors {
    const errors: FieldErrors = {};
    for (const item of detail) {
        const field = item.loc[item.loc.length - 1];
        if (field === "email" || field === "password" || field === "display_name") {
            errors[field] = item.msg;
        }
    }
    return errors;
}
// Onnistuneen rekisteröinnin jälkeen ohjataan /login-sivulle.
// POST /auth/register palauttaa UserPublic-olion eikä tokenia, joten auto-login ei ole mahdollinen.

function RegisterPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [displayName, setDisplayName] = useState("");
    const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
    const [formError, setFormError] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setFormError(null);

        const errors: FieldErrors = {};
        if (!email.trim()) errors.email = "Sähköposti on pakollinen";
        if (!password) errors.password = "Salasana on pakollinen";
        if (!displayName.trim()) errors.display_name = "Nimimerkki on pakollinen";
        setFieldErrors(errors);
        if (Object.keys(errors).length > 0) return;

        setSubmitting(true);
        try {
            const response = await apiPost("/auth/register", {
                email: email.trim(),
                password,
                display_name: displayName.trim(),
            });
            if (response.ok) {
                navigate("/login");
                return;
            }
            const data = await response.json().catch(() => null);
            if (response.status === 422 && Array.isArray(data?.detail)) {
                const mapped = mapValidationErrors(data.detail);
                setFieldErrors(mapped);
                if (Object.keys(mapped).length === 0) setFormError("Tarkista lomakkeen tiedot");
            } else {
                setFormError(typeof data?.detail === "string" ? data.detail : `Virhe (${response.status})`);
            }
        } catch {
            setFormError("Palvelimeen ei saatu yhteyttä");
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <div>
            <h1>Rekisteröidy</h1>
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
                <div>
                    <label htmlFor="display_name">Nimimerkki</label>
                    <input id="display_name" type="text" value={displayName}
                           onChange={(e) => setDisplayName(e.target.value)} />
                    {fieldErrors.display_name && <p>{fieldErrors.display_name}</p>}
                </div>
                <button type="submit" disabled={submitting}>
                    {submitting ? "Rekisteröidään..." : "Rekisteröidy"}
                </button>
            </form>
        </div>
    );
}

export default RegisterPage;
