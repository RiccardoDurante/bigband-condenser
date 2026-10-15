---
document: Change Log
document_id: CL-BBC-001
project: Big Band Condenser v1
version: 0.7
status: Active
last_updated: 2026-10-15
language: it
changelog:
  - v0.7 (2026-10-15): aggiunte D-020 (Kronos committato), D-021 (Risk Register v0.4), D-022 (principio notazione vs playback), D-023 (Spike M2 implementato Q1-Q6 con 5/6 PASS + 1 productive FAIL, Risk Register v0.5 con R27 downgraded + R28/R29/R30 nuovi), D-024 (Spike M2 chiuso PASS, decisione formale D-A procedi M3 come pianificato)
  - v0.6 (2026-10-14): D-019 piano operativo Spike M2 con Kronos test case
  - v0.5 (2026-10-14): D-017 verifica assunzioni A2/A3/A4, D-018 Risk Register v0.3
  - v0.4 (2026-10-13): D-016 passaggio repo pubblico
  - v0.3 (2026-10-13): D-015 Roles Register minimalista
  - v0.2 (2026-10-12): D-013 licenza MIT, D-014 repo privato pre-M1
  - v0.1 (2026-10-12): scheletro
---

# Change Log - Big Band Condenser v1

## Formato Change Request

## Decisioni

| ID | Data | Decisione | Motivazione | Documenti |
|---|---|---|---|---|
| D-001 | 2026-10-11 | Nuovo progetto Big Band Condenser distinto da BigBand AI | Problemi diversi | Charter |
| D-002 | 2026-10-11 | Dominio big band jazz 4 sistemi concert pitch | Organico definito | Charter |
| D-003 | 2026-10-11 | Annotazioni analitiche fuori scope | Valore manuale Sponsor | Charter |
| D-004 | 2026-10-11 | Web interface rimandata | Fase futura | Charter |
| D-005 | 2026-10-12 | Repo separato, BigBand AI read-only | Separazione | Charter |
| D-006 | 2026-10-12 | Input solo MusicXML, OMR a carico utente | Evitare sotto-progetto | Charter |
| D-007 | 2026-10-12 | Reference terzi solo privato | Copyright | Charter |
| D-008 | 2026-10-12 | Markdown + Git + PDF milestone | Tracciabilita | Charter |
| D-009 | 2026-10-12 | Lingua: PMI italiano, README inglese | Riuso tesi | Charter |
| D-010 | 2026-10-12 | Deadline 31/01/2027, 200 EUR, 60h | Sponsor | Charter |
| D-011 | 2026-10-12 | Claude Pro + VS Code + role-switching | Budget-compatible | Charter |
| D-012 | 2026-10-12 | PDF generation primo task VS Code | Baseline | Charter |
| D-013 | 2026-10-12 | Licenza MIT | Standard tool Python | LICENSE |
| D-014 | 2026-10-12 | Repo privato in Initiating, pubblico a M1 | Minore pressione setup | README |
| D-015 | 2026-10-13 | Roles Register placeholder minimalista v0.1 | Role ambiguity prevention | ROLES.md |
| D-016 | 2026-10-13 | Passaggio repo a pubblico, chiude D-014 | M1 completato | README |
| D-017 | 2026-10-14 | Verifica assunzioni A2/A3/A4 completata | Saving 12.5-19h validato | BIGBAND_AI_REUSE_ASSESSMENT.md |
| D-018 | 2026-10-14 | Risk Register v0.3 (R04/R05 Non materializzato, R06 Non applicabile, R24 nuovo) | Verifica assunzioni positiva | Risk Register v0.3 |
| D-019 | 2026-10-14 | Piano operativo Spike M2 con Kronos CC-BY 4.0, timebox 12h, 6 Q | Charter sezione 6 M2 | SPIKE_M2_PLAN.md v0.1 |
| D-020 | 2026-10-14 | Committati nel repo pubblico: ``samples/kronos_kai_kairos.musicxml`` (full 6min, 142 battute, 19 parti XML, Finale v27.4 export) e ``samples/kronos_kai_kairos_extract.musicxml`` (pickup 0 + bars 1-32, 716 KB, prodotto via XML manipulation diretta per aggirare music21.write fail su durate drum 2048th). Licenza CC-BY 4.0 Riccardo Durante. Scoperte preliminari cloud: Q1 PASS, Q2 PASS 19/19 via partName, Q3 PASS 6/6 traspositori, Q5 source side OK | Charter sezione 12.2 (corpus test = composizioni Sponsor). Alternative scartate (Schneider copyright, standard jazz quasi tutti protetti). Kronos risolve legalmente pulito e testa organico non canonico (soprano sax + 2 corni F) | samples/, KRONOS_KAI_KAIROS_FINDINGS.md v0.2 |
| D-021 | 2026-10-14 | Risk Register v0.4: R07 (music21 drum fail) e R12 (export Finale non Dorico) passati a "Materializzato" con evidenza empirica. Aggiunti R26 (music21 instrument class detection inaffidabile su export Finale, 19/19 Kronos misclassificati, score 6 alta priorita) e R27 (music21.write fallisce su durate drum sub-32th tipiche Finale, score 9 CRITICAL) | Il Risk Register vive per definizione: i rischi vanno aggiornati quando emergono dati nuovi dalla verifica cloud preliminare | Risk Register v0.4, KRONOS_KAI_KAIROS_FINDINGS.md |
| D-022 | 2026-10-15 | Principio operativo "notazione scritta vs playback MIDI". Il Condenser v1 opera sulla notazione intenzionale del compositore, non sui dati di realistic playback MIDI aggiunti dal software source (Finale realistic playback, humanization, risonanze template Garritan/EWQL). Soglia operativa: durate < 0.25 quarterLength (sotto semicroma) nelle drum parts sono considerate playback artifacts e scartate pre-write | Input esplicito dello Sponsor/Music Expert nel ruolo di dominio durante Spike M2 Q4: "io vorrei che ti attenessi ai valori delle note scritte effettivamente, non mi interessa l'esecuzione". Validato empiricamente: grace tag count = 0 nel source (artefatti standalone non grace notes legittime). Impatto: R27 downgradato da critico (score 9) a medio (score 4), mitigazione semplificata | SPIKE_M2_REPORT.md sezione 4, Risk Register v0.5 |
| D-023 | 2026-10-15 | Spike M2 implementato Q1-Q6 (5 moduli Python, ~1300 righe totali di codice test). Risultati: Q1 PASS parse integrity, Q2 PASS 19/19 classify via partName + hidden detection validata, Q3 PASS 17/17 trasposizioni, Q4 PASS via strip-hidden + filter-sub-semicroma, Q5 FAIL 1/16 productive (scoperta R30), Q6 PASS 4-pentagrammi structure skeleton. Bump Risk Register v0.5 con R27 downgraded + R28 (hidden parts detection, score 4), R29 (octave-transposing conventions, score 1), R30 (music21.write output corruption da wrong class, score 9 CRITICAL) | Spike M2 ha fatto il suo mestiere: ha trovato 3 nuovi rischi (di cui 1 critico), ha validato 2 mitigazioni, ha definito strategia architetturale output | Risk Register v0.5, SPIKE_M2_REPORT.md v0.1 |
| D-024 | 2026-10-15 | Spike M2 CHIUSO con verdetto PASS (criteri successo S1+S2+S3 tutti soddisfatti). Decisione formale: **D-A - procedi con M3 come pianificato nel Charter sezione 6, nessuna ricalibrazione necessaria**. Tag git M2-feasibility sul commit di chiusura. Monte ore M2 effettivo: ~1h40 (vs 12h timebox del piano) grazie al valore enorme del preliminary cloud spike (14 ott) che ha accelerato il locale (15 ott). Residuo monte ore cumulato: ~51h su 60h, pace sotto baseline 5h/sett, deadline 31/01/2027 raggiungibile con margine ragionevole | Charter sezione 6 target M2 "fine ottobre" rispettato con 15 giorni di anticipo. Scoperte critiche R27 downgraded + R30 nuova mitigation definita. Base solida per M3 (Parser + Classifier production code) | SPIKE_M2_REPORT.md v0.1, STATUS.md, tag M2-feasibility |

## Change Request

_Nessuna al momento._
