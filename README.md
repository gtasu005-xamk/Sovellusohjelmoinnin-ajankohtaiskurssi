Monorepo for Sovellusohjelmoinnin ajankohtaiskurssi 2026 (Exercise Progress Tracker)

/backend - FastAPI + Python backend

/frontend - Vite + React frontend

/docs - Projekti/sprintit dokumentaatiot

Vaatimukset:
Docker Desktop
Git
- Node.js ja Python tarvitaan, jos frontend ja/tai backend ajetaan paikallisesti ilman Dockeria.

Ympäristömuuttujat
Luo paikallinen .env kopioimalla .env.example (projektin juuri) ja frontend/.env kopioimalla frontend/.env.example.
.env sisältää sovelluksen asetukset, kuten tietokannan tunnukset ja yhteysosoitteen.
.env tiedostoa ei tule lisätä Gitiin!

| Muuttuja | Tarkoitus |
|---|---|
| SECRET_KEY | JWT-tokenien allekirjoitusavain (pakollinen, vaihda) |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT:n voimassaoloaika minuutteina |
| CORS_ORIGINS | Frontendin origin(it), joilta API hyväksyy selainpyynnöt (oletus http://localhost:5173) |
| SQLADMIN_USERNAME / SQLADMIN_PASSWORD | /admin-kirjautumisen tunnukset |
| SQLADMIN_SECRET_KEY | /admin-session cookien allekirjoitusavain |
| VITE_API_BASE_URL (frontend/.env) | API:n osoite selaimelle (http://localhost:8000) |

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


Tietokannan migraatiot ja katalogin seed
Kun kontit ovat käynnissä, aja projektin juuresta:
docker compose exec api alembic upgrade head
docker compose exec api python -m app.db.init_db
- ensimmäinen luo taulut, toinen lisää järjestelmän yksiköt, aktiviteetit ja niiden linkit (seed on idempotentti, voi ajaa uudelleen).

Kaksi erillistä kirjautumista
| URL | Tarkoitus | Tunnukset |
|---|---|---|
| http://localhost:5173/register, /login | Sovelluksen käyttäjät | Oma sähköposti + salasana → JWT (localStorage) → /auth/me |
| http://localhost:8000/admin | SQLAdmin, tietokannan selaus | .env: SQLADMIN_USERNAME / SQLADMIN_PASSWORD (oletus admin / admin) |

- Sovelluksen JWT EI avaa /admin-sivua, eikä admin-salasanalla voi kutsua /auth/me-endpointia.
- Oletustunnukset admin / admin on vaihdettava, jos sovellus on jaetussa käytössä.

SQLAdmin seedin jälkeen
- Unit types: 4 yksikköä (Duration (min), Distance (km), Reps, Weight (kg))
- Activity types: liikekohtaiset aktiviteetit (Running, Cycling, Bench press, Barbell curl, Hammer curl, Incline curl, Face pull, Other)
- Activity-unit links: Running/Cycling → duration + distance, voimaliikkeet → reps + weight (per set), Other → duration
- Sprint 3 käyttää tätä katalogia.

Ensimmäisen käyttäjän luonti
1. Avaa http://localhost:5173/register ja täytä sähköposti, salasana (väh. 8 merkkiä) ja nimimerkki.
2. Onnistunut rekisteröinti ohjaa /login-sivulle, kirjaudu samoilla tunnuksilla.
3. Etusivun yläreunassa näkyy nimimerkki ja sähköposti (haettu /auth/me:sta), ja käyttäjä näkyy myös SQLAdminin Users-taulussa.

Salasanasäännöt (rekisteröinti): 8–64 merkkiä, vähintään yksi iso kirjain ja yksi numero. Muuten HTTP 422.
Demotunnus: demo@example.com / Demo1234 / DisplayName: DemoTunnus
