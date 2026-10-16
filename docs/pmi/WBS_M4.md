---
document: WBS M4 - Reeds Condenser Breakdown
document_id: WBS-BBC-M4-001
project: Big Band Condenser v1
version: 0.1
status: Active (post retrospective 2026-10-16)
last_updated: 2026-10-16
language: it
changelog:
  - v0.1 (2026-10-16): prima emissione dopo retrospettiva M4-R1 fallito su visual validation (metadata/measure structure mancanti). WBS granulare con 8 sotto-step M4.1-M4.8, ciascuno validato visualmente in Dorico prima del successivo.
---

# WBS M4 - Reeds Condenser Breakdown

## 1. Scopo e lezione appresa

Il **primo tentativo M4-R1** (2026-10-16) e fallito su visual validation in Dorico pur avendo 9/9 pytest green. Problemi scoperti dal Music Expert:
- Armatura di chiave mancante
- Tempo mancante
- Tonalita di partenza mancante
- Suddivisione in battute errata
- Molti errori notazionali generici

**Causa radice**: scope R1 troppo ampio, nessuna validation visiva intermedia. L'approccio "split + quantize + makeNotation + write" in un unico step saltava i pezzi fondamentali di preservazione metadata e struttura.

**Lezione (R31 candidato)**: ogni sotto-step di condensation richiede **visual validation obbligatoria** in Dorico/Finale prima del prossimo. pytest green non e sufficiente - garantisce assenza di eccezioni Python, non correttezza musicologica.

## 2. Principi WBS

1. **Micro-incrementi**: ogni sotto-step 20-60 min di lavoro
2. **Visual validation obbligatoria**: dopo ogni sotto-step, output in Dorico + feedback Music Expert PRIMA di procedere
3. **Commit intermedio su main** per ogni sotto-step completato
4. **Rollback explicit**: se un sotto-step fallisce visualmente, STOP + retrospective + non si procede
5. **Scope creep protection**: lo scope di ogni sotto-step e vincolante, no "intanto che ci sono" aggiunte

## 3. Sotto-step M4

### M4.0 - Infrastruttura condenser/ (completato 2026-10-16)

**Scope**: creare package `src/bigband_condenser/condenser/` con `base.py` + `reeds.py` scaffolded. Non include logica musicologica.

**Deliverable**:
- `src/bigband_condenser/condenser/__init__.py`
- `src/bigband_condenser/condenser/base.py` (SectionCondenser abstract class)
- `src/bigband_condenser/condenser/reeds.py` (scaffold con split 2+3 naive)
- `tests/test_condenser_reeds.py` (9 test green)

**Status**: ✅ COMPLETATO. Non visually validated ma riusabile come scaffold.

### M4.1 - Metadata preservation

**Scope**: nel ReedsCondenser, copiare dal source Score i seguenti metadata nel condensed output:
- Key signature iniziale (es. Bb major)
- Time signature iniziale (es. 4/4)
- Tempo marking iniziale (es. 120 BPM, "Medium swing")
- Score-level metadata (title, composer, movement name)

**Non in scope M4.1**: cambi di key/time/tempo mid-score, dynamics, articulations.

**Durata target**: 30-45 min.

**Deliverable**:
- ReedsCondenser accetta parametro `source_score: music21.Score` opzionale per leggere metadata
- Script preview aggiornato
- Test pytest `test_metadata_preserved`

**Validation visiva (OBBLIGATORIA prima di M4.2)**:
- Dorico mostra l'armatura di chiave corretta all'inizio
- Dorico mostra il time signature corretto
- Dorico mostra il tempo marking all'inizio
- Il titolo del brano appare

### M4.2 - Measure structure preservation

**Scope**: preservare la struttura di misure del source:
- Numero di misure totale (33 per Kronos extract: pickup + bars 1-32)
- Pickup measure (anacrusi) a battuta 0
- Barlines nelle posizioni corrette
- Numeri di misura progressivi

**Non in scope M4.2**: double barlines, repeat marks, codetta/coda, section markers.

**Durata target**: 30-45 min.

**Deliverable**:
- ReedsCondenser costruisce Part con Measure objects espliciti (non insert() a offset arbitrari)
- Test pytest `test_measure_count` e `test_pickup_preserved`

**Validation visiva**:
- Dorico mostra 33 misure contate correttamente
- Pickup measure visibile come battuta 0 (anacrusi)
- Nessun errore "measure incomplete" o "overfilled measure"

### M4.3 - Single-voice passthrough

**Scope**: copia 1 sola voce sax (es. Soprano) nel pentagramma superiore del condensed, no ranking, no split. Serve a validare che il **pipeline completo di preservazione metadata + struttura funziona per 1 voce**.

**Non in scope M4.3**: multiple voices, split, chord.

**Durata target**: 20-30 min.

**Deliverable**:
- Modalita "passthrough" nel ReedsCondenser (parametro `_debug_single_voice=True`)
- Test pytest che verifica numero note = numero note sax originale
- Preview output riconoscibile come "Soprano Sax"

**Validation visiva**:
- Dorico mostra la parte di Soprano Sax leggibile, con tutte le note nelle posizioni corrette
- Metadata preservati (M4.1)
- Struttura di misure corretta (M4.2)
- Se musicologicamente leggibile come "parte di Soprano", M4.3 PASS

### M4.4 - Dynamic 2+3 split by pitch

**Scope**: introdurre il ranking dinamico 2+3 per altezza, treble/bass clef (D-028 variant). Riusa il codice R1 scaffolded in M4.0.

**Non in scope M4.4**: chord notation, text directions, voice crossing markers.

**Durata target**: 30-45 min.

**Deliverable**:
- ReedsCondenser.condense() con logica split by pitch sopra la base M4.1-M4.3
- Test pytest aggiornati per 2+3 split
- Preview output con 5 voci distribuite 2 top + 3 bottom

**Validation visiva**:
- Le 2 voci piu acute sono nel pentagramma superiore (treble)
- Le 3 voci piu gravi sono nel pentagramma inferiore (bass clef)
- Riconoscibile come "sezione Reeds a 5 voci condensata"
- Range delle note bass clef appropriato (non troppo basso, non troppo alto)

### M4.5 - Chord notation for simultaneous notes

**Scope**: quando 2+ note hanno lo stesso onset nello stesso pentagramma, aggregare come music21.chord.Chord object (unica entita verticale), non come note separate impilate.

**Non in scope M4.5**: chord symbol analysis (es. "Cmaj9"), chord inversion detection.

**Durata target**: 30-45 min.

**Deliverable**:
- ReedsCondenser raggruppa note stesso onset in Chord
- Test pytest `test_simultaneous_notes_become_chord`
- Preview output con chord verticali leggibili

**Validation visiva**:
- Chord verticali ben formati in Dorico (teste di nota allineate)
- Nessun "note cluster illeggibile"
- Durate dei chord coerenti con le note originali

### M4.6 - Omoritmia detection

**Scope**: identificare passaggi dove tutte le 5 voci della sezione suonano lo stesso ritmo (block chord). In quei passaggi, assicurare che l'output abbia chord verticali simultanei upper + lower.

**Non in scope M4.6**: analisi contrappuntistica, polifonia complessa.

**Durata target**: 45-60 min.

**Deliverable**:
- Funzione `_detect_omoritmia(parts)` nel ReedsCondenser
- Test pytest con un onset group che e omoritmico
- Preview output con block chord sezione riconoscibili

**Validation visiva**:
- Nei block chord della partitura originale, l'output condensed mostra chord simultanei
- Nei passaggi non-omoritmici, le voci sono distribuite ma non forzate in chord

### M4.7 - Text directions per soli / unisono / cast change

**Scope**: quando cambia il set di strumenti attivi (soli, unisono, rientro sezione), inserire text direction esplicita all'inizio del nuovo evento. Format: nome strumento o lista strumenti.

**Non in scope M4.7**: analisi narrativa musicale, interpretazione di sezioni formali.

**Durata target**: 45-60 min.

**Deliverable**:
- Logica cast tracking frame-by-frame
- Text direction insert con music21.expressions.TextExpression
- Test pytest con un cast change
- Preview output con etichette strumenti sopra le note

**Validation visiva**:
- All'inizio di un solo di Alto Sax 1 appare "A.Sax 1" sopra la nota
- All'inizio di un unisono appare la lista degli strumenti
- Al rientro della sezione, nessuna etichetta (default)

### M4.8 - Voice crossing markers

**Scope**: quando l'algoritmo di split pone una voce in posizione "non standard" (es. Baritone finisce nel pentagramma superiore perche suona piu acuto del Soprano), aggiungere marker testuale che dichiara il crossing.

**Durata target**: 30 min.

**Deliverable**:
- Marker visivo (text expression breve, es. "Bar.>")
- Test pytest con un crossing simulato
- Preview output con marker chiaramente visibile sui crossing

**Validation visiva**:
- Nei (rari) crossing, il marker e leggibile
- Nei passaggi normali (nessun crossing), nessun marker rumoroso

## 4. Totali e integration

**Durata totale M4 revisionata**: 4-6 ore effettive (vs 2-3h stima originale).

**Riferimenti Charter**: milestone M4 target "fine novembre 2026". Oggi 16/10/2026, ~6 settimane di margine. Scope revisionato dentro margine.

**Decisioni di dominio referenziate**:
- D-022: notazione > playback MIDI (filter sub-semicroma)
- D-028: dynamic split 2+3 treble/bass (user input 2026-10-16)
- P1: tie-breaking stabile per nome strumento
- P2: trigger text = cast change

**Rischi coperti**:
- R15 scope creep: WBS granulare prevede confini espliciti per ogni sotto-step
- R30 music21.write corruption: gia mitigato in M3 preprocessor
- R31 candidato (sottostima M4): mitigation = WBS corrente + visual validation

**Backlog items** (NON scope M4):
- FR-M4-A: Adaptive clef (bass clef quando sezione troppo grave, treble quando troppo acuta)
- Chord symbol analysis automatica (fase D Charter)
- Dinamiche, articolazioni, slurs preservati (fase M4-bis o M5-6)

## 5. Processo di validation per ogni sotto-step

## 6. Prossimi passi immediati

1. Commit intermedio corrente (M4.0 completato, M4-R1 originale fallito su validation ma scaffold riusabile)
2. Iniziare M4.1 (metadata preservation) in sessione successiva
3. Bump CHANGE_LOG v0.9 con D-028, D-029 (WBS M4 formalizzata), R31 nel Risk Register
