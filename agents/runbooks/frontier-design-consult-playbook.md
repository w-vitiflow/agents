# Runbook: Frontier-Design Consult (Opus 5.5) — Playbook

> Geleerd uit het JaccoShell Raadsagent-traject, 29–30 september 2026 (consult ≈ $2–3,
> volledige implementatie + 3 reviewcycli → 118+ tests groen, 6 deploys, nul productieregressies).
> Doel: herhaalbaar recept voor "frontier-ontwerp kopen met lokale modellen die het bouwen".

## Waarom dit werkte (kerninzicht)

Frontier-modellen zijn duur in token maar sterk in **smaak, patterns en het zien van fouten**.
Lokale/goedkope modellen zijn sterk in **onbeperkt bouwen en herhalen**. De winning combinatie:
koop *oordeel*, bouw *lokaal*, laat de frontier-rijke het *resultaat* weer beoordelen in cycli.
De frontier-modél heeft dan 3 screenshots per cyclus nodig (~$0,50–1,00), niet de hele codebase.

## Recept in 7 stappen

1. **Pakket samenstellen vóór de consult** (`opus-design-brief.md` + `opus-design-pack/`):
   - Zelfstandige brief: productcontext, doelgroep, beperkingen (stack, huisstijl, toegankelijkheid), wat er al staat.
   - **14 fullpage-screenshots van élke route** (desktop), per scherm een contextbestand (wat is dit, welke data).
   - INDEX.md die het pakket beschrijft. Frontier-modellen redeneren beter met beeld+context dan met HTML-dumps.
2. **Twee beurten i.p.v. één**: eerste aanroep = Top-10 aanbevelingen; tweede = implementatieplan voor de gekozen drie.
   **Waarom:** Opus schrijft voorbij `max_tokens` en de response truncate stilletjes. Twee gerichte beurten met een
   expliciet eindmarker werkt beter dan één lange poging.
3. **Vraag om gestructureerde output**: per advies {patroonnaam, module, HTML/CSS-schets, rationale, effort S/M/L}.
   Dat maakt advies direct bouwbaar en rangschikbaar.
4. **Laat de lokale agent bouwen** (GLM in dit geval): advies → todo's → per item implementeren met tests. Additief-only
   discipline: nieuwe routes/CSS, productieroutes onaangetast.
5. **Reviewcycli (het goud):** na elke implementatieronde nieuwe fullpage-screenshots → zelfde OpenRouter-call-formaat →
   verdict per scherm (goed/polijsten/fundamenteel-opnieuw) → fixes → herdeploy. 3 cycli was genoeg.
6. **Verifieer pariteit vóór je reviewt:** het adviesdocument dat uit cyclus 3 kwam: render de **build-hash** in de UI en
   review alleen screenshots waarvan de hash ≡ productie. Anders review je oude screenshots en betaal je voor herhaalde
   vondsten (dit kostte ons één volledige cyclus).
7. **Bewaar het archief:** advies, brief, screenshots en verdicts in een reports-map; werk de variant-concepten die niet
   live gingen naar een archiefpagina (bijv. `/workshop-archief`) — ideeën-recycling zonder productie-clutter.

## Wat het opleverde (concreet, voor calibratie)

- **5 echte productiebugs gevonden uitsluitend uit screenshots** (dubbele paginakop, `termijn <titel>` i.p.v. datum,
  overlappende kolomkoppen, afgebroken badge-lettergrepen, off-brand linkkleuren) — vóór énig ontwerpadvies.
- 3 flagship-patterns die live gingen: Zaakdossier (identiteit = zaaknummer), Termijn-hittestrook (pure CSS),
  Raadsritme-horizon.
- Eindoordeel cyclus 3: geen enkel scherm "fundamenteel-opnieuw" — de structuur was goed; rest was polijsten.

## Model-split lessons

| Rol | Model | Waarom |
|---|---|---|
| Ontwerp + review-verdicts | frontier (Opus 5.5) | smaak, patroonherkenning, bug-zien in pixels |
| Implementatie | lokaal (GLM-5.3-Flash-EXL3) | onbeperkte iteratie, geen token angst, tests draaien |
| Vision QA op screenshots | goedkope vision (Gemini Flash) | $0.25 voor 28 calls; goed genoeg voor layoutchecks |
| Compressie bij volle context | goedkoop flash-model | context-management is geen reden voor een frontier-model |

## Valkuilen

- **Eén shot te groot** → truncatie midden in het advies. Twee beurten + eindmarker.
- **Stale screenshots reviewen** → herhaalde valse bevindingen. Build-hash-pariteitscheck eerst.
- **Advies als "waarheid" behandelen** → sommige adviezen passen niet; de agent mag adviezen weglaten met redenen
  (de meeste Top-10-gingen wel live; de afvallers staan in het archief).
- **Review-verdicts zonder herhaalbare invoer** → bewaar de screenshot-pack per cyclus, anders kun je het verdict
  nooit reproduceren.

## Herbruikbare artefacten

- Brief-template: zie `opus-design-brief.md`-structuur in dit document (context, beperkingen, huidige staat, vraag).
- Verdict-format per scherm: {route, hash, oordeel, bevindingen[], fix-les}.
- Screenshot-pack-layout: `{pack}/{ctx_<route>.md + <route>.png}` + INDEX.md.
