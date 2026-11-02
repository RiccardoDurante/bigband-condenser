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

## Sessione 2026-11-01 (ripresa M4)

- **Completato**: Music Expert conferma visivamente corrette le battute del preview Reeds. Sotto-step M4.0-M4.3 chiusi (vedi WBS_M4 v0.2).
- **Decisioni**: D-030 (collisioni cross-onset: troncamento deterministico, Opzione A), D-031 (re-baseline M4.4/M4.5). Numerazione corretta: la prima versione di queste entry collideva con D-029 gia' esistente.
- **Stato codice**: reeds.py contiene gia' split 2+3, collapse unisono/accordo (Chord) e clipping delle sovrapposizioni, anticipati durante il debug di M4.2. Mancano i gate formali di M4.4/M4.5: test dedicati e validazione visiva su segmento denso (D-029).
- **Rischi**: nessun rischio nuovo. R31/R32 gia' formali e mitigati nel Risk Register.
- **Backlog**: FR-M4-A (clef adattiva), FR-M4-B (enarmonia Ab/G#), FR-M4-C (composer non renderizzato), FR-M4-E (re-voicing con legatura, M4.6/M4.7), consolidamento pause.
- **Pending**: individuare il segmento denso (scripts/find_dense_segment.py), emettere WBS_M4 v0.3 registrando FR-M4-B/C/E, chiudere i gate M4.4/M4.5.
- **Prossimo passo**: eseguire scripts/find_dense_segment.py e scegliere il segmento per validare lo split 2+3.

## Sessione 2026-11-01 (M4.4 chiuso)

- **Completato**: M4.4 chiuso con gate pytest + fidelity (0/33 misure fuori tolleranza, da 5/33 pre-fix) + visuale Dorico su m0-m7. M4.5 assorbito.
- **Decisioni**: D-032 (segmentazione per sounding set, supera D-030 lossy e FR-M4-D). Legato intra-parte clippato all'onset successivo della stessa parte (D-022).
- **Backlog**: FR-M4-F nuovo (nota che cambia rigo tra segmenti: re-attack senza legatura). FR-M4-A/B/C/E invariati.
- **Prossimo passo**: valutare se M4.6 (omoritmia detection) resta necessario post D-032 - la segmentazione produce gia' chord verticali simultanei upper+lower nei block chord. Candidato primo step: M4.7 (text directions per soli / unisono / cast change).

## Sessione 2026-11-01 (M4.6 assorbita, M4.7 implementato)

- **Completato**: M4.6 ASSORBITO (D-033), M4.7 IMPLEMENTATO (D-034). Pipeline Reeds produce: struttura battute (M4.2), split 2+3 per sounding set con legature (M4.4), chord simultanei nei block chord (assorbito M4.6), text direction cast-change (M4.7).
- **Decisioni**: posizionamento label sopra violino + sotto basso, split a meta', font 4pt via MusicXML. Dorico applica le proprie font/position: il Music Expert accetta di aggiustare in Engraving Options.
- **Backlog**: FR-M4-F (cambio rigo senza legatura), FR-M4-G (rendering font/position editor-dependent).
- **Prossimo passo**: decidere se chiudere M4.8 (voice crossing markers) o rinviarlo al backlog e passare a M5 (Brass). Voice crossing e' edge case raro per dichiarazione del Music Expert ('casi rari, in orchestra si tende a mantenere i ruoli').

## Sessione 2026-11-01 (M4 CHIUSO)

- **Completato**: M4.6 ASSORBITO (D-033), M4.7 IMPLEMENTATO (D-034), M4.8 IMPLEMENTATO (D-035). **MILESTONE M4 CHIUSA**: Reeds condenser production-ready con struttura battute, split 2+3 per sounding set, chord simultanei, cast labels, voice crossing markers.
- **Decisioni**: posizionamento label sopra violino + sotto basso con split a meta', font 4pt via MusicXML (rendering editor-dependent), marker crossing '[abbr]>' / '[abbr]<' solo per cast >= 2.
- **Backlog M4**: FR-M4-F (cambio rigo senza legatura), FR-M4-G (rendering font editor-dependent).
- **Prossimo passo**: M5 (Brass condenser). Convenzioni gia' note: trombe in chiave di violino, tromboni in chiave di basso. Riuso previsto di tutta l'infrastruttura M4 (skeleton, split, cast labels, crossings).

## Sessione 2026-11-01 (serale) - M5 Brass scaffold + requirement layout

- **Completato**: Refactor _common.py (D-036), BrassCondenser scaffold (D-037). 79 test verdi. Fidelity brass PASS. Visual gate Dorico PASS su Kronos extract. Commit 7270d9e, tag M5-brass-scaffold.
- **Decisioni**: family-based routing per brass (trumpets+horns treble, trombones bass); flugelhorn resta tra le trombe anche se scende grave.
- **Nuovo requirement (D-038)**: PDF finale in landscape, max 8 battute per pagina, max 3 sistemi (doppi righi) per pagina. Implementazione separata.
- **Backlog**: FR-M5-A (cross-staff pitch inversion marker); aggiornare Charter con D-038.
- **Prossimo passo**: scelta tra M6 (Rhythm: piano+basso+chitarra con chord symbols e comping/shout), M7 (Drum preserver), oppure anticipare D-038 (page layout) per vedere subito risultati stampabili.

- **Fase B pianificata (D-039)**: dopo release v1.0.0, primo deliverable sara' una web app semplice (Gradio + HuggingFace Spaces) per upload MusicXML -> download PDF landscape condensed, senza GUI Dorico/Finale. Scope ridotto, zero auth. PDF-in rimane Fase C.

## Sessione 2026-11-01 (tardo serale) - M7 Drums parziale

- **Completato (parziale)**: DrumsCondenser preserver + Z translator Opzione 1 (euristica semplificata). Fidelity PASS (0 note perse). 91/91 test verdi.
- **NON passato**: visual gate in Dorico. Z Opzione 1 non remappa posizioni basse (D3/E3/F3 restano graficamente sotto il rigo come kick drum anche quando il compositore intendeva cymbals/snare). Decisione Music Expert di accettare l'imperfezione e procedere.
- **Decisioni**: D-040 (M7 + Z Opzione 1 come v1 parziale).
- **Backlog (FR-M7-D, PRIORITARIO per ripresa)**: implementare mappatura puntuale composer -> Weinberg basata su tabella Music Expert. Il compositore dovra' fornire tabella display -> strumento target per i 12-14 display usati (D3, E3, F3, G3, A3, B1, D2, B2, F5, G5, A5, B5 con casi speciali size='full'). Riferimento: Weinberg / PAS Guide to Standardized Drumset Notation.
- **Prossimo passo (next session)**: ripresa M7 con tabella puntuale + eventualmente M6 Rhythm (il piu' complesso rimasto). Monte ore consumato stima ~22h totali (su 60 budget), 38h residue per M6 + CLI + validator + docs + release.

## Sessione 2026-11-02 (mattina) - M7 Drums COMPLETE

- **Completato**: M7 chiuso definitivamente. Z Opzione 3 (by instrument name con pre-parse MusicXML raw) applica mappatura Weinberg/PAS puntuale. Scoperta chiave: il file ha 2 drum part - 'Drum Set 1' (lead sheet visibile, muted) e 'Drum Set 2' (playback, hidden). Preprocessor correttamente seleziona P17 per il condenser.
- **Decisioni**: D-041 (M7 COMPLETE).
- **Fix bug**: collect_note_instrument_names_from_xml saltava note 'MIDI82' hidden a livello di singola nota, causando disallineamento indice XML<->music21. Risolto skip print-object=no nel collect.
- **Visual gate**: PASSATO. Ride/crash/bell/splash/hi-hat tutti su posizioni Weinberg corrette.
- **Progresso v1**: M3 ✓, M4 Reeds ✓, M5 Brass scaffold ✓, M7 Drums ✓. Rimangono: M6 Rhythm (il blocco grosso), CLI, validator, docs, D-038 PDF layout landscape, release v1.0.0, poi Fase B (web app Gradio).
- **Monte ore stimato**: ~24h consumate, ~36h residue, 12 settimane alla deadline. M6 Rhythm e' il rischio principale.
- **Prossimo passo**: M6 Rhythm condenser (piano+basso+chitarra con chord symbols + discriminazione comping/shout) oppure CLI/validator per avere pipeline end-to-end minima funzionante prima di affondare su M6.
