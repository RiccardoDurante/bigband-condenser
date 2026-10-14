---
document: Project Status
project: Big Band Condenser v1
updated: 2026-10-14 21:15 (CEST)
session: 2026-10-14 (Fase A verifica + Fase B pianificazione + Fase C samples setup + Fase D test case + Fase E extract + Risk Register v0.4)
---

# Project Status

## Milestone corrente

**M1 - Project Initiation Baseline**: COMPLETATO E RILASCIATO (tag ``M1-initiation`` su commit ``2abfee7``)
**M2 - Spike di fattibilita**: PIANIFICATO + TEST CASE PRONTO + FINDINGS PRELIMINARI
Piano operativo: ``docs/pmi/SPIKE_M2_PLAN.md`` v0.1.
Findings cloud preliminari: ``docs/pmi/KRONOS_KAI_KAIROS_FINDINGS.md`` v0.2.

## Task completati nella sessione del 14 ottobre 2026 (3h complessive)

### Fase A - Verifica assunzioni Charter (cappello Researcher, ~1h)

- Lettura read-only di 3 target in BigBand AI
- Verdetti: A2=B copia selettiva, A3=B copia integrale uso parziale, A4 scissa (bridge=D fuori scope, musicxml_writer orfano=A riuso diretto)
- Saving confermato: 12.5-19 ore
- Prodotto BIGBAND_AI_REUSE_ASSESSMENT.md v0.1
- Bump Risk Register v0.3

### Fase B - Pianificazione spike M2 (cappello Business Analyst, ~45min)

- Discussione estesa su test case (scartato Schneider sotto copyright, scelta Kronos CC-BY 4.0)
- Prodotto SPIKE_M2_PLAN.md v0.1 con 6 Q, timebox 12h, criteri successo

### Fase C - Setup samples/ (cappello Doc Writer, ~20min)

- Policy inclusione in samples/README.md
- Testo canonico LICENSE-CC-BY-4.0.txt
- Attribution specifica kronos_kai_kairos.LICENSE

### Fase D - Test case + preliminary findings (cappelli Developer + Researcher + Risk Officer, ~45min cloud)

- Ricevuto file Kronos (export Finale v27.4, 142 battute, 19 parti XML, 17 strumenti logici)
- Preliminary parse cloud: Q1 PASS, Q2 PASS 19/19 via partName, Q3 PASS 6/6 strumenti
- Scoperta R26: music21 instrument class INAFFIDABILE su Finale (tutti 19 misclassificati)
- Commit full score in repo + FINDINGS v0.1

### Fase E - Extract 32 battute (cappello Developer, ~25min cloud)

- Tentativo extract via music21.write() -> FAIL su durate 2048th in drum
- Fallback: extract via XML diretta (``xml.etree.ElementTree``)
- Scoperta R27 CRITICA: music21.write() fallisce su durate drum sub-32th tipiche Finale
- Prodotto extract 33 battute (pickup 0 + bars 1-32), 716 KB
- Bump FINDINGS a v0.2 con sezione Q4 anticipata + R27 proposto

### Chiusura - Risk Register v0.4 + STATUS (cappelli Risk Officer + Doc Writer, ~20min)

- Bump Risk Register v0.4: R07 e R12 Materializzati, R26 nuovo (score 6), R27 nuovo (score 9 critico)
- STATUS.md allineato con tutte le fasi A-E

## Task pendenti - priorita per prossima sessione

1. **Setup stub codice spike** (cappello Developer): cartella ``src/bigband_condenser/_spike/`` con 7 file Python stub + README. **Rimandato per fine sessione raggiunta oggi**
2. **Decisione architetturale Q4** (cappello Tech Lead): valutare se ``musicxml_writer.py`` orfano estende naturalmente a XML pass-through per drum. Possibile Change Request su Charter sezione 3.8
3. **Esecuzione Q1 locale** su extract 32 battute (replica cloud findings nel venv Windows)
4. **Esecuzione Q4 locale** con priorita alta (il bottleneck architetturale scoperto)
5. **Bump CHANGE_LOG v0.7** con D-020 (Kronos committato) e D-021 (Risk Register v0.4 con R07/R12 materializzati + R26/R27 nuovi)
6. Procedere Q2-Q3-Q5-Q6 secondo timebox

## Decisioni importanti registrate oggi

- D-017: Verifica assunzioni Charter completata
- D-018: Risk Register v0.3 con R04/R05/R06 declassati, R24 nuovo
- D-019: Piano operativo spike M2 con test case Kronos kai Kairos
- (da registrare in CHANGE_LOG prossima sessione): D-020 commit Kronos full + extract, D-021 Risk Register v0.4

## Rischi emersi oggi

- **R07 MATERIALIZZATO** (music21 male con drum): empiricamente confermato
- **R12 MATERIALIZZATO** (export Finale != Dorico): confermato su file reale
- **R26 nuovo** (music21 instrument class inaffidabile Finale): P=3, I=2, score 6
- **R27 nuovo CRITICO** (music21.write fallisce su drum sub-32th durations): P=3, I=3, score 9
- R04, R05 declassati "Non materializzato" (sessione precedente)
- R06 declassato "Non applicabile v1" (sessione precedente)

## Monte ore consumato in sessione

- 14 ottobre 2026: ~3h00 (15:30 - 21:15 CEST con pausa)
- Totale cumulato (12-13-14 ott): ~7h30 su 60h = 12.5%
- Residuo: ~52.5h in ~14 settimane (~3.75h/sett medie, sotto baseline 5h/sett)

## Prossimo passo consigliato

**Cappello Developer** per stub codice spike in ``src/bigband_condenser/_spike/``.

Oppure cappello Tech Lead per decisione architetturale su Q4 (XML pass-through strategy per drum) prima di scrivere codice.

Durata stimata prossima sessione: 1h-1h30.

## Debito tipografico PDF

Rinviato a refresh pre-tesi CAPM (correzioni B/C, tabella Budget Charter). Nessun impatto operativo.
