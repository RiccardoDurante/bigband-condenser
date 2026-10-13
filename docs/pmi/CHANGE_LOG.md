---
document: Change Log
document_id: CL-BBC-001
project: Big Band Condenser v1
version: 0.4
status: Active
last_updated: 2026-10-13
language: it
changelog:
  - v0.4 (2026-10-13): aggiunta D-016 (passaggio repo a visibilita pubblica, chiude D-014 in modalita completamento)
  - v0.3 (2026-10-13): aggiunta D-015 (creazione Roles Register come placeholder minimalista, bump a v0.2 completo dopo WBS)
  - v0.2 (2026-10-12): aggiunte D-013 (licenza MIT formalizzata) e D-014 (repo GitHub privato in Initiating, pubblico a M1 completato) prese nella sessione di setup del 12/10/2026
  - v0.1 (2026-10-12): scheletro con decisioni di avvio
---

# Change Log - Big Band Condenser v1

Registro delle decisioni di alto livello e delle Change Request. Non sostituisce la cronologia Git: ci vanno solo eventi significativi per scope, tempi, costi, rischi, architettura.

## Formato di una Change Request

## Decisioni di avvio (fase di scoping, 11-12 ottobre 2026)

| ID | Data | Decisione | Motivazione | Documenti |
|---|---|---|---|---|
| D-001 | 2026-10-11 | Nuovo progetto Big Band Condenser (riduzione), distinto da BigBand AI Assistant (generazione) | Problemi diversi; BigBand AI resta progetto donatore | Charter |
| D-002 | 2026-10-11 | Dominio: big band jazz, 4 sistemi (Reeds, Brass, Rhythm, Drums) in concert pitch | Organico ristretto e convenzioni definite dal reference dello Sponsor | Charter, Scope Statement |
| D-003 | 2026-10-11 | Annotazioni analitiche (numeri romani, box, frecce) fuori scope | Valore aggiunto manuale dello Sponsor, non requisito del tool | Charter |
| D-004 | 2026-10-11 | Interfaccia web rimandata a fase futura | Progetto a se, con costi e responsabilita operative | Charter (roadmap) |
| D-005 | 2026-10-12 | Repository separato ``bigband-condenser``; BigBand AI in sola lettura | Separazione netta delle responsabilita | Charter |
| D-006 | 2026-10-12 | Input solo MusicXML; OMR a carico dell'utente | Evitare un sotto-progetto di ricerca aperta | Charter |
| D-007 | 2026-10-12 | Reference di terzi solo ad uso privato, fuori dal repository | Vincolo di copyright; test pubblici con materiale proprio o di pubblico dominio | Charter, Risk Register |
| D-008 | 2026-10-12 | Documentazione: Markdown + Git + PDF ai milestone | Tracciabilita senza overhead | Charter |
| D-009 | 2026-10-12 | Lingua: documenti PMI in italiano; README, architettura e codice in inglese | Riuso nella tesi e leggibilita internazionale | Charter |
| D-010 | 2026-10-12 | Vincoli: deadline 31/01/2027, budget 200 EUR, 5 ore/settimana, sforzo stimato 60 ore | Dati forniti dallo Sponsor; stima da verificare con lo spike | Charter |
| D-011 | 2026-10-12 | Modello di lavoro: Claude Pro, ruoli funzionali dichiarati a inizio sessione, esecuzione tecnica in VS Code | Compatibile con budget e con la pratica gia consolidata | Charter |
| D-012 | 2026-10-12 | Generazione dei PDF come primo task in VS Code | Baseline documentale formale | Charter |
| D-013 | 2026-10-12 | Licenza open source: MIT | Semplicita, standard de facto per tool Python di nicchia, allineata con ecosistema (music21 BSD, Pydantic MIT); decisione presa in sessione di setup iniziale M1 | Charter v0.4 (sezione 5), file LICENSE nel repository root |
| D-014 | 2026-10-12 | Repository GitHub ``RiccardoDurante/bigband-condenser`` privato in fase di Initiating, passaggio a pubblico a M1 completato | Minore pressione in fase di setup; zero rischio di push accidentali di materiale non pronto (incluso reference artifact privato di terzi); passaggio privato -> pubblico e reversibile mentre il contrario non lo e | README.md (status pre-release), README.it.md |
| D-015 | 2026-10-13 | Creazione Roles Register (``docs/pmi/ROLES.md``) come placeholder minimalista v0.1, con 8 ruoli funzionali e definizione "cosa fa / cosa non fa" per ciascuno; bump a v0.2 completo rimandato post-WBS | Role ambiguity prevista come rischio operativo del role-switching single-chat: senza definizione esplicita dei confini di ruolo, derive progressive nelle sessioni successive. Scelto formato minimalista perche la RACI completa richiede WBS come prerequisito (PROJECT_SCOPING_SUMMARY sezione 11) | ROLES.md v0.1 |
| D-016 | 2026-10-13 | Passaggio repository da privato a pubblico (chiude D-014 come completata). URL pubblica: https://github.com/RiccardoDurante/bigband-condenser | M1 Baseline completato (Charter, Stakeholder Register, Risk Register, ROLES, Change Log, README, 6 PDF di release); scoping summary sezione 2 e 9 prevedevano repo pubblico come deliverable; coerenza con triplice obiettivo del progetto (esercitazione CAPM, utilita personale, contributo open source) | README.md (aggiornare sezione Contributing per rimuovere nota "repository currently private"), scoping summary allineato |

## Change Request

_Nessuna al momento._
