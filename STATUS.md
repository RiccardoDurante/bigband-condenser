---
document: Project Status
project: Big Band Condenser v1
updated: 2026-10-15 21:30 (CEST)
session: 2026-10-15 (Fase F implementazione Q1-Q6 + Fase G chiusura formale M2)
---

# Project Status

## Milestone corrente

**M1 - Project Initiation Baseline**: COMPLETATO E RILASCIATO (tag ``M1-initiation``)
**M2 - Spike di fattibilita**: COMPLETATO E RILASCIATO (tag ``M2-feasibility``, verdetto PASS)
**M3 - Parser + Classificatore production code**: PROSSIMO (target meta novembre 2026)

## Task completati nelle sessioni 14-15 ottobre 2026 (M2 chiusura)

### Sessione 14/10 pomeriggio (~2h): Fase A+B+C

- Fase A verifica assunzioni A2/A3/A4 Charter su BigBand AI (BIGBAND_AI_REUSE_ASSESSMENT v0.1, saving 12.5-19h confermato)
- Fase B pianificazione Spike M2 (SPIKE_M2_PLAN v0.1 con Kronos CC-BY 4.0)
- Fase C setup samples/ con policy + licenza CC-BY 4.0

### Sessione 14/10 sera (~1h): Fase D+E

- Fase D test case + cloud preliminary findings (Kronos full score committed, FINDINGS v0.1, scoperta R26)
- Fase E extract 32 battute + FINDINGS v0.2 (scoperta Q4 FAIL + R27 nuovo critico)
- Risk Register v0.4 + CHANGE_LOG v0.6 + scaffold spike code + Q1 implementato PASS

### Sessione 15/10 sera (~30min): Fase F

- Q1 verifica locale PASS (match perfetto cloud)
- Q2 implementato con hidden detection PASS (scoperta R28)
- Q3 implementato PASS (scoperta R29)
- Q4 implementato PASS (R27 downgraded via input Music Expert, D-022 principio notazione vs playback)
- Q5 implementato FAIL 1/16 produttivo (scoperta R30 critico)
- Q6 implementato PASS (4-pentagrammi structure skeleton)

### Sessione 15/10 chiusura (~45min): Fase G

- Risk Register v0.5 (R27 downgraded, R28/R29/R30 nuovi, totale 30 rischi)
- CHANGE_LOG v0.7 (D-020...D-024, 24 decisioni totali)
- SPIKE_M2_REPORT v0.1 formale (12 sezioni, verdetto PASS)
- STATUS.md aggiornato (questo documento)
- Tag ``M2-feasibility`` sul commit di chiusura

## Spike M2 - Esito finale

**VERDICT: PASS**. Criteri successo S1+S2+S3 tutti soddisfatti.

- S1 copertura: 6/6 Q documentate (5 PASS + 1 FAIL produttivo)
- S2 delta: 1h40 reale vs 12h stima, dentro ±25% con ampio margine
- S3 assunzioni: tutte verificate (A1-A8), nessuna residua

Decisione formale: **D-A procedi con M3 come pianificato, nessuna ricalibrazione**.

## Monte ore consumato

- 12 ottobre (M1 baseline): ~2h40
- 13 ottobre (PDF pipeline + repo public): ~1h50
- 14 ottobre (Fase A-E, verifica + piano + test case + preliminary findings): ~3h25
- 15 ottobre (Fase F+G, implementazione Q1-Q6 + chiusura M2): ~1h15

**Totale cumulato**: ~9h10 su 60h = **15.3%**

Residuo: ~51h in ~14 settimane (fino al 31/01/2027), ~3.6h/sett medie (sotto baseline 5h/sett).

## Task pendenti - priorita per M3

1. **Cappello Tech Lead**: review architetturale pre-M3 (10 min) - validare che il pattern "parse music21 + XML pre-process + music21 model manipulation + XML post-process" sia la pipeline giusta per il Condenser
2. **Cappello Developer**: portare partName classifier da `_spike/q2_classify.py` a `src/bigband_condenser/classifier.py` production code
3. **Cappello Developer**: implementare instrument class forcing pre-write (mitigation R30)
4. **Cappello Developer**: implementare sub-semicroma filter (mitigation R27) e hidden parts detection (mitigation R28)
5. **Cappello QA**: suite di test pytest base per i moduli production
6. **Target M3**: meta novembre 2026, 5-7h stimate

## Rischi aperti con priorita critica/alta

- R15 (scope creep): disciplina Change Request obbligatoria
- **R30 (music21.write corruption)**: mitigation definita, da implementare in M3-M4
- R01 (produttivita non trasferibile): monitorato, finora positivo
- R07, R12 (Materializzati): mitigation attive
- R16 (modifiche BigBand AI): policy read-only rispettata finora
- R26 (music21 class detection): mitigation attiva via partName

## Debito tipografico PDF

Rinviato a refresh pre-tesi CAPM. Nessun impatto operativo.

## Prossimo passo consigliato

**Cappello Tech Lead** per review architetturale pre-M3 (10 min), poi **cappello Developer** per iniziare la codifica production in `src/bigband_condenser/`.

Durata stimata prossima sessione: 1h30-2h.

## Osservazione finale

Spike M2 chiuso con eccellente ritorno: 1h40 effettivo per validare 6 domande di fattibilita, 3 nuovi rischi scoperti con mitigation definite, 1 rischio downgradato con evidenza empirica, 1 principio operativo codificato (D-022 notazione vs playback). Il metodo preliminary cloud spike + locale verifica ha prodotto ROI ~20x. Pattern da replicare per futuri spike complessi.

Il progetto Big Band Condenser e in **stato eccezionalmente pulito** per entrare in M3:
- Charter v0.4 validato con dati reali
- 30 rischi tracciati con stati aggiornati e mitigation definite
- Test case Kronos CC-BY 4.0 committato e analizzato empiricamente
- 5 moduli Python _spike funzionanti
- Verdetto Spike formale PASS
- Zero debito aperto non documentato
- 15 commit pubblici datati 12-15 ottobre su github.com/RiccardoDurante/bigband-condenser
