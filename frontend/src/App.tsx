import {Routes, Route} from "react-router-dom";
import HomePage from "./pages/HomePage.tsx";
import './App.css'
import RegisterPage from "./pages/RegisterPage.tsx";
import LoginPage from "./pages/LoginPage.tsx";
import ProtectedRoute from "./auth/ProtectedRoute.tsx";
import SessionsPage from "./pages/SessionsPage.tsx";
import SessionFormPage from "./pages/SessionFormPage.tsx";
import PlansPage from "./pages/PlansPage.tsx";
import PlanDetailPage from "./pages/PlanDetailPage.tsx";

function App() {
  
  return (
    <Routes>
      <Route element={<ProtectedRoute />}>
              <Route path="/" element={<HomePage />} />
              <Route path="/sessions" element={<SessionsPage />} />
              <Route path="/sessions/new" element={<SessionFormPage />} />
              <Route path="/sessions/:sessionId" element={<SessionFormPage />} />
              <Route path="/plans" element={<PlansPage />} />
              <Route path="/plans/:planId" element={<PlanDetailPage />} />

      </Route>
      
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />
    </Routes>
  )

}

export default App
