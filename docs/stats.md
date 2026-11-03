# Tilastot (Sprint 4)

Kaikki `/stats`-endpointit vaativat kirjautumisen (Bearer-token) ja palauttavat vain kirjautuneen käyttäjän dataa. Vastausten tarkat muodot löytyvät OpenAPI-dokumentaatiosta: http://localhost:8000/docs (ryhmä **stats**).

## Endpointit

| Endpoint | Mihin | Query-parametrit |
|---|---|---|
| `GET /stats/summary` | Yhteenveto aikaväliltä: sessioiden määrä, kokonaiskesto ja -matka, keskim. intensiteetti ja jako harjoituksittain (`by_activity`) | `from`, `to` (pakolliset, ISO-aika) |
| `GET /stats/progress` | Aikasarja kaavioita varten, lista pisteitä `{period_label, period_start, value}` | `from`, `to` (pakolliset), `metric` = `sessions` / `duration_min` / `distance_km` (oletus `sessions`), `granularity` = `week` / `month` (oletus `week`), `activity_type_id` (valinnainen) |
| `GET /stats/streaks` | Nykyinen ja pisin treeniputki päivinä sekä viimeisin treenipäivä | ei parametreja, lasketaan koko historiasta |

Virheet:
- `from` on `to`:n jälkeen → `400`
- tuntematon `metric` tai `granularity` → `422`
- tuntematon `activity_type_id` → `422`
- ei tokenia → `401`

Esimerkki:

```
GET /stats/progress?from=2026-09-01T00:00:00Z&to=2026-10-31T23:59:59Z&metric=distance_km&granularity=month
```

## Mistä luvut tulevat

- **Kesto ja matka** lasketaan mittausten `actual_value`-arvoista. Yksikkö tunnistetaan Sprint 2:n katalogin slugista: `duration_min` = kesto, `distance_km` = matka. Planned-arvoja ei lasketa mukaan.
- **Ajastamattomat sessiot** (`session_at` puuttuu) eivät näy tilastoissa.
- **Viikot** ovat ISO-viikkoja (alkavat maanantaina), esim. `2026-W44`. Kuukaudet ovat muotoa `2026-10`.
- **Laskenta** tehdään tiedostossa `backend/app/services/analytics.py`. Se on pelkkää Pythonia ilman FastAPI:a tai tietokantaa. `backend/app/services/stats.py` hakee käyttäjän sessiot kannasta ja antaa ne analytiikalle.

## Putken määritelmä

Putki on peräkkäisten päivien (UTC) määrä, joina käyttäjällä on vähintään yksi päivätty sessio. Ajastamattomia ja tulevaisuuteen ajastettuja sessioita ei lasketa. Nykyinen putki jatkuu, jos viimeisin treenipäivä on tänään tai eilen, joten putki ei katkea aamulla ennen päivän treeniä. Jos viimeisin treeni oli toissapäivänä tai aiemmin, nykyinen putki on 0. Pisin putki on koko historian pisin peräkkäisten päivien jakso.

## Testit

Analytiikan yksikkötestit kutsuvat suoraan `services/analytics.py`:tä, joten ne eivät tarvitse Postgresia eikä Dockeria:

```
cd backend
.venv\Scripts\python -m pytest tests/test_analytics.py
```

Käyttäjärajauksen testit (käyttäjä A ei näe B:n tilastoja) ovat tiedostossa `tests/test_stats_scoping.py`. Kaikki testit saa ajettua komennolla `.venv\Scripts\python -m pytest`.

## Frontendissä

- **Edistyminen** (`/progress`) näyttää sessiot ajan yli ja matkan ja keston harjoituksittain. Aikavälin ja jakson (viikko/kuukausi) voi valita.
- **Etusivu** näyttää `/stats/summary`-luvut valitulle jaksolle viimeisimpien sessioiden yläpuolella.


