# Runbook: App-specifieke apparaatvarianten (iPad / Phone) — Playbook

> Geleerd uit het JaccoShell Raadsagent-traject, 30 september 2026. Aanleiding: een ander model
> (Grok) had een "iPad-vriendelijke" UI gebouwd met globale CSS-aanpassingen; het wrakte de
> desktop-ervaring en moest worden teruggedraaid. De hersenbuild (commit `0eb2b0a` +
> `phone.css`/`phone.js`) ging zonder enige desktop-regressie live. Dit document = het recept
> voor toekomstige projecten die een echte iPad- en/of telefoonvariant nodig hebben.

## De kernles (waarom de eerste poging faalde)

**Fout:** apparaat-specifieke stijl mengen in de globale CSS met breedte-media-queries
(`@media (max-width: …)`). Elke desktopgebruiker met een smal venster kreeg toen tablet-layout;
niets was meer voorspelbaar.

**Juiste architectuur: een apparaat-laag, geactiveerd door class, niet door breedte.**

## Het recept

### 1. Detectie: vinger + scherm, niet User-Agent

`static/tablet.js` (45 regels) zet bij load:

```js
var isTablet = (navigator.maxTouchPoints > 1) && (Math.min(screen.width, screen.height) >= 600);
document.documentElement.classList.toggle('is-tablet', isTablet);
```

- **Vinger als primaire invoer** (`maxTouchPoints > 1`) én **minimale schermafmeting** → tablet.
- Desktop met touchscreen of een klein laptopvenster krijgt NIET de tabletlaag.
- Werkt ook voor **iPadOS dat zich als macOS voordoet** (iPadOS 13+ rapporteert een Mac-UA;
  touch+size valt het alsnog correct aan).
- Telefoonvariant analoog: touch + scherm < 600px → `is-phone` (of aparte detectie).
- Zet de class vóór eerste render (inline script in `<head>`) zodat er geen flits van verkeerde
  layout is (FOUC).

### 2. Alle stijl in een eigen laag, nergens anders

- `static/tablet.css` (798 regels in dit project) — elke regel gescoped onder `html.is-tablet`.
- Desktop-CSS blijft 100% onaangetast; geen gedeelde regels, geen overrides halverwege bestanden.
- `web.py` laadt de laag conditioneel: `<link rel="stylesheet" href="/static/tablet.css">` alleen als
  de request-context tablet is (of onvoorwaardelijk — de class-guard maakt hem inert op desktop).
- Telefonie: zelfde patroon met `phone.css`/`phone.js` + `html.is-phone`.

### 3. Ontwerp per apparaat, niet "responsief verkleinen"

Wat de tabletlaag in dit project deed (patroon voor hergebruik):

- **Navigatie:** sidebar wordt een bovenste tabbladbalk; hover-acties worden tik-acties.
- **Tabellen → kaarten:** dichte registertabellen worden stapelkaarten (titel boven, status als
  pill rechts, geen horizontale scroll).
- **Aanraakdoelen ≥ 44px**, geen hover-only informaties, grotere lettergroottes voor leescomfort.
- **Portret vs landschap** beide getest (kaarten full-width in portret).
- **Behoud van informatie-dichtheid waar het kan:** tablet is geen grote telefoon; kolommen die
  werken blijven, alleen de interactie verandert.

### 4. QA: multi-viewport screenshot-gate (dit is het goud)

Het project bouwde een herhaalbare QA-pijplijn (`/tmp/phqa`-toolkit + Playwright):

1. **shoot.py**: fullpage-screenshots van élke route × élk profiel
   (`desktop, desktop-narrow, desktop-tiny, ipad-p, ipad-l, ipadpro-l, phone-p, phone-l` …)
   via een headless-browser; `--resume` maakt incrementele rondes goedkoop.
2. **gate.py**: geautomatiseerde checks per screenshot — geen horizontale overflow, geen
   overlappende elementen, tekst niet afgeknipt, klikdoelen groot genoeg. Exit-code bepaalt
   doorgaan (`PHONEGATE 0`) of terug naar tekenwerk.
3. **Vision-QA**: screenshots naar een vision-model (Gemini Flash; $0.25/ronde) met de vraag
   "wat raakt af/overlap/leesbaarheid". Vangt wat automatische checks missen.
4. **Fysieke check door de gebruiker** op het echte apparaat als laatste poort.

Deze pijplijn is het verschil tussen "ziet er uit op mijn scherm" en "werkt op iemands iPad".

### 5. Discipline

- **Test-copy eerst** (`/tmp/js-tablet`), pas merge naar de hoofdtak na groene gate + eigen review.
- **One commit per apparaatlaag** (`0eb2b0a UI: tablet-laag alleen voor iPad`) met een commitbericht
  dat de detectieregel en de scope noemt — zo is terugdraaien één revert.
- **Regressietests**: bestaande suite blijft groen (desktop onaangetast); nieuwe tests asserten de
  class-detectie en de belangrijkste tablet-layoutinvarianten.
- **Rollback-pad bewaken**: als een apparaatlaag een desktop-bug introduceert, is de laag niet
  goed genoeg gescoped — terug naar de tekenbord, niet patchen in de globale CSS.

## Waarom class-scope beter is dan media-queries (samenvatting)

| | media-queries (breedte) | class-laag (touch+formaat) |
|---|---|---|
| Smal desktopvenster | krijgt mobiele UI (fout) | blijft desktop (goed) |
| iPad in desktop-mode | gemist | gedetecteerd via touch |
| Scope van wijzigingen | overal, moeilijk te achterhalen | één bestand, één selector-prefix |
| Terugdraaien | pijnlijk | één revert / laag uitschakelen |
| Testen | browser-resize | class togglen in een test is triviaal |

## Checklist voor een nieuwe apparaatvariant

1. Detectie-script (touch + formaat) → `html.is-<device>`, inline vóór render
2. Lege `<device>.css` + `<device>.js` scaffold, gescoped op de class
3. Per module beslissen: kaart-lay-out? navigatie-vorm? aanraakdoelen? dichtheid?
4. shoot.py-profiel toevoegen + gate.py-regels voor het nieuwe formaat
5. Vision-QA-ronde + fysieke check op het apparaat
6. Test-copy → groene gate → één commit → deploy → live screenshots als bewijs

## Artefacten om te kopiëren naar nieuwe projecten

- `static/tablet.js` (detectie, ~45 regels) — direct herbruikbaar
- shoot.py/gate.py multi-viewport QA-toolkit — direct herbruikbaar (backend-agnostisch: werkt op elke URL)
- Het commitbericht-formaat: "UI: <variant>-laag alleen voor <device>" + detectieregel in de body
