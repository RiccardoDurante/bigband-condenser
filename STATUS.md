---
document: Project Status
project: Big Band Condenser v1
updated: 2026-10-18 16:09 (CEST)
session: 2026-10-18 (M4.1-M4.3 chiusi, fix visual-gate R32, scope M4.4 deciso)
---

# Project Status

## Milestone corrente

**M1 - Project Initiation Baseline**: COMPLETATO (tag `M1-initiation`)
**M2 - Spike di fattibilita**: COMPLETATO (tag `M2-feasibility`, verdetto PASS)
**M3 - Parser + Classificatore production code**: COMPLETATO (tag `M3-production`)
**M4 - Condensatore di sezione funzionante**: IN CORSO (target fine novembre 2026)
  - M4.1 (metadata preservation): CHIUSO
  - M4.2 (measure structure preservation): CHIUSO (tag `M4.2-measures`, `M4.2-visual-fix`)
  - M4.3 (single-voice passthrough): CHIUSO (tag `M4.3-passthrough`)
  - M4.4 (split 2+3 su 5 voci reeds): SCOPING fatto, implementazione da iniziare

## Task completati nella sessione 18 ottobre (circa 1h10)

### M4.2 - Fix critico visual-gate (R32)

- Bug segnalato dall'utente: misure visivamente incomplete in Dorico nonostante durata XML totale corretta (32/66 misure)
- Diagnosi empirica con script dedicati (`scripts/diagnose_measure_durations.py`, `scripts/diagnose_visible_durations.py`, `scripts/probe_skeleton.py`, `scripts/probe_pipeline.py`): isolato il bug nel music21 v10.5 MusicXML writer, non nel codice del progetto (0 hidden in-memory, 34 hidden nel file scritto)
- Fix: `src/bigband_condenser/musicxml_sanitizer.py` (post-write XML sanitizer, rimuove `print-object="no"` spurio da Rest)
- Rivalidato: 0 misure numericamente errate, 0 visivamente corte, confermato in Dorico dall'utente
- 52 pytest GREEN (nessuna regressione)

### M4.3 - Single-voice passthrough

- `scripts/preview_single_voice.py`: isola la pipeline di scrittura dallo split 2+3, zero modifiche a `reeds.py`
- Validato su Soprano Sax (55 note, 33 misure): upper 55/55, lower 0 (atteso), dual-gate numerico + Dorico OK
- `TestReedsCondenserM43Passthrough` (2 nuovi test), 19/19 GREEN su `test_condenser_reeds.py`

### Documentazione PMI

- Risk Register v0.6: R31 formalizzato (dual-gate numerico totale+visibile), R32 nuovo (music21 writer quirk), entrambi Mitigato
- WBS_M4.md v0.2: chiusura M4.2 (nota fix) e M4.3
- CHANGE_LOG v0.9: D-028 (chiusura M4.1-M4.3 + R31/R32), D-029 (decisione scope M4.4)

## Decisione di scope - M4.4

Split 2+3 su tutte e 5 le voci reeds verra validato su un **nuovo segmento denso** (tutti i 5 reeds attivi simultaneamente, es. shout chorus/tutti), non su riuso diretto di `kronos_kai_kairos_extract.musicxml`. Motivazione: l'extract esistente non garantisce onset complessi/incroci di voce necessari a stressare la logica di split; un segmento dedicato isola meglio eventuali bug introdotti dallo split stesso rispetto a bug di pipeline (gia' esclusi da M4.1-M4.3). Vedi D-029 in CHANGE_LOG.md.

## Lezione di metodo (da portare avanti su tutto M4 restante)

Il gate numerico "durata totale" da solo NON basta a validare la notazione. Da M4.2 in poi, ogni sotto-step richiede il **dual-gate numerico** (durata totale + durata visibile/print-object) PRIMA del gate visivo Dorico. Gli script `diagnose_measure_durations.py` e `diagnose_visible_durations.py` sono riutilizzabili su qualunque output futuro.

## Monte ore consumato

- Cumulato al 16 ottobre: circa 11h10 su 60h (18.6%)
- 18 ottobre (M4.1-M4.3 + fix R32 + docs): circa 1h10
- **Totale cumulato**: circa 12h20 su 60h = **20.6%**
- Residuo: circa 47.7h in circa 13 settimane

**Anticipo sulla roadmap**: invariato, M4 target fine novembre, nessun consumo di buffer rilevato.

## Task pendenti - priorita per prossima sessione

1. **Cappello Developer**: M4.4 - estrarre/creare segmento denso (5 reeds simultanei) da `kronos_kai_kairos.musicxml` (file completo), o sorgente alternativa se piu adatta
2. **Cappello Developer**: validare split 2+3 su 5 voci con dual-gate numerico + Dorico sul nuovo segmento
3. **Cappello QA**: espandere pytest per il caso 5-voci (oltre ai 2 test M4.3 single-voice)
4. Attenzione R15 (scope creep): M4.4 resta "split 2+3 base", non introduce logica di ranking/priorita avanzata senza CR

## Rischi aperti - priorita

- R15 (scope creep): disciplina Change Request obbligatoria, invariato
- **R31 (Mitigato 18/10)**: dual-gate numerico totale+visibile obbligatorio prima del gate Dorico
- **R32 (Mitigato 18/10)**: music21 writer print-object quirk, mitigato via sanitizer - ATTENZIONE: il sanitizer e' indiscriminato (rimuove print-object="no" da OGNI Rest), da raffinare se in futuro servono multi-measure rest simbolici legittimamente nascosti
- R30 (music21.write corruption): MITIGATO, invariato da M3
- R01 (produttivita): monitoraggio positivo, invariato

## Repository stato

- 23 commit pubblici (12-18 ottobre)
- 6 tag milestone: M1-initiation, M2-feasibility, M3-production, M4.2-measures, M4.2-visual-fix, M4.3-passthrough
- Nuovi moduli: `musicxml_sanitizer.py`, `scripts/preview_single_voice.py`, script diagnostici (`diagnose_measure_durations.py`, `diagnose_visible_durations.py`, `probe_skeleton.py`, `probe_pipeline.py`)
- 19/19 test su `test_condenser_reeds.py` GREEN (52 totali progetto, nessuna regressione)
- Documentazione PMI allineata: Risk Register v0.6, WBS_M4 v0.2, CHANGE_LOG v0.9

## Prossimo passo consigliato

**Cappello Developer** per M4.4: creare/estrarre il segmento denso a 5 voci reeds, poi implementare e validare split 2+3 con dual-gate. Durata stimata prossima sessione: 1h30-2h (estrazione + implementazione + dual-gate + Dorico).

## Debito tipografico PDF

Rinviato a refresh pre-tesi CAPM. Zero impatto operativo.
