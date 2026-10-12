---
document: Project Scoping Summary
project: Big Band Condenser v1
version: 1.0
status: Baseline for Initiation Phase
created: 2026-10-12
owner: Sponsor/PM
---

# Big Band Condenser v1 — Project Scoping Summary

Questo documento consolida le decisioni prese durante la fase di scoping del
12 ottobre 2026. Serve come input autoritativo per la fase di Initiating
operativa che partirà in una nuova sessione di lavoro.

## 1. Natura del progetto

Big Band Condenser v1 è un tool open source che trasforma automaticamente
una partitura big band in formato MusicXML in una condensed score (particella
analitica) in formato MusicXML strutturata in 4 sistemi:

- Sistema 1 — Reeds (doppio pentagramma, concert pitch)
- Sistema 2 — Brass (doppio pentagramma, concert pitch)
- Sistema 3 — Rhythm section melodica (doppio pentagramma, con chord symbols)
- Sistema 4 — Drum set (pentagramma singolo con slash e rhythmic notation)

Il progetto è autodiretto, part-time, con triplice obiettivo:
esercitazione CAPM applicata, costruzione di uno strumento utile all'autore,
contributo alla community open source.

## 2. Scope v1

### In scope

- Pipeline Python che legge MusicXML big band, produce MusicXML condensed
- Trasposizione automatica in concert pitch
- Preservazione completa delle note (nessuna persa)
- Preservazione di dinamiche, accenti, legature, articolazioni, text directions
- Discriminazione automatica comping vs shout sul rigo Rhythm
- Estrazione chord symbols dalla parte piano/chitarra e riposizionamento sul rigo Rhythm
- Preservazione parte batteria con slash notation, rhythmic notation, text directions
- Validità MusicXML W3C e compatibilità Dorico
- CLI invocabile
- Repository pubblico GitHub con documentazione tecnica e PMI completa

### Out of scope v1

- Conversione PDF to MusicXML (responsabilità utente, usa OMR esterno)
- Analisi funzionale con numeri romani
- Box analitici, frecce motiviche, annotazioni didattiche
- Cross-reference automatiche tra sistemi
- Generazione automatica kick-overs batteria
- Suonabilità pianistica dell'output
- Interfaccia web o UI grafica
- Repertorio non big band jazz
- Materiale sotto copyright nel corpus di test pubblico

### Roadmap future phases

- Fase B — Web Interface
- Fase C — OMR Integration
- Fase D — Analisi musicale automatica
- Fase E — Generazione automatica kick-overs batteria

## 3. Vincoli e assunzioni chiave

### Vincoli

- Deadline target: 31 gennaio 2027 (15 settimane calendario da oggi)
- Budget massimo: 200 EUR totali, stimati ~75 EUR effettivi
- Monte ore baseline: 5h/settimana + buffer flessibile
- Monte ore totale stimato: 60 ore
- Stack obbligato: Python 3.11+, music21, Pydantic, VSCode, Pandoc, Git, Dorico 5+
- Repertorio di test pubblico: solo composizioni dello Sponsor o pubblico dominio
- Reference artifact privato di terzi: uso interno esclusivo, non versionato nel repo

### Assunzioni da verificare nelle prime 2 settimane

- La produttività dimostrata dallo Sponsor su progetto BigBand AI (30h per output
  complesso) è trasferibile al Condenser
- `shared/models.py` di BigBand AI riusabile senza refactoring sostanziale
- `knowledge/chord_scales.py` di BigBand AI riusa parser jazz standalone
- `dorico_bridge/` di BigBand AI compatibile con versione Dorico installata
- music21 supporta tutte le feature MusicXML necessarie
- OMR esterno (es. PhotoScore, Audiveris) produce MusicXML sufficientemente
  pulito per uso downstream

## 4. Architettura di lavoro

### Setup Claude

- Claude Pro web, 20 USD/mese
- Un Claude Project dedicato al Big Band Condenser come memoria persistente
- Documenti PMI caricati nel Project come knowledge base
- Reference artifact privato caricato nel Project per uso interno (non pubblicato)

### Workflow operativo

Role-switching in single-chat: ogni sessione dichiara apertamente il ruolo
funzionale attivo (Business Analyst, Tech Lead, Developer, QA, Music Expert,
Researcher, Doc Writer, Risk Officer). Claude adatta la risposta al focus
del ruolo dichiarato. Zero chat multiple parallele.

### Persistenza tra sessioni

- `STATUS.md` aggiornato alla fine di ogni sessione di lavoro
- `CHANGE_LOG.md` tracciamento decisioni di alto livello
- Git commit frequenti con messaggi descrittivi
- Version block in testa a ogni documento Markdown
- PDF di release generati ai milestone con Pandoc

### Esecuzione tecnica

- IDE: VSCode con terminale integrato
- Copy/paste tra Claude web e VSCode per codice e output
- Comandi, test, build, git lanciati dallo Sponsor da VSCode terminal
- Nessuna automazione di esecuzione autonoma lato Claude

## 5. Riuso da progetto BigBand AI

Progetto donatore in read-only. Nessuna modifica senza Change Request formale
in quel progetto.

### Componenti riusabili v1

- `backend/dorico_bridge/` — client WebSocket Dorico (riuso diretto, cruciale)
- `backend/knowledge/chord_scales.py` — parser chord symbols jazz (riuso parziale)
- `backend/shared/models.py` — da verificare se generico (assunzione)
- Pattern di validator interpretabili con metriche separate (meta-riuso)
- Pattern di documentazione modulare (meta-riuso)
- Stack tecnico identico (Python 3.11+, music21, Pydantic)

### Componenti da costruire ex novo

1. MusicXML Score Parser (lettura partitura big band completa)
2. Instrument Classifier (strumento to sezione)
3. Concert Pitch Transposer
4. Section Condenser Engine (cuore del progetto)
5. Comping vs Shout Detector
6. Chord Symbol Extractor
7. Drum Part Preserver
8. MusicXML Score Writer (output condensed)
9. Validators con metriche separate
10. CLI

## 6. Lingua documentale

Scelta asimmetrica:

- Documenti PMI formali (Charter, Stakeholder Register, Risk Register, WBS,
  Change Log, Lessons Learned, Communication Plan, Change Control Plan):
  in italiano, per riuso in tesi
- Documenti public-facing del repo (README, CONTRIBUTING, ARCHITECTURE,
  CHANGELOG tecnico): in inglese, per visibilità open source internazionale
- Un README.it.md aggiuntivo per lettori italiani del repo

## 7. Stakeholder identificati

- Sponsor (lo Sponsor/PM/Developer in uno solo)
- Project Manager (stesso individuo, cappello diverso)
- Developer utilizzatore futuro del tool (stesso individuo)
- Ruoli funzionali del team: Business Analyst, Tech Lead, Developer, QA,
  Music Expert, Researcher, Doc Writer, Risk Officer (attivati come
  contesti di lavoro in Claude)
- Utenti futuri open source: arrangiatori, studenti jazz, direttori di big band
- Community Python open source: potenziali contributori
- music21 maintainers: dependency maintainer
- Steinberg Dorico: piattaforma target per import MusicXML
- Comunità PMI/CAPM: potenziale pubblico di studio metodologico

## 8. Milestone principali

- M1 — Project Initiation Baseline: Charter, Stakeholder Register, Risk Register
  depositati nel repo (prima sessione di lavoro operativa)
- M2 — Feasibility Spike completato: prototipo minimale su MusicXML tuo
- M3 — Parser MusicXML + Classificatore strumenti funzionanti
- M4 — Section Condenser Engine funzionante su una sezione
- M5 — Pipeline end-to-end su un brano test
- M6 — Comping/shout + chord symbols + drums completati
- M7 — Validator + test suite completati
- M8 — CLI + documentazione utente + esempi completati
- M9 — Documentazione PMI finale + release v1.0.0

Target completamento M9: 31 gennaio 2027.

## 9. Decisioni di documentazione e versioning

- Working documents in Markdown dentro `docs/pmi/`
- Git come storico ufficiale delle versioni
- Version block in testa ai documenti per leggibilità umana
- PDF generati con Pandoc ai milestone, salvati in `docs/pmi/releases/`
- Repo pubblico GitHub
- Licenza open source: candidate MIT o Apache 2.0, decisione in M1

## 10. Priorità operative immediate per la prossima sessione

1. Creare il repository `bigband-condenser` in locale e su GitHub
2. Setup ambiente: Python venv, music21, pytest, Pandoc, MiKTeX se mancanti
3. Produrre Charter v0.3, Stakeholder Register v0.1, Risk Register v0.1
4. Primo commit e tag `M1-initiation`
5. Pianificare feasibility spike (settimana 2) con un tuo MusicXML di test

## 11. Elementi di scoping ancora da chiudere

Da affrontare nelle prossime sessioni operative:

- Verifica compatibilità `shared/models.py` da BigBand AI (prima sessione)
- Scelta licenza open source definitiva (M1)
- Communication Plan e Change Control Plan dettagliati (dopo M1)
- WBS dettagliata con stime per task (dopo M1)
- Matrice RACI con mappatura ruoli-task (dopo M1)
- Quality Management Plan (durante M2)
- Benefit Realization Plan (opzionale, per esercizio CAPM completo)

---

Fine scoping. La fase di Initiating operativa parte dalla prossima sessione.
