import {useEffect, useState} from "react";
import {Navigate, Outlet, useNavigate} from "react-router-dom";
import {apiGet} from "../api/client.ts";
import {getToken, clearToken} from "../auth/token.ts";
import Header from "../components/Header.tsx";


type User = {
    id: number;
    email: string;
    display_name: string;
}


function ProtectedRoute() {
    const navigate = useNavigate();
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(() => getToken() !== null);

    useEffect(() => {
        if (!getToken()) return;
        apiGet("/auth/me")
            .then(async (response) => setUser(response.ok ? await response.json() : null))
            .catch(() => setUser(null))
            .finally(() => setLoading(false));}, []);

    function handleLogout() { clearToken(); setUser(null);
        navigate("/login", {replace: true});}

    if (loading) {
        return <p>Ladataan</p>;}

    if (!user) { return <Navigate to="/login" replace />;}

    return (
        <>
            <Header displayName={user.display_name} email={user.email} onLogout={handleLogout} />
            <Outlet />
        </>
    );
}

export default ProtectedRoute;
