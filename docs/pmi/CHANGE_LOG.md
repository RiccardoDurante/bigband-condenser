---
document: Change Log
document_id: CL-BBC-001
project: Big Band Condenser v1
version: 0.18
status: Active
last_updated: 2026-11-10
language: it
changelog:
  - v0.18 (2026-11-10): aggiunta D-043 (M8 CLI orchestrator MVP, pipeline end-to-end funzionante al 80%, rifinimenti post-v1).
  - v0.17 (2026-11-02): aggiunta D-042 (M6 RhythmCondenser COMPLETE con big-band hit pattern decomposition e chord extraction jazz-standard).
  - v0.16 (2026-11-02): aggiunta D-041 (M7 COMPLETE con Z Opzione 3 by instrument name, visual gate Dorico passato).
  - v0.15 (2026-11-01): aggiunta D-040 (M7 drums preserver + Z Opzione 1 euristica, PARZIALE: visual gate posizioni basse non passato, FR-M7-D in backlog per mappatura precisa post-v1).
  - v0.14 (2026-11-01): aggiunta D-039 (web app prototipo come primo deliverable Fase B, stack Gradio + HuggingFace Spaces).
  - v0.13 (2026-11-01): aggiunte D-036 (refactor _common.py), D-037 (M5 BrassCondenser scaffold) e D-038 (requirement page layout landscape 8bars/page).
  - v0.12 (2026-11-01): aggiunte D-033 (M4.6 assorbita in M4.4) e D-034 (M4.7 implementato). FR-M4-F (nota cambia-rigo senza legatura) e FR-M4-G (rendering font/posizione editor-dependent) a backlog.
  - v0.12 (2026-11-01): aggiunte D-033 (M4.6 assorbita in M4.4), D-034 (M4.7 cast labels) e D-035 (M4.8 voice crossing markers). M4 CHIUSO. FR-M4-F (cambio rigo senza legatura), FR-M4-G (rendering editor-dependent) a backlog.
  - v0.11 (2026-11-01): aggiunta D-032 (M4.4 sounding-set segmentation, supera D-030 e FR-M4-D). Terzo gate (fedelta' output vs sorgente) formalizzato.
  - v0.10 (2026-11-01): aggiunte D-030 (collisioni cross-onset, troncamento Opzione A, bugfix M4.2a-e) e D-031 (re-baseline M4.4/M4.5). Corretta collisione di ID con D-029 gia' esistente.
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
| D-030 | 2026-11-01 | Collisioni cross-onset su stessa voce (nota sostenuta ancora attiva all'ingresso di un altro strumento): troncamento deterministico della nota precedente al nuovo onset (Opzione A). Bugfix M4.2a-e in reeds.py: ripristino durata misure dopo purga, split su barra con legatura, riempimento pause per misura, collapse unisono/accordo, clipping sovrapposizioni | Cambio di cast a meta' battuta (Charter P2) non ancora gestito da logica dedicata; Opzione B (segmentazione completa per cast-change) anticipa scope M4.6/M4.7; il troncamento e' pratica standard di re-voicing nelle condensed score | reeds.py, backlog FR-M4-E (re-voicing con legatura in M4.6/M4.7) |
| D-031 | 2026-11-01 | Re-baseline M4.4/M4.5: split 2+3 per altezza e chord/unisono sono gia' implementati in reeds.py (anticipati durante il debug di M4.2); restano da chiudere i gate formali (test dedicati e validazione visiva su segmento denso come da D-029) | Senza chord collapse la struttura delle battute non era validabile: sequenziamento WBS errato. Evita di rifare lavoro gia' fatto senza rinunciare ai gate obbligatori | WBS_M4.md (v0.3 da emettere), STATUS.md |
| D-032 | 2026-11-01 | M4.4 split 2+3 riprogettato: segmentazione per sounding set invece di ranking solo-sugli-attacchi. Ad ogni cambio del set attivo le note sonanti sono riordinate per altezza; le voci che continuano sono legate nota per nota. Supera D-030 (troncamento lossy) e FR-M4-D (durate falsate da onset-merge). Legato intra-parte clippato all'onset successivo della stessa parte (D-022) | Gate fedelta' (scripts/check_fidelity.py): 5/33 misure fuori tolleranza, 7.2% missing / 1.8% extra -> 0/33 misure, 0.1% missing / 0.4% extra. Visual gate Dorico su m0-m7 OK | reeds.py riscritto, TestReedsSoundingSetSegmentation, scripts/check_fidelity.py come 3o gate |
| D-033 | 2026-11-01 | M4.6 (omoritmia detection) chiuso come ASSORBITO in M4.4. La segmentazione per sounding set produce naturalmente Chord simultanei upper+lower nei block chord | Verifica dump_measure m5/m7: upper e lower con stessa offset e durata | WBS_M4 esito M4.6 |
| D-034 | 2026-11-01 | M4.7 (text directions per cast change) implementato: label sopra violino + sotto basso, split 2+3, abbreviazioni S.Sx/A.Sx/T.Sx 1/T.Sx 2/Bar.Sx, 'Tutti' per 5 strumenti non-unisono, font-size=4pt, soglia 1 misura (bypass unisono) | Rendering font/posizione editor-dependent (Dorico applica proprio Technique Text style); Music Expert accetta e sistema una tantum in Engraving Options. FR-M4-G a backlog | reeds.py cast module, TestReedsCastChange (10 test) |
| D-035 | 2026-11-01 | M4.8 (voice crossing markers) implementato: marker breve '[abbr]>' per strumento in rigo sopra il default, '[abbr]<' per sotto. Default rank 1-5 (Soprano, Alto, T1, T2, Bari). Inserito solo per cast >= 2 strumenti | Edge case raro ('in orchestra si tende a mantenere i ruoli'); su extract Kronos probabilmente zero crossing attivi | reeds.py: _detect_crossings, _format_crossing_marker, _insert_text_direction (helper comune M4.7+M4.8), TestReedsVoiceCrossing (5 test) |
| D-036 | 2026-11-01 | Refactor: estratta infrastruttura generica in condenser/_common.py (380 righe); reeds.py ridotto a costanti section-specific + class (90 righe) | Backward compat preservato via import re-export; 74 test reeds continuano a passare. Preparazione per M6/M7 | condenser/_common.py (nuovo), condenser/reeds.py riscritto |
| D-037 | 2026-11-01 | M5 BrassCondenser scaffold IMPLEMENTATO: family-based routing (Trumpets 1-4 + Horns 1-2 -> treble; Trombone + Bass Trombone -> bass). Pitch ordering dentro famiglia, voice counts dinamici (99 max), no crossing marker (family rigido) | Fidelity gate PASS (0/33 misure fuori tolleranza, 0.1% missing/extra). Visual gate Dorico OK. Scaffold completato in <30 min grazie al refactor D-036 | brass.py, test_condenser_brass.py (5 test), preview_brass.py, check_fidelity_brass.py, tag M5-brass-scaffold |
| D-038 | 2026-11-01 | REQUIREMENT futuro (page layout PDF): formato landscape, max 8 battute per pagina, max 3 sistemi (doppi righi) per pagina | Scope separato dalle condensation sections (ambito page/print layout). Implementazione pianificata come step dedicato, verosimilmente in M8 (CLI + documentazione finale) o milestone nuova M6b | TBD: aggiornare Charter |
| D-039 | 2026-11-01 | Web app semplice (upload MusicXML, download PDF landscape condensed score) confermata come PRIMO DELIVERABLE DI FASE B (post v1.0.0, gennaio-febbraio 2027). Stack previsto: Gradio su HuggingFace Spaces (deploy gratuito, LilyPond disponibile via packages.txt). Scope ridotto: solo upload+download, no auth, no cronologia, no multi-user. PDF-in resta fuori scope (OMR = Fase C) | Scope v1 Charter preservato (web interface era gia' Fase B in roadmap). Monte ore v1 protetto: M6 Rhythm resta priorita'. Prototipo web diventa demo per release v1.1 pochi mesi dopo v1.0 | TBD Fase B |
| D-040 | 2026-11-01 | M7 DrumsCondenser (preserver) + Z translator Opzione 1 (euristica semplificata, NON mappatura puntuale). Z: display ottava>=5 -> notehead=x stem=up (cymbal zone); size='full' -> notehead=slash stem=up (ensemble cue, override octave); altre -> notehead=normal preservato. Non remappa posizioni (preserva display come scritto nel sorgente) | PARZIALE: visual gate NON passato per le posizioni basse (D3/E3/F3 restano visualizzate basse con tagli addizionali, Dorico le mostra come kick quando il compositore voleva cymbals sostenuti in m3-m6, snare in m110-m112). Fidelity gate PASS (43 note sorgente = 43 output, zero perdite). 91/91 test verdi. Decisione Music Expert: accettare Opzione 1 come v1, mappatura puntuale rinviata a backlog FR-M7-D | drums.py, drum_normalizer.py, test_condenser_drums.py (4 test), test_drum_normalizer.py (8 test), preview_drums.py, check_fidelity_drums.py, tag M7-drums-partial-z1 |
| D-041 | 2026-11-02 | M7 COMPLETE: Z translator Opzione 3 (by instrument name) con mappatura Weinberg/PAS puntuale. Letto raw MusicXML part-list per estrarre score-instrument name di ogni nota (music21 collassa i percussion score-instrument in un unico generic 'Percussion', perdendo la mappatura per-nota). Fix bug di disallineamento indice XML<->music21 saltando note con print-object=no nel collect. Scoperto che il file Kronos ha 2 drum part: Drum Set 1 (lead sheet visibile, muted) e Drum Set 2 (playback MIDI, hidden). Il preprocessor correttamente strippa P18 e preserva P17 come richiesto dal Music Expert | Visual gate Dorico confermato: ride/crash/bell/splash/hi-hat tutti su posizioni Weinberg corrette (F5/A5/B5/G5) con notehead X e stem up. Fidelity gate PASS (43 note sorgente = 43 output, zero perdite). 93/93 test verdi | drum_normalizer.py (by-name + XML prepass), drums.py (source_xml_path param), test_drum_normalizer.py (10 test by-name), tag M7-drums-complete |
| D-042 | 2026-11-02 | M6 COMPLETE: RhythmCondenser (Opzione D con staff-style awareness). Preserver + merger che combina Guitar + Bass visibili in 2 righi condensati, estrae chord symbols dal Piano hidden (fonte autoritativa 120 chord nel full Kronos), applica slash notation nelle regioni dichiarate da <measure-style><slash/> MusicXML standard. Per le 6 misure di ensemble figure cue (m99/101/103/105/106/108) applica la decomposizione standard big band chart: [quarter + quarter + dotted-quarter + eighth tied-to-next-bar], con eighth in rhythmic notation (stem+flag) e legatura cross-measure per anticipo dell'accordo | Visual gate Dorico CONFERMATO. Chord symbols jazz standard (Am9, G7sus, Cmaj9/E). Scoperte chiave: measure-style/slash come game-changer deterministico (vs euristica), Piano usato solo per chord non per note trascritte. 93/93 test verdi | 4 nuovi moduli: rhythm_staff_style.py, chord_extractor.py, piano_cues.py, condenser/rhythm.py. preview_rhythm.py, tag M6-rhythm-complete |
| D-043 | 2026-11-10 | M8 CLI orchestrator MVP: comando 'bbcondenser' end-to-end. Argparse minimale (input + -o output). Pipeline: parse -> preprocess -> classify -> condense Reeds/Brass/Rhythm/Drums -> merge 7-part Score -> write MusicXML -> sanitize R32. Entry point via pyproject.toml gia' dichiarato (bbcondenser = cli:main) | Visual gate Dorico PASS al 80% (Music Expert: 'ragionevole, rifinimenti dopo'). Test end-to-end su Kronos full (142 bar): 625+559+1010+394 note su 7 parts, 1.5MB output, sanitizer attivo (27 rest unhidden). 93/93 test verdi | cli.py (nuovo), tag M8-cli-mvp |
| D-033 | 2026-11-01 | M4.6 (omoritmia detection) chiuso come ASSORBITO in M4.4. La segmentazione per sounding set produce naturalmente Chord simultanei upper+lower quando il sorgente ha onset coincidenti - nessun codice dedicato necessario | Verifica su dump_measure m5 e m7 (block chord): upper e lower hanno Chord con stessa offset e stessa durata | WBS_M4 esito M4.6 |
| D-034 | 2026-11-01 | M4.7 (text directions per cast change) implementato: label sopra rigo violino + sotto rigo basso, split 2+3, abbreviazioni S.Sx/A.Sx/T.Sx 1/T.Sx 2/Bar.Sx, 'Tutti' per 5 strumenti non-unisono, font-size=4pt, soglia 1 misura (bypass per unisono) | Rendering effettivo di font e posizione dipende dall'editor target (Dorico ignora font-size e default-y da MusicXML, applica Technique Text paragraph style). Music Expert accetta e sistema una tantum in Engraving Options. FR-M4-G a backlog | reeds.py cast module (10 funzioni), TestReedsCastChange (10 test) |

## Change Request

_Nessuna al momento._

---

## 2026-11-10 — D-040: Output layout = A4 landscape

**Owner:** Developer
**Richiesto da:** Sponsor
**Contesto:** Preview output in portrait produceva 3 misure/pagina con
spaziature irregolari tra sistemi.
**Decisione:**
- `<page-layout>` A4 landscape (page-width 1684, page-height 1190 tenths)
- `<system-distance>` 90, `<staff-distance>` 75, `<top-system-distance>` 110
- Strip di tutti i `<page-layout>`, `<system-layout>`, `<staff-layout>`
  locali dentro gli elementi `<print>` (override del `<defaults>` globale)
**Impatto:** M10 PDF (D-038) si allinea a landscape. CLI inietta layout
dopo la write via `page_layout.inject_landscape_layout`.
**Supersedes:** nessuna.

---

## 2026-11-10 — D-041: Part labels compatti (jazz-standard)

**Owner:** Developer
**Richiesto da:** Sponsor
**Contesto:** part-name verbose ereditati dal source (`Reeds (upper)`,
`S. Sx.`, ...) spingevano i righi per far spazio alle etichette.
**Decisione:**
- Mapping: Reeds 1/R1, Reeds 2/R2, Brass 1/B1, Brass 2/B2,
  Guitar/Gtr, Bass/Bs, Piano/Pno, Drums/Dr
- Font-size: 9pt per `<part-name>`, 8pt per `<part-abbreviation>`
- Strip di `<part-name-display>` e `<part-abbreviation-display>` ereditati
**Rischio noto (R-NEW-01):** Dorico può ignorare il `font-size` MusicXML
e usare l'Engraving Options locale. Da verificare nel PDF finale (M10).
LilyPond rispetta il `font-size` nativamente.
**Supersedes:** nessuna.

---

## 2026-11-10 — M9 Validator chiuso

**Owner:** Developer
**Contesto:** Fidelity validator unificato per le 4 sezioni, CLI integrato
(`--validate`, `--report`, `--tolerance`).
**Risultati su Kronos Kai Kairos (142 misure, 20 strumenti):**
- Drums: `PASS` strict (0/1)
- Brass: `PASS*` (1/142 = 0.7%, sotto soglia 2%)
- Rhythm: `PASS*` (1/98 = 1.0%, 44 slash-region bars escluse)
- Reeds: `FAIL` (59/142 = 41.5%) — bug noto, TK-Reeds-01
**Semantica:** `PASS` = 0 bars bad. `PASS*` = bars_bad/bars_checked <= 2%.
`FAIL` = oltre soglia.
**Tolleranze per sezione:** Reeds 0.25q, Brass 0.75q, Rhythm 0.25q.


---

## 2026-11-10 — D-042: TK-Reeds-01 risolto parzialmente (known limitation v1.0)

**Owner:** QA
**Contesto:** Fidelity validator segnala 59/142 bars FAIL nella sezione Reeds
(missing `≈` extra `≈` 24%). Investigazione ha rivelato 3 pattern distinti:

1. **Chord sorgente anomali** (es. Soprano Sax m82 con 7 pitch gravi
   simultanei): il 2+3 split pitch-based scarta le pitch eccedenti. Fix
   richiede preprocessore che filtri chord > 2 pitch per sax.

2. **Tie cross-measure**: alcune note di fine misura appaiono all'inizio
   della successiva (m84 missing=4, m85 extra=4). Fix richiede rework del
   tie handling in `_build_voice_elements`.

3. **Music21 writer quantizza durate non-standard** (es. terzina 0.67q)
   spezzandole in tie di micro-note durante `Score.write("musicxml")`.
   Il writer aggiunge ~88 note durante il write su Kronos. Fix richiede
   snap preventivo delle durate a griglia (0.25q + 1/3q) prima del write.

**Decisione:** parzialmente risolto per v1.0. Mitigation applicata:
- `coalesce_tied_pitches`: fonde note adiacenti stesso pitch (riduce
  Rhythm 1010→742 note, Brass 559→419)
- `filter_micro_notes` (min_duration=0.125q): safety net per futuri source
  con micro-note in memoria

**Stato per v1.0:**
- Reeds: FAIL validator (41.5% bars), output musicalmente leggibile
- Brass: PASS* (0.7%)
- Rhythm: PASS* (1.0%)
- Drums: PASS strict

**Rinvio:** FR-v1.1 TK-Reeds-02, FR-v1.1 TK-Reeds-03, FR-v1.1 TK-Reeds-04
(uno per pattern). Stima totale 4-6h.

**Documentazione utente:** README sezione "Known limitations" + esempio.


---

## 2026-11-10 — M10-partial: LilyPond pipeline operativa ma limitata

**Owner:** Developer
**Risultato:**
- `scripts/build_pdf.py` funzionante: converte MusicXML condensed in PDF
  A4 landscape via music21 + LilyPond
- `\paper` block con margini simmetrici, max 4 systems/page, indent 25mm
- `uniform-stretching = ##t` per bar di larghezza simile
- Tentativo `musicxml2ly` (converter LilyPond nativo) fallisce sul nostro
  MusicXML (probabile incompatibilità con `<measure-style>` o chord
  anomali); fallback automatico su `music21.write("lily")`

**Qualità PDF:**
- Orientamento A4 landscape ✓
- Densità bars/pagina ~ target
- Labels compatti all'inizio dei sistemi
- **Limitazioni note:** battute di larghezze non perfettamente uniformi
  (uniform-stretching mitiga ma non elimina), durate non sempre fedeli al
  source XML (music21 writer quantizza), note extra/missing in bars con
  pattern D-042

**Verdict Tech Lead:** LilyPond pipeline ha raggiunto il tetto pratico con
questa toolchain. Miglioramenti ulteriori richiederebbero riscrittura del
backend LilyPond di music21 (fuori scope) o fix dei pattern D-042 (4-6h).

---

## 2026-11-10 — PROPOSTA D-043: ridefinire M10 come "MusicXML + Dorico template"

**Owner:** PM
**Stato:** PROPOSED — attende decisione sponsor

**Motivazione:**
1. Qualità PDF LilyPond inferiore rispetto a Dorico export (gap ~15%)
2. User target (arrangiatori jazz professionisti) usano Dorico/Finale/Sibelius
3. MusicXML condensed è il vero deliverable; il PDF è un re-render

**Decisione proposta:**
- M10 primary deliverable = `output.musicxml` + template Dorico
  (`templates/bigband_condensed.dorico`) + guida `docs/how_to_pdf.md`
- `scripts/build_pdf.py` resta come tool opzionale "best-effort" per
  utenti senza software professionale, con disclaimer in README

**Impatto budget:**
- Risparmio: 6-8h di polish LilyPond
- Costo: 2-3h per template Dorico + how-to
- Netto: +4-5h di buffer sulla deadline

**Alternativa:** restare su LilyPond, accettare quality gap, documentare.

