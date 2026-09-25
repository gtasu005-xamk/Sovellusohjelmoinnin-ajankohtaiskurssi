import {useEffect, useState} from "react";
import {Navigate, Outlet} from "react-router-dom";
import {apiGet} from "../api/client.ts";
import {getToken} from "../auth/token.ts";

type AuthStatus = "loading" | "authenticated" | "unauthenticated";

function ProtectedRoute() {
    const [status, setStatus] = useState<AuthStatus>(() =>
        getToken() ? "loading" : "unauthenticated");

    useEffect(() => {
        if (!getToken()) return;
        apiGet("/auth/me")
            .then((response) => setStatus(response.ok ? "authenticated" : "unauthenticated"))
            .catch(() => setStatus("unauthenticated"));}, []);

    if (status === "loading") {
        return <p>Ladataan...</p>;}

    if (status === "unauthenticated") {
        return <Navigate to="/login" replace />;}
    return <Outlet />;
}

export default ProtectedRoute;
