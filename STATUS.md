---
document: Project Status
project: Big Band Condenser v1
updated: 2026-10-16 11:35 (CEST)
session: 2026-10-16 (M3 Fase 1+2 production code + pytest baseline + writer + docs + tag M3-production)
---

# Project Status

## Milestone corrente

**M1 - Project Initiation Baseline**: COMPLETATO (tag ``M1-initiation``)
**M2 - Spike di fattibilita**: COMPLETATO (tag ``M2-feasibility``, verdetto PASS)
**M3 - Parser + Classificatore production code**: **COMPLETATO** (tag ``M3-production``)
**M4 - Condensatore di sezione funzionante**: PROSSIMO (target fine novembre 2026)

## Task completati nelle sessioni 12-16 ottobre

Vedi sessioni precedenti per M1 e M2. Sessione 2026-10-16 (M3 chiusura, circa 2h):

### M3 Fase 1 - Core production code (circa 1h)

- ``src/bigband_condenser/models.py``: NoteData, MelodyData (copia selettiva BigBand AI)
- ``src/bigband_condenser/instrument_mapping.py``: 40+ partName -> (semitones, music21 class) con lookup exact-match + substring fallback
- ``src/bigband_condenser/classifier.py``: classify_section + detect_hidden_part_names + classify_score + summarize
- ``src/bigband_condenser/preprocessor.py``: orchestra strip hidden + force class + filter drums (3 mitigation Spike M2)
- End-to-end validation su Kronos extract: music21.write() SUCCESS 565 KB
- Scoperta: classifier production conta 18 XML parts (vs 19 music21 iter per split Piano grand-staff)

### M3 Fase 2 - QA + Writer (circa 50 min)

- ``tests/conftest.py`` + ``tests/test_classifier.py`` + ``tests/test_instrument_mapping.py`` + ``tests/test_preprocessor.py`` + ``tests/test_writer.py``
- 35 test totali, tutti GREEN in 4.3 secondi
- ``src/bigband_condenser/writer.py``: wrapper music21.write() con diagnostic R27 (hint preprocess) + verify re-parse

### M3 Fase 3 - Docs (circa 20 min)

- SPIKE_M2_REPORT v0.2 con sezione 13 Errata (18 vs 19 parts)
- CHANGE_LOG v0.8 con D-025, D-026, D-027
- STATUS.md aggiornato

### M3 Fase 4 - Chiusura

- Tag ``M3-production`` sul commit finale
- Monte ore cumulato: circa 12h su 60h totali

## Spike M2 - Esito finale (archivio)

**PASS**. S1+S2+S3 soddisfatti. Decisione D-A procedi M3 come pianificato (ora completato).

## Monte ore consumato

- 12 ottobre (M1 baseline): circa 2h40
- 13 ottobre (PDF pipeline + repo public): circa 1h50
- 14 ottobre (M2 fase A-E): circa 3h25
- 15 ottobre (M2 fase F+G chiusura): circa 1h15
- 16 ottobre (M3 completo): circa 2h

**Totale cumulato**: circa 11h10 su 60h = **18.6%**
Residuo: circa 48.9h in circa 13 settimane (3.7h/sett sotto baseline).

**Anticipo sulla roadmap**: M3 era target meta novembre, chiuso il 16 ottobre. Circa 4 settimane di buffer accumulato.

## Task pendenti - priorita per M4

1. **Cappello Tech Lead**: review architetturale di M4 - come implementare condensation logic di 1 sezione
2. **Cappello Developer**: ``src/bigband_condenser/condenser/`` package con un modulo per sezione (reeds_condenser, brass_condenser, rhythm_condenser, drums_condenser)
3. **Cappello Developer**: iniziare da Reeds (sezione piu simmetrica, 5 strumenti stesso famiglia)
4. **Cappello QA**: pytest expansion per i nuovi moduli condensation
5. **Target M4**: fine novembre 2026, 6-8h stimate

Attenzione: **il buffer accumulato non va bruciato in scope creep (R15)**. Va preservato per M5-M6 (condensation logic ha iterazioni musicologiche imprevedibili).

## Rischi aperti - priorita

- R15 (scope creep): disciplina Change Request obbligatoria
- **R30 (music21.write corruption)**: **MITIGATO** via force_instrument_classes in preprocessor.py, validato in pytest (test_bass_class_corrected)
- R27, R28: mitigati via preprocessor
- R01 (produttivita): monitoraggio positivo (anticipo roadmap)
- R07, R12, R16, R26: mitigation attive

## Repository stato

- 17 commit pubblici (12-16 ottobre)
- 3 tag milestone: M1-initiation, M2-feasibility, M3-production
- 4 moduli production + 5 moduli test
- 35 test automatici GREEN
- Documentazione PMI completa e allineata

## Prossimo passo consigliato

**Cappello Tech Lead** per M4 architettura condenser di sezione. Durata stimata prossima sessione: 1h30-2h.

## Debito tipografico PDF

Rinviato a refresh pre-tesi CAPM. Zero impatto operativo.
