Monorepo for Sovellusohjelmoinnin ajankohtaiskurssi 2026 (Exercise Progress Tracker)

/backend - FastAPI + Python backend

/frontend - Vite + React frontend

/docs - Projekti/sprintit dokumentaatiot

Vaatimukset:
Docker Desktop
Git
- Node.js ja Python tarvitaan, jos frontend ja/tai backend ajetaan paikallisesti ilman Dockeria.

Ympäristömuuttujat
Luo paikallinen .env kopioimalla .env.example.
.env sisältää sovelluksen asetukset, kuten tietokannan tunnukset ja yhteysosoitteen. 
.env tiedostoa ei tule lisätä Gitiin!

Sovelluksen käynnistäminen
Käynnistä sovellus projektin juuresta:
docker compose up --build
- komento käynnistää PostgreSQL-tietokannan, FastAPI-backendin ja Vite-frontendin.

Palvelut:
frontend        =       http://localhost:5173
API             =       http://localhost:8000
API-dokumentaatio =     http://localhost:8000/docs
Health check    =       http://localhost:8000/health
PostgreSQL      =       localhost:5432

