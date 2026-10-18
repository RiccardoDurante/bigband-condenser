---
document: Change Log
document_id: CL-BBC-001
project: Big Band Condenser v1
version: 0.9
status: Active
last_updated: 2026-10-18
language: it
changelog:
  - v0.9 (2026-10-18): aggiunte D-028 (M4.1-M4.3 chiusi, R31 formalizzato, R32 scoperto e mitigato via sanitizer), D-029 (decisione scope M4.4: segmento denso dedicato per split 2+3 su 5 voci reeds)
  - v0.8 (2026-10-16): aggiunte D-025 (M3 production code Fase 1 shipped - 4 moduli production + pytest baseline 35 test green), D-026 (errata SPIKE_M2_REPORT v0.2 count parti), D-027 (M3 chiuso con tag M3-production)
  - v0.7 (2026-10-15): D-020 Kronos committato, D-021 Risk Register v0.4, D-022 principio notazione vs playback, D-023 Spike M2 implementato, D-024 Spike M2 chiuso PASS
  - v0.6 (2026-10-14): D-019 piano operativo Spike M2
  - v0.5 (2026-10-14): D-017 verifica assunzioni, D-018 Risk Register v0.3
  - v0.4 (2026-10-13): D-016 repo pubblico
  - v0.3 (2026-10-13): D-015 Roles Register
  - v0.2 (2026-10-12): D-013 MIT, D-014 repo privato pre-M1
  - v0.1 (2026-10-12): scheletro
---

# Change Log - Big Band Condenser v1

## Formato Change Request

## Decisioni

| ID | Data | Decisione | Motivazione | Documenti |
|---|---|---|---|---|
| D-001 | 2026-10-11 | Nuovo progetto Big Band Condenser distinto da BigBand AI | Problemi diversi | Charter |
| D-002 | 2026-10-11 | Dominio big band jazz 4 sistemi concert pitch | Organico definito | Charter |
| D-003 | 2026-10-11 | Annotazioni analitiche fuori scope | Valore manuale | Charter |
| D-004 | 2026-10-11 | Web interface rimandata | Fase futura | Charter |
| D-005 | 2026-10-12 | Repo separato, BigBand AI read-only | Separazione | Charter |
| D-006 | 2026-10-12 | Input solo MusicXML, OMR a utente | Evitare sotto-progetto | Charter |
| D-007 | 2026-10-12 | Reference terzi solo privato | Copyright | Charter |
| D-008 | 2026-10-12 | Markdown + Git + PDF milestone | Tracciabilita | Charter |
| D-009 | 2026-10-12 | PMI italiano, README inglese | Riuso tesi | Charter |
| D-010 | 2026-10-12 | Deadline 31/01/2027, 200 EUR, 60h | Sponsor | Charter |
| D-011 | 2026-10-12 | Claude Pro + VS Code + role-switching | Budget | Charter |
| D-012 | 2026-10-12 | PDF generation primo task | Baseline | Charter |
| D-013 | 2026-10-12 | Licenza MIT | Standard | LICENSE |
| D-014 | 2026-10-12 | Repo privato in Initiating | Setup pressure-free | README |
| D-015 | 2026-10-13 | Roles Register placeholder | Role ambiguity | ROLES.md |
| D-016 | 2026-10-13 | Repo pubblico, chiude D-014 | M1 completato | README |
| D-017 | 2026-10-14 | Verifica assunzioni A2/A3/A4 | Saving 12.5-19h | BIGBAND_AI_REUSE_ASSESSMENT.md |
| D-018 | 2026-10-14 | Risk Register v0.3 | Verifica positiva | Risk Register v0.3 |
| D-019 | 2026-10-14 | Piano Spike M2 Kronos | Charter sez. 6 | SPIKE_M2_PLAN.md |
| D-020 | 2026-10-14 | Kronos full + extract committati | Charter 12.2 | samples/, FINDINGS v0.2 |
| D-021 | 2026-10-14 | Risk Register v0.4 (R07/R12 Materializzati, R26/R27 nuovi) | Verifica cloud | Risk Register v0.4 |
| D-022 | 2026-10-15 | Principio notazione scritta vs playback MIDI | Music Expert | SPIKE_M2_REPORT sez. 4 |
| D-023 | 2026-10-15 | Spike M2 implementato Q1-Q6, Risk Register v0.5 | Spike produce rischi | Risk Register v0.5, SPIKE_M2_REPORT |
| D-024 | 2026-10-15 | Spike M2 CHIUSO PASS, decisione D-A procedi M3 | S1+S2+S3 soddisfatti | tag M2-feasibility |
| D-025 | 2026-10-16 | M3 Fase 1 shipped: 4 moduli production (models.py, instrument_mapping.py, classifier.py, preprocessor.py) + writer.py + pytest baseline 35 test green. Preprocessor orchestra 3 mitigation Spike M2 (R27 filter sub-semicroma, R28 strip hidden, R30 force instrument class). End-to-end validated su Kronos extract: 1 hidden stripped, 18 classes forced, 157 sub-semicroma filtered, music21.write SUCCESS 565 KB | Charter sezione 6 M3 target meta novembre: anticipo di 1 mese sulla roadmap. Pattern pipeline singola (no dual) confermato come architettura v1. Writer con diagnostica R27 (hint "chiamare preprocess") per DX | src/bigband_condenser/*.py, tests/*.py |
| D-026 | 2026-10-16 | Errata SPIKE_M2_REPORT v0.2: count parti 18 XML vs 19 music21 iter (Piano grand-staff). Risultato logico 17 strumenti visible invariato | Scoperta durante porting Q2 a classifier production (ElementTree vs music21.score.parts) | SPIKE_M2_REPORT v0.2 sezione 13 |
| D-027 | 2026-10-16 | M3 CHIUSO con tag M3-production. Monte ore M3 effettivo: circa 2h. Scope M4 (condensation logic di 1 sezione) target fine novembre, 6-8h stimate | Deliverable M3: 4 moduli production + writer + pytest 35 test. Tutte mitigation Spike M2 attive. Deadline 31/01/2027 con buffer accumulato di circa 2 settimane | tag M3-production, STATUS.md |

| D-028 | 2026-10-18 | M4.1 (metadata), M4.2 (measure structure) e M4.3 (single-voice passthrough) completati. Durante gate visivo M4.2 scoperto bug critico: 32/66 misure visivamente corte nonostante durata XML totale corretta (causa music21 v10.5 writer, print-object="no" spurio su Rest in Measure). Fix: musicxml_sanitizer.py post-write. R31 formalizzato (dual-gate numerico totale+visibile obbligatorio prima del gate Dorico), R32 nuovo (music21 writer quirk, mitigato). Risk Register v0.6 | Gate numerico da solo non basta a validare notazione; lezione di metodo per tutti i sotto-step M4 restanti | Risk Register v0.6, WBS_M4.md, tag M4.2-measures/M4.2-visual-fix/M4.3-passthrough |
| D-029 | 2026-10-18 | M4.4 scope: split 2+3 su 5 voci reeds, da validare su nuovo segmento denso (tutti i 5 reeds attivi simultaneamente, es. shout chorus/tutti) invece di riuso diretto di kronos_kai_kairos_extract.musicxml | extract esistente non garantisce onset complessi/incroci di voce necessari a stressare la logica di split; segmento dedicato isola meglio eventuali bug dallo split stesso | WBS_M4.md (M4.4 scope, pending estrazione) |

## Change Request

_Nessuna al momento._
