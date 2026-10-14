---
document: BigBand AI Reuse Assessment
document_id: AR-BBC-001
project: Big Band Condenser v1
version: 0.1
status: Draft
last_updated: 2026-10-14
language: it
changelog:
  - v0.1 (2026-10-14): prima emissione dopo verifica assunzioni A2/A3/A4 Charter su codice BigBand AI
---

# BigBand AI Reuse Assessment

## 1. Scopo e metodo

Verifica delle assunzioni A2, A3, A4 del Charter sul riuso del codice del progetto donatore BigBand AI (``C:/Users/ricca/Projects/bigband-ai``). Metodo: lettura read-only del codice sorgente, nessuna modifica al progetto donatore (vincolo Charter sezione 12.5 e Risk Register R16).

Data della verifica: 14 ottobre 2026, sessione cappello Researcher.

Scala verdetti:

- **A** = Riusabile diretto (import e usa, nessuna modifica)
- **B** = Riusabile con copia selettiva (copia solo parti utili, con attribuzione)
- **C** = Riusabile come ispirazione (pattern valido, riscrittura necessaria)
- **D** = Non riusabile per v1 (meglio partire da zero o scope diverso)

## 2. Assunzione A2 - shared/models.py

**Target**: ``C:/Users/ricca/Projects/bigband-ai/backend/shared/models.py``

**Dimensione**: 22 righe effettive, 3 classi Pydantic.

**Classi presenti**:

| Classe | Scopo in BigBand AI | Riusabile per Condenser |
|---|---|---|
| ``NoteData`` | Nota concert pitch (pitch/duration/offset) | Si, generica |
| ``MelodyData`` | Sequenza di note con metadata source (key, time_sig, tempo, instrument, bar range) | Si, generica e con metadata source utili |
| ``WriteRequest`` | Richiesta scrittura in Dorico con flag confirmed | No, specifica al flusso generativo |

**Dipendenze esterne**: solo ``pydantic``. Nessuna dipendenza interna su altri moduli di BigBand AI. Classi stateless.

**Verdetto A2**: **B - Riusabile con copia selettiva**.

**Strategia**: copiare ``NoteData`` e ``MelodyData`` in ``src/bigband_condenser/models.py`` con header di attribuzione:

**Impatto monte ore**: saving concreto **4-6 ore** rispetto a scrittura da zero (catalogo basato su reference autoritativo + parser con fallback multi-notazione). L'assunzione A3 regge e supera le aspettative.

## 4. Assunzione A4 - dorico_bridge/

**Target**: ``C:/Users/ricca/Projects/bigband-ai/backend/dorico_bridge/``

**Struttura cartella** (file Python, ignorando ``__pycache__``):

| File | Dimensione | Ruolo |
|---|---|---|
| ``__init__.py`` | 413 B | Export API pubblica |
| ``client.py`` | 9267 B | Client WebSocket principale |
| ``commands.py`` | 4663 B | Comandi Dorico Remote Control |
| ``mock_server.py`` | 4175 B | Mock server per test offline |
| ``models.py`` | 1128 B | Modelli ConnectionState/DoricoCommand/DoricoResponse |
| ``musicxml_writer.py`` | 5734 B | **Writer MusicXML standalone (orfano organizzativo)** |
| ``score_reader.py`` | 6128 B | Lettore score da Dorico |
| ``score_writer.py`` | 5075 B | Scrittore score verso Dorico |

**Osservazione critica**: ``musicxml_writer.py`` non ha niente a che fare con Dorico Remote Control. E un **orfano con nome fuorviante**: zero import di ``client.py``, zero ``DoricoCommand``, usa solo stdlib + music21. L'organizzazione in ``dorico_bridge/`` e una scelta accidentale di BigBand AI, non un vincolo tecnico.

Il verdetto A4 va quindi scisso in due componenti distinti.

### 4.1 Bridge WebSocket vero (7 file su 8)

Comprende: ``client.py``, ``commands.py``, ``mock_server.py``, ``score_reader.py``, ``score_writer.py``, ``models.py``, ``__init__.py``.

**Analisi client.py** (il piu rilevante):
- Client WebSocket asyncio ben scritto
- Dipendenze: stdlib + ``websockets`` (lib terza, da aggiungere a ``pyproject.toml`` se usato) + ``backend.dorico_bridge.models`` (interno)
- Hard-coded defaults parametrizzati: ``host="127.0.0.1"``, ``port=4560``, ``client_name``
- Handshake con auto-retry su token stale
- Token persistiti in ``%APPDATA%/bigband-ai/session_token.json`` (path include "bigband-ai")
- Qualita codice alta (async pattern, context manager, error handling, logging)

**Verdetto 4.1**: **D - Non riusabile per v1**.

**Motivi**:
- Charter sezione 13 dice che il flusso primario e import manuale in Dorico; il bridge e "facoltativo"
- Richiederebbe test live con Dorico installato e Remote Control API attiva (dipendenza runtime fuori controllo)
- ~30 KB di codice specifico a un flusso fuori scope v1
- Zero valore per i deliverable v1
- Rischio R06 (dorico_bridge incompatibile) non si materializza perche semplicemente non useremo il bridge

### 4.2 musicxml_writer.py (orfano)

**Contenuto chiave**:

- ``_INSTRUMENT_TRANSPOSITIONS`` dict hard-coded con 13 strumenti big band standard (Alto Sax 1/2, Tenor Sax 1/2, Baritone Sax, 4 Trumpets, 3 Trombones, Bass Trombone) con semitoni esatti concert->written
- ``_M21_INSTRUMENT_MAP`` dict che mappa nomi stringa -> classi ``music21.instrument``
- ``_make_part`` funzione per creare Part music21 con instrument/key/time/tempo
- ``write_arrangement_to_musicxml`` funzione end-to-end: arrangements + durations -> MusicXML file
- ``_fix_missing_transpose_tags`` workaround XML post-processing per bug noto music21 (parti multiple stessa classe strumento omettono ``<transpose>``)

**Rilevanza per Condenser v1**:

- La tabella trasposizioni e esattamente quello che Charter sezione 3.3 richiede (concert pitch per tutti gli strumenti traspositori)
- La mappa instrument class e la base dell'**Instrument Classifier** (componente 2 dei "da costruire ex novo" nello scoping)
- Il workaround music21 ci risparmia di scoprire il bug in debugging
- Il pattern di write MusicXML completo (score -> parts -> notes -> write + post-process) e esattamente il nostro **MusicXML Score Writer** (componente 8 dei "da costruire ex novo")

**Verdetto 4.2**: **A - Riusabile diretto** (unico caso di tutta l'analisi).

**Strategia**: copiare ``musicxml_writer.py`` in ``src/bigband_condenser/musicxml_writer.py`` con header di attribuzione, zero refactoring per v1 (nessun ``backend.*`` import da sostituire).

**Impatto monte ore 4.2**: saving concreto **8-12 ore** (tabella trasposizioni 2-3h + instrument map 1-2h + writer end-to-end 3-4h + workaround music21 2-3h).

### Verdetto A4 consolidato

**A4.1 Bridge WebSocket**: D (fuori scope v1).
**A4.2 musicxml_writer orfano**: A (riuso diretto).

L'assunzione A4 originaria del Charter era formulata genericamente ("dorico_bridge/ compatibile con la versione di Dorico installata") e **non prevedeva la scoperta dell'orfano musicxml_writer**. La verifica ha prodotto un risultato misto ma complessivamente **positivo**: non useremo il bridge, ma guadagniamo un asset non previsto che vale 8-12h.

## 5. Riepilogo complessivo e follow-up

### Verdetti consolidati

| Assunzione | Verdetto | Saving monte ore |
|---|---|---|
| A2 - shared/models.py | B (copia selettiva) | 0.5-1h |
| A3 - chord_scales.py | B (copia integrale, uso parziale v1) | 4-6h |
| A4.1 - dorico_bridge WebSocket | D (fuori scope v1) | 0h |
| A4.2 - musicxml_writer orfano | A (riuso diretto) | 8-12h |

**Saving totale confermato**: **12.5-19 ore** rispetto a scrittura da zero. Allineato con l'ordine di grandezza del Charter.

### Impatto sui rischi

- **R04** (``shared/models.py`` troppo legato a flusso generativo): non materializzato, candidato a chiusura
- **R05** (``chord_scales.py`` non utilizzabile standalone): non materializzato, candidato a chiusura
- **R06** (``dorico_bridge/`` incompatibile Dorico installato): declassabile a "non applicabile v1" visto che il bridge e fuori scope
- **Nuovo R24 proposto**: "Bug music21 noti (es. transpose tag omesso in parti multiple stessa classe strumento) impattano qualita output MusicXML". Mitigazione gia nota via workaround ereditato da ``musicxml_writer.py``. P=2, I=2, priorita media.

Aggiornamento Risk Register raccomandato in sessione contestuale (bump v0.3).

### Nessuna modifica al progetto donatore

Conforme a Charter sezione 12.5 e R16. Nessun file di BigBand AI e stato toccato durante la verifica.

### Follow-up operativo per prossime sessioni

1. Creare i 3 file ereditati nel Condenser al momento opportuno (M3 per models e chord_parser, M4-M5 per musicxml_writer), con attribuzione in header
2. Aggiungere ``websockets`` a ``pyproject.toml`` **solo se** mai riprenderemo il bridge in fase futura (per adesso no)
3. Al momento della scrittura del Condenser MusicXML writer, cambiare ``_INSTRUMENT_TRANSPOSITIONS`` includendo anche strumenti opzionali big band (flicorni, soprano sax, clarinetti doubled dalle reeds) non presenti in BigBand AI
4. Verificare runtime del parser chord su un corpus di test reale (prima di fidarsi del 100% dei casi coperti)

### Dubbi aperti

- Nessuno bloccante per lo spike M2.
- Il "catalogo CHORD_SCALES" potrebbe avere bias verso certe varianti stilistiche jazz (Berklee-oriented); valutare in fase di uso reale se altre varianti (es. latin jazz, be-bop) richiedono estensioni.
