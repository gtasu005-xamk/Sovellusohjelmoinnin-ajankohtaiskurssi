# IDOR-demo: toisen käyttäjän datan suojaus

Tämän ohjeen avulla voit todeta, ettei käyttäjä B pääse käsiksi käyttäjän A sessioihin, planeihin, tavoitteisiin tai kalenteriin, vaikka tietäisi niiden ID:t.

## Odotetut vastaukset

| Kutsu | Tulos |
|---|---|
| Ei tokenia | `401` `{"detail":"Invalid authentication credentials"}` |
| Toisen käyttäjän session GET, PATCH, DELETE tai clone | `404` `{"detail":"Session not found"}` |
| Toisen käyttäjän planin GET, PATCH, DELETE tai oman session liittäminen hänen planiinsa | `404` `{"detail":"Plan not found"}` |
| Toisen käyttäjän tavoitteen GET, PATCH tai DELETE | `404` `{"detail":"Goal not found"}` |
| Toisen käyttäjän session liittäminen omaan planiin | `404` `{"detail":"Session not found"}` |
| `GET /sessions` tai `GET /calendar` toisen käyttäjän `plan_id`:llä | `200` ja tyhjä lista `[]` |
| Olematon ID (esim. `999999`) | sama `404`-vastaus kuin toisen käyttäjän ID:llä |

API vastaa yksittäisten objektien kohdalla **404 eikä 403**. Lisäksi `detail` on sama kuin kokonaan olemattomalla ID:llä. Näin B ei saa selville, onko jokin ID olemassa ja kuuluuko se jollekulle toiselle. Listat (`/sessions`, `/plans`, `/goals`, `/calendar`) eivät koskaan sisällä toisen käyttäjän rivejä.

Projektin ID:t ovat kokonaislukuja. Satunnaisena ID:nä käytetään siksi olematonta numeroa. UUID polussa antaa `422`, koska se ei ole kelvollinen kokonaisluku. Se on syötteen validointia eikä liity käyttöoikeuksiin.

## Ennen kuin aloitat

Käynnistä projekti ja aja migraatiot ja seed projektin juuressa. Seed lisää katalogin yksiköt ja aktiviteetit, joita tavoite tarvitsee.

```powershell
docker compose up -d --build
docker compose exec api alembic upgrade head
docker compose exec api python -m app.db.init_db
```

Kaikki alla olevat komennot ajetaan **samassa PowerShell-ikkunassa**, koska tokenit ja ID:t tallennetaan muuttujiin.

## 1. Apufunktiot

`Call` tulostaa statuskoodin ja vastauksen myös virhetilanteissa. `Api` palauttaa vastauksen objektina, ja sitä käytetään datan luontiin.

```powershell
$API = "http://localhost:8000"

function Call($Method, $Path, $Token, $Body) {
    $headers = @{}
    if ($Token) { $headers["Authorization"] = "Bearer $Token" }
    $params = @{ Method = $Method; Uri = "$API$Path"; Headers = $headers; ContentType = "application/json"; UseBasicParsing = $true }
    if ($Body) { $params.Body = ($Body | ConvertTo-Json -Depth 5) }
    try {
        $response = Invoke-WebRequest @params
        "$($response.StatusCode) $($response.Content)"
    } catch {
        "$([int]$_.Exception.Response.StatusCode) $($_.ErrorDetails.Message)"
    }
}

function Api($Method, $Path, $Token, $Body) {
    $headers = @{ Authorization = "Bearer $Token" }
    if ($Body) {
        return Invoke-RestMethod -Method $Method -Uri "$API$Path" -Headers $headers -ContentType "application/json" -Body ($Body | ConvertTo-Json -Depth 5)
    }
    return Invoke-RestMethod -Method $Method -Uri "$API$Path" -Headers $headers
}
```

## 2. Käyttäjät A ja B

`display_name` vaatii vähintään 8 merkkiä. Jos käyttäjä on jo olemassa, rekisteröinti palauttaa 409, mutta kirjautuminen toimii silti.

```powershell
function Login($Email, $Name) {
    Call POST "/auth/register" $null @{ email = $Email; password = "Demo1234"; display_name = $Name } | Out-Null
    $login = Invoke-RestMethod -Method POST -Uri "$API/auth/login" -ContentType "application/json" -Body (@{ email = $Email; password = "Demo1234" } | ConvertTo-Json)
    return $login.access_token
}

$tokenA = Login "idor-a@example.com" "Kayttaja A"
$tokenB = Login "idor-b@example.com" "Kayttaja B"
```

## 3. A luo session, planin ja tavoitteen

Haetaan ensin aktiviteetit, jotta käytössä ovat oikeat `unit_type_id`-arvot.

```powershell
$activityTypes = Api GET "/activity-types" $tokenA
$running = $activityTypes | Where-Object { $_.slug -eq "running" }
$durationId = ($running.unit_links | Where-Object { $_.unit_type.slug -eq "duration_min" }).unit_type_id
$distanceId = ($running.unit_links | Where-Object { $_.unit_type.slug -eq "distance_km" }).unit_type_id

$sessionA = Api POST "/sessions" $tokenA @{
    name = "A:n juoksu"
    session_at = "2026-10-20T17:00:00Z"
    items = @(@{ activity_type_id = $running.id; measurements = @(@{ unit_type_id = $durationId; planned_value = 30 }) })
}
$planA = Api POST "/plans" $tokenA @{ name = "A:n plan" }
Api POST "/plans/$($planA.id)/sessions/$($sessionA.id)" $tokenA | Out-Null
$goalA = Api POST "/goals" $tokenA @{ unit_type_id = $distanceId; target_value = 20; period = "week" }
```

A näkee omat objektinsa:

```powershell
Call GET "/sessions/$($sessionA.id)" $tokenA   # 200
Call GET "/plans/$($planA.id)" $tokenA         # 200
Call GET "/goals/$($goalA.id)" $tokenA         # 200
```

B tarvitsee liittämistestiä varten oman planin ja session:

```powershell
$planB = Api POST "/plans" $tokenB @{ name = "B:n plan" }
$sessionB = Api POST "/sessions" $tokenB @{ name = "B:n sessio" }
```

## 4. Ilman tokenia

```powershell
Call GET "/sessions" $null
# 401 {"detail":"Invalid authentication credentials"}
```

## 5. B yrittää käyttää A:n objekteja

**Sessio:**

```powershell
Call GET "/sessions/$($sessionA.id)" $tokenB
Call PATCH "/sessions/$($sessionA.id)" $tokenB @{ name = "hakkeroitu" }
Call DELETE "/sessions/$($sessionA.id)" $tokenB
Call POST "/sessions/$($sessionA.id)/clone" $tokenB @{ name = "kopio" }
# kaikki: 404 {"detail":"Session not found"}
```

**Plan:**

```powershell
Call GET "/plans/$($planA.id)" $tokenB
Call PATCH "/plans/$($planA.id)" $tokenB @{ name = "hakkeroitu" }
Call DELETE "/plans/$($planA.id)" $tokenB
Call POST "/plans/$($planA.id)/sessions/$($sessionB.id)" $tokenB
# kaikki: 404 {"detail":"Plan not found"}
```

**A:n session liittäminen B:n omaan planiin:**

```powershell
Call POST "/plans/$($planB.id)/sessions/$($sessionA.id)" $tokenB
# 404 {"detail":"Session not found"}
```

**Tavoite:**

```powershell
Call GET "/goals/$($goalA.id)" $tokenB
Call PATCH "/goals/$($goalA.id)" $tokenB @{ active = $false }
Call DELETE "/goals/$($goalA.id)" $tokenB
# kaikki: 404 {"detail":"Goal not found"}
```

**Olematon ID antaa saman vastauksen:**

```powershell
Call GET "/sessions/999999" $tokenB
# 404 {"detail":"Session not found"}
```

## 6. B:n listat

```powershell
Call GET "/sessions" $tokenB    # 200, vain B:n sessio
Call GET "/plans" $tokenB       # 200, vain B:n plan
Call GET "/goals" $tokenB       # 200 []
Call GET "/calendar?from=2026-10-01T00:00:00Z&to=2026-10-31T23:59:59Z" $tokenB   # 200 []
```

**A:n `plan_id` suodattimena antaa tyhjän listan eikä virhettä:**

```powershell
Call GET "/sessions?plan_id=$($planA.id)" $tokenB
Call GET "/calendar?from=2026-10-01T00:00:00Z&to=2026-10-31T23:59:59Z&plan_id=$($planA.id)" $tokenB
# molemmat: 200 []
```

## 7. A:n data ei muuttunut

```powershell
Call GET "/sessions/$($sessionA.id)" $tokenA
# 200, nimi on yhä "A:n juoksu" ja plan_id on A:n plan
```

B:n PATCH- ja DELETE-yritykset eivät muuttaneet tai poistaneet mitään.

## Käyttöliittymässä

Sama näkyy frontendissä. Kun B avaa osoitteen `/sessions/<A:n id>`, sivulla lukee "Session not found.". Osoitteessa `/plans/<A:n id>` lukee "Plan not found.".
