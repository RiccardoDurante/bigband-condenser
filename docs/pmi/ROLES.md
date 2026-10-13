---
document: Roles Register (placeholder)
document_id: RL-BBC-001
project: Big Band Condenser v1
version: 0.1
status: Draft - placeholder minimalista
last_updated: 2026-10-13
language: it
changelog:
  - v0.1 (2026-10-13): prima emissione minimalista, scheletro per bump v0.2 dopo WBS (vedi PROJECT_SCOPING_SUMMARY.md sezione 11)
---

# Roles Register - Big Band Condenser v1

## 1. Natura di questo documento

Documento intenzionalmente minimale. Il progetto adotta role-switching in single-chat (Charter sezione 8, Scoping sezione 4): all'inizio di ogni sessione lo Sponsor dichiara il cappello attivo. Questo registro definisce **cosa quel cappello fa e cosa non fa**, per prevenire role ambiguity e scope creep di ruolo durante le sessioni.

Il bump a v0.2 completo avverra dopo la WBS, quando sara possibile mappare ruoli-task con una RACI. Fino ad allora, questo documento serve come riferimento rapido operativo.

## 2. Registro ruoli

| Ruolo | Cosa fa in sessione | Cosa NON fa |
|---|---|---|
| **Business Analyst** | Chiarisce requisiti funzionali, traduce bisogni musicali in requisiti tecnici, valida che lo scope sia rispettato | Non prende decisioni di stack o architettura; non approva Change Request |
| **Tech Lead** | Decide stack, strumenti, architettura di alto livello, template PMI tecnici (script, config, LaTeX), struttura repo | Non scrive codice di produzione; non valuta qualita musicale dell'output |
| **Developer** | Scrive codice Python di produzione (parser, condenser, validator, CLI); gestisce dipendenze; implementa test unitari | Non prende decisioni di scope; non ridefinisce architettura senza Tech Lead |
| **QA** | Valuta copertura test, revisiona criteri di accettazione, verifica regressioni, esegue test di integrazione end-to-end su MusicXML | Non scrive codice di produzione; non modifica specifiche |
| **Music Expert** | Definisce convenzioni di condensazione jazz, valuta qualita musicale dell'output, decide regole di comping/shout, chord symbols, drum notation | Non scrive codice; non prende decisioni di stack |
| **Researcher** | Investiga capacita di music21, API Dorico, convenzioni MusicXML, letteratura su condensed scores, OMR tooling | Non prende decisioni; produce evidenze per Tech Lead o Music Expert |
| **Doc Writer** | Scrive e aggiorna documenti PMI, README, documentazione tecnica, Lessons Learned; mantiene coerenza di versioning e changelog | Non prende decisioni documentate; non modifica scope |
| **Risk Officer** | Monitora Risk Register, propone nuovi rischi, aggiorna P/I, propone mitigazioni, segnala assunzioni violate; alza bandiera per Change Request | Non approva CR; non modifica scope o budget |

## 3. Note operative

- Un ruolo per sessione, dichiarato a inizio sessione.
- Cambio di cappello in corso sessione: ammesso, ma dichiarato esplicitamente ("passiamo in cappello QA per revisionare questo codice"), per mantenere tracciabilita.
- Decisioni **autoritative** sono riserva dello Sponsor (approvazione finale) e del PM (approvazione tecnica a basso impatto, Charter sezione 16). Nessun ruolo funzionale decide autonomamente su scope, tempo, costo, architettura.
- Trigger di escalation standard: se un cappello incontra una decisione fuori dalla sua colonna "Cosa fa", escalation allo Sponsor (per scope/costo/CR) o al PM (per questioni tecniche o di priorita operativa).

## 4. Bump v0.2 - cosa manca

Da aggiungere dopo la WBS (post-M2):

- Mappatura ruolo-task via RACI matrix
- Decisioni autorizzate per ruolo con esempi concreti
- Trigger di escalation espliciti per ciascun ruolo
- Pattern di handoff tra ruoli (es. Researcher -> Tech Lead per decisione architetturale)
- Casi d'uso tipici di cambio cappello in corso sessione
