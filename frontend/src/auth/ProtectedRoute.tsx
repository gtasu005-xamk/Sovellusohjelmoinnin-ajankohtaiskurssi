import {Navigate, Outlet, useNavigate} from "react-router-dom";
import {getToken, clearToken} from "../auth/token.ts";
import Header from "../components/Header.tsx";
import {useQuery} from "@tanstack/react-query";
import {apiFetch} from "../api/client.ts";
import {queryKeys} from "../api/queryKeys.ts";

type User = {
    id: number;
    email: string;
    display_name: string;
}


function ProtectedRoute() {
    const navigate = useNavigate();
    const token = getToken();
    const {data: user, isLoading, isError} = useQuery({
        queryKey: queryKeys.me(token),
        queryFn: () => apiFetch<User>("/auth/me"),
        enabled: token !== null,
    });

    function handleLogout() {
        clearToken();
        navigate("/login", {replace: true});
    }

    if (!token) {
        return <Navigate to="/login" replace />;
    }

    if (isLoading) {
        return <p>Ladataan</p>;
    }

    if (isError || !user) {
        return <Navigate to="/login" replace />;
    }

    return (
        <>
            <Header displayName={user.display_name} email={user.email} onLogout={handleLogout} />
            <Outlet />
        </>
    );
}

export default ProtectedRoute;
