import {Routes, Route} from "react-router-dom";
import HomePage from "./pages/HomePage.tsx";
import './App.css'
import RegisterPage from "./pages/RegisterPage.tsx";
import LoginPage from "./pages/LoginPage.tsx";
import ProtectedRoute from "./auth/ProtectedRoute.tsx";

function App() {
  
  return (
    <Routes>
      <Route element={<ProtectedRoute />}>
              <Route path="/" element={<HomePage />} />
      </Route>
      
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />
    </Routes>
  )

}

export default App
