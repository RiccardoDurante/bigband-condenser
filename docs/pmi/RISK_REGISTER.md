---
document: Risk Register
document_id: RR-BBC-001
project: Big Band Condenser v1
version: 0.6
status: Draft
last_updated: 2026-10-18
language: it
changelog:
  - v0.6 (2026-10-18): R31 promosso da candidato (WBS_M4.md) a formale e Mitigato dopo il fix M4.2 visual-gate. Aggiunto R32 (music21 writer print-object quirk), Mitigato. Totale rischi: 32.
  - v0.5 (2026-10-15): post-Spike M2 implementation. R27 DOWNGRADED da score 9 (critico) a score 4 (medio) con evidenza empirica. Aggiunti R28 (hidden parts detection, mitigation validata), R29 (octave-transposing conventions, lezione di dominio), R30 (music21.write output corruption da wrong class, nuovo CRITICO con mitigation definita). Totale rischi: 30.
  - v0.4 (2026-10-14): R07 e R12 passati a "Materializzato"; aggiunti R26 (music21 class detection unreliable Finale) e R27 (music21.write drum fail, critico)
  - v0.3 (2026-10-14): R04/R05 "Non materializzato", R06 "Non applicabile v1", aggiunto R24
  - v0.2 (2026-10-12): aggiunto R23 (qualita MusicXML input)
  - v0.1 (2026-10-12): prima emissione, 22 rischi
---

# Risk Register - Big Band Condenser v1

**Scala.** P e I da 1 a 3. Punteggio = P x I (1-9). Priorita: 6-9 alta, 3-4 media, 1-2 bassa.
**Stato:** Aperto / In monitoraggio / Mitigato / Materializzato / Non materializzato / Non applicabile v1 / Chiuso.

| ID | Categoria | Rischio | P | I | Punt. | Risposta e mitigazione | Stato |
|---|---|---|---|---|---|---|---|
| R01 | Pianificazione | Produttivita BigBand AI non trasferibile, 60 ore sottostimate | 2 | 3 | 6 | Verifica nelle prime 2 settimane (spike M2); ristimare con dati reali | Aperto |
| R02 | Pianificazione | Deadline 31/01/2027 non rispettata | 2 | 2 | 4 | Buffer 25%; monitoraggio settimanale | Aperto |
| R03 | Pianificazione | Disponibilita Sponsor < 5h/sett | 2 | 2 | 4 | Sessioni brevi; STATUS.md | Aperto |
| R04 | Tecnico | shared/models.py troppo legato a flusso generativo | 2 | 1 | 2 | Verifica precoce; copia solo generica | Non materializzato (14/10) |
| R05 | Tecnico | chord_scales.py non utilizzabile standalone | 2 | 1 | 2 | Isolare dipendenze | Non materializzato (14/10) |
| R06 | Tecnico | dorico_bridge/ incompatibile con Dorico | 1 | 3 | 3 | Flusso primario import manuale | Non applicabile v1 (14/10) |
| R07 | Tecnico | music21 gestisce male multi-staff/slash/drums | 2 | 3 | 6 | XML pass-through drum; workaround ereditato | Materializzato (14/10, mitigato via R27 strategia) |
| R08 | Tecnico | Rilevatore comping/shout non converge su borderline | 2 | 2 | 4 | Soglie parametrizzabili; override manuale | Aperto |
| R09 | Tecnico | Chord symbols duplicati piano/chitarra | 2 | 1 | 2 | Precedenza piano; test dedicati | Aperto |
| R10 | Tecnico | Doubling reeds gestito errato | 2 | 2 | 4 | Classificazione per esecutore | Aperto |
| R11 | Tecnico | Assegnazione ritmica ambigua | 2 | 2 | 4 | Tabella esplicita + override | Aperto |
| R12 | Tecnico | Differenze export MusicXML (Dorico/Sibelius/Finale/MuseScore) | 3 | 2 | 6 | Dichiarare support Dorico v1, altri best effort | Materializzato (14/10, Kronos e Finale) |
| R13 | Qualita | Materiale test insufficiente | 2 | 2 | 4 | Brani apposta; motore BigBand AI | Aperto |
| R14 | Qualita | Qualita musicale condensed non adeguata | 2 | 2 | 4 | Valutazione Sponsor 1-5; iterazioni | Aperto |
| R15 | Scope | Scope creep | 3 | 3 | 9 | Charter vincolante; Change Request obbligatoria | Aperto |
| R16 | Scope | Modifiche non autorizzate a BigBand AI | 2 | 3 | 6 | Policy read-only; CR nel donatore | Aperto |
| R17 | Legale | Reference copyright nel repo pubblico | 1 | 3 | 3 | Reference locale .gitignore; pre-commit check | Aperto |
| R18 | Risorse | Limiti Claude Pro rallentano | 2 | 2 | 4 | Sessioni focalizzate | Aperto |
| R19 | Risorse | Perdita contesto tra sessioni | 2 | 2 | 4 | STATUS.md; Project memory; commit frequenti | Aperto |
| R20 | Costi | Budget 200 EUR superato | 1 | 2 | 2 | Riserva 120 EUR; no acquisti senza CR | Aperto |
| R21 | Fornitori | Anthropic modifica piani/prezzi | 1 | 2 | 2 | Documentazione indipendente | Aperto |
| R22 | Processo | Overhead documentale sottrae ore sviluppo | 2 | 2 | 4 | Documenti compatti; PDF solo milestone | Aperto |
| R23 | Qualita | Qualita MusicXML input bassa | 2 | 2 | 4 | README chiaro; validator diagnostico | Aperto |
| R24 | Tecnico | Bug music21 omissione <transpose> parti multiple stessa classe | 2 | 2 | 4 | Workaround ereditato _fix_missing_transpose_tags; nel Kronos NON si manifesta perche R26 fa vedere a music21 classi diverse (sbagliate) per ogni parte | Aperto - non manifestato in Spike M2 |
| R25 | Tecnico | Classificazione fallisce su organici non canonici (corni F, flicorni) | 2 | 2 | 4 | partName matching per categoria strumentale. Validato 19/19 su Kronos (soprano sax + 2 corni F) in Spike M2 Q2 | Aperto - mitigation validata |
| R26 | Tecnico | music21 instrument class INAFFIDABILE su export Finale (19/19 Kronos misclassificati). Causa: Finale esporta MIDI program del template playback | 3 | 2 | 6 | Classifier NON usa part.getInstruments(); usa partName testuale. Validato empiricamente. ATTENZIONE: impatta anche R30 (output corruption) | Aperto - mitigation validata |
| R27 | Tecnico | music21.write() fallisce su durate drum sub-semicroma di export Finale (eventi 2048th usati per realistic playback, grace note roll, humanization) | 2 | 2 | 4 | **DOWNGRADED da score 9 a score 4** in Spike M2 Q4 (15/10). Strategia validata empiricamente: strip hidden parts + filter durate < 0.25 quarterLength pre-write. Validato su Kronos extract: 157 sub-semicroma Drum Set 1 + 153 Drum Set 2 scartati sono playback MIDI artifacts, non notazione intenzionale. Grace tag count = 0 (zero notazione legittima persa). Principio D-022 codificato: notazione scritta > dati playback MIDI | Mitigato validato |
| R28 | Tecnico | Parti MusicXML marcate hidden dal software source (es. Finale <staff-details print-object=no/>) sono playback-only e non devono entrare nella condensed. Esempio Kronos: Drum Set 2 e parte MIDI playback hidden, Drum Set 1 e parte visibile notazionale | 2 | 2 | 4 | Detect hidden parts pre-classify via XML parsing del tag <staff-details print-object=no/> senza attributo number. Validato empiricamente in Spike M2 Q2 | Aperto - mitigation validata |
| R29 | Processo | Convenzioni trasposizione di ottava (guitar/bass notati 1 ottava sopra sounding; piccolo trombone; piccolo in Db a 1 ottava sopra; ecc.) possono generare falsi positivi di errore nei test se le tabelle expected non le includono | 1 | 1 | 1 | Documentare convenzioni notazione nelle tabelle expected del test suite. Lezione di dominio emersa in Spike M2 Q3 | Aperto - lezione documentata |
| R30 | Tecnico | music21.write() RIGENERA il tag <transpose> dalla instrument class interna invece di preservare il tag source XML. Combined con R26 (wrong class detection), causa SILENT CORRUPTION dell'output per parti mis-classificate: Acoustic Bass Kronos scritto come SopranoSaxophone (tag -2 st) invece del corretto -12 st octave. Guitar non impattato (music21 lo vede come Instrument generica, no default transposition, preserva tag source) | 3 | 3 | 9 | **PRIORITA CRITICA**. Mitigazione: forzare instrument class corretta pre-write via partName -> music21.instrument class mapping (tabella basata su _INSTRUMENT_TRANSPOSITIONS ereditata da BigBand AI musicxml_writer orfano). Alternativa: post-process XML output per overwrite <transpose> da source. Scoperto empiricamente in Spike M2 Q5. Da implementare in M3/M4 | Aperto - mitigation definita |
| R31 | Processo | Visual validation Dorico da sola non e sufficiente: una misura puo avere durata XML totale corretta (quadra con la TimeSignature) ma apparire visivamente incompleta se la libreria di scrittura introduce elementi non-stampabili (print-object="no"). Un gate numerico ingenuo che misura solo la durata totale non rileva il problema. Scoperto nel fix M4.2 visual-gate (18/10): 32/66 misure del preview reeds erano visivamente corte nonostante durata totale corretta | 2 | 3 | 6 | Invariante numerico a doppio livello: durata totale E durata visibile (print-object) per misura/voce, verificato automaticamente prima del gate visivo Dorico. Script scripts/diagnose_measure_durations.py (totale) + scripts/diagnose_visible_durations.py (visibile). Una divergenza tra i due blocca il gate finche non e spiegata | Mitigato (18/10, M4.2 visual-gate fix, tag M4.2-visual-fix) |
| R32 | Tecnico | music21 v10.5 MusicXML writer emette print-object="no" spurio su oggetti Rest inseriti direttamente in Measure (non in Voice), anche quando nessun oggetto Python ha hideObjectOnPrint=True. Causa misure visivamente incomplete in Dorico nonostante XML numericamente corretto. Confermato empiricamente (scripts/probe_pipeline.py): 0 hidden in-memory prima della scrittura, 34 hidden nel file XML scritto | 2 | 2 | 4 | Post-write XML sanitizer (src/bigband_condenser/musicxml_sanitizer.py, funzione unhide_rests) rimuove print-object="no" da ogni elemento <note> contenente <rest>. Chiamato da scripts/preview_reeds.py dopo la scrittura. ATTENZIONE: potrebbe rimuovere hidden rest future legittimamente intenzionali (es. simboli multi-measure rest) — raffinare il filtro se necessario quando quel caso si presenta | Mitigato (18/10) |

## Sintesi

- **Priorita critica (9):** R15 (scope creep), R30 (music21.write corruption)
- **Alta priorita (6):** R01, R07 (Materializzato), R12 (Materializzato), R16, R26, **R31 (nuovo, Mitigato)**
- **Media priorita (3-4):** R02, R03, R08, R10, R11, R13, R14, R17, R18, R19, R22, R23, R24, R25, R27 (downgradato), R28, **R32 (nuovo, Mitigato)**
- **Bassa priorita (1-2):** R20, R21, R29
- **Non materializzato:** R04, R05
- **Non applicabile v1:** R06

**Totale rischi tracciati:** 32 (27 aperti + 2 non materializzati + 1 non applicabile v1 + 2 nuovi mitigati [R31, R32]).

Il registro viene rivisto a ogni milestone e dopo ogni Change Request.
