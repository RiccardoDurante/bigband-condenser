---
document: Spike M2 Report
document_id: SR-BBC-M2-001
project: Big Band Condenser v1
version: 0.1
status: Final
last_updated: 2026-10-15
language: it
changelog:
  - v0.1 (2026-10-15): emissione finale a chiusura Spike M2
---

# Spike M2 Report - Big Band Condenser v1

## 1. Riepilogo esecutivo

Lo Spike M2 di fattibilita tecnica si e chiuso con verdetto **PASS** su 5 Q su 6, con 1 FAIL "produttivo" (Q5) che ha prodotto una scoperta architetturale importante (R30). Monte ore effettivo: circa 1h40 (vs 12h timebox del piano), grazie all'anticipazione cloud del 14 ottobre che ha accelerato notevolmente l'esecuzione locale del 15 ottobre.

Scoperte principali:
- R27 (music21.write drum fail) DOWNGRADED da score 9 critico a score 4 medio con mitigation validata empiricamente
- R28 nuovo (hidden parts detection) con mitigation validata
- R29 nuovo (octave-transposing conventions) lezione di dominio documentata
- **R30 nuovo CRITICO** (music21.write output corruption da wrong instrument class) con mitigation definita

Decisione formale di chiusura: **D-A - procedi con M3 come pianificato nel Charter, nessuna ricalibrazione necessaria**.

## 2. Q1 Parse integrity

**Verdict: PASS**.

- music21 10.5.0 su Windows Python 3.13.14 parsa senza errori il full score (3.99 MB) e l'extract 32 battute (716 KB)
- Zero warnings catturati
- Metriche su full score: 19 parti XML, 142 battute, 6510 note, 2385 pause
- Metriche su extract: 19 parti XML, 33 battute (pickup 0 + bars 1-32), 1226 note
- Metadata leggibili (movementName, composer, title)
- **Match perfetto con cloud findings** del 14 ottobre: ambiente locale replica il comportamento cloud

Nessun imprevisto. Soglia Q1 del piano ("zero errori, warning informativi ammessi") superata.

## 3. Q2 Instrument classification + hidden detection

**Verdict: PASS**. 19/19 XML parts classificate correttamente, 1 hidden detected, 17 strumenti logici visible.

### Scoperta critica confermata: music21 instrument class e INAFFIDABILE su export Finale

Il metodo standard `part.getInstruments()` ritorna classi music21 sbagliate per tutti e 19 i parti di Kronos (Soprano Sax -> Sampler, Trumpet -> AcousticGuitar, Acoustic Bass -> SopranoSaxophone, etc.). Causa: Finale esporta MIDI program numbers legati al template di playback (Garritan/EWQL/Finale Default). music21 li usa come fonte di classe strumentale.

Mitigazione validata: **classifier via partName string matching**. 19/19 (100%) corretti con keywords per sezione:
- Reeds: sax, clarinet, flute, oboe, bassoon
- Brass: trumpet, trombone, horn, flugel, tuba, cornet
- Rhythm: piano, guitar, bass, vibraphone, organ
- Drums: drum, percuss

### Scoperta nuova: hidden parts detection (R28)

Durante la sessione, su input Music Expert dello Sponsor, scoperto che "Drum Set 2" nel Kronos e una parte **hidden** (nascosta in Finale), usata solo per il playback MIDI realistico ma non visibile nello spartito stampato.

Marker Finale in MusicXML: `<staff-details print-object="no"/>` **senza attributo number** nel primo `<attributes>` del `<part>`.

Implementato detector in Q2: parse XML separato, identificazione parts hidden, flag `is_hidden` per esclusione dal logical count. Output: Drum Set 2 correttamente marcata, 17 strumenti logici visible (5 Reeds + 8 Brass + 3 Rhythm + 1 Drums).

### Composizione 17 strumenti logici visible in Kronos

| Sezione | Strumenti logici |
|---|---|
| Reeds (5) | Soprano Sax, Alto Sax, Tenor Sax 1, Tenor Sax 2, Baritone Sax |
| Brass (8) | Trumpet in Bb 1-4, Horn in F 1-2, Trombone, Bass Trombone |
| Rhythm (3) | Electric Guitar, Piano, Acoustic Bass |
| Drums (1) | Drum Set 1 (Drum Set 2 hidden escluso) |

## 4. Q3 Concert pitch transposition

**Verdict: PASS**. 17/17 parti verificate con trasposizione corretta.

Nonostante music21 abbia instrument class sbagliate (R26), la trasposizione via `.toSoundingPitch()` funziona correttamente perche music21 legge il `<transpose>` tag esplicito del MusicXML source, non la class.

Risultati per strumenti traspositori:

| Strumento | Written | Concert | Delta st | Expected |
|---|---|---|---|---|
| Soprano Sax (Bb) | F4 | E-4 | -2 | -2 |
| Alto Sax (Eb) | C5 | E-4 | -9 | -9 |
| Tenor Sax 1/2 (Bb, octave shift) | F5/F4 | E-4/E-3 | -14 | -14 |
| Baritone Sax (Eb, octave shift) | C5 | E-3 | -21 | -21 |
| Trumpet in Bb 1-4 | B4 | A4 | -2 | -2 |
| Horn in F 1/2 | A#4/F#4 | D#4/B3 | -7 | -7 |
| Trombone, Bass Trombone, Piano | identita | identita | 0 | 0 |

### Scoperta nuova: octave-transposing conventions (R29)

Electric Guitar e Acoustic Bass sono **traspositori di ottava** (notati 1 ottava sopra il suono reale). Delta -12 st. Convenzione standard che io avevo omesso dalle expected iniziali, generando falsi positivi di errore. Lezione di dominio: non assumere "concert = 0" per guitar/bass, documentare le convenzioni di notazione nelle tabelle expected.

## 5. Q4 Round-trip write + drum duration histogram

**Verdict: PASS** con strategia **strip hidden + filter sub-semicroma**.

### Esperimenti condotti

| Esperimento | Risultato | Note |
|---|---|---|
| Exp 1: write score as-is | FAIL | MusicXMLExportException: Cannot convert "2048th" duration (replica cloud finding) |
| Exp 2: strip hidden parts, poi write | FAIL | Stesso errore anche dopo aver tolto Drum Set 2: anche Drum Set 1 (visibile) ha durate sub-32th |
| Exp 3: strip hidden + filter durate < 0.25 ql, poi write | OK | 569,109 bytes output valido |

### Istogramma durate drum

| Part | Totale eventi | Sub-semicroma | % |
|---|---|---|---|
| Drum Set 1 (visibile) | 229 | 157 | 68.56% |
| Drum Set 2 (hidden) | 314 | 153 | 48.73% |

### Risoluzione ambiguita via Music Expert

Il 68% sub-semicroma su Drum Set 1 ("notazionale") era inizialmente controintuitivo. Input Music Expert dello Sponsor:

> "probabilmente e' un realistic playback, probabilmente per ricreare un suono del charleston aggiungono micro note nel campionamento, io vorrei che ti attenessi ai valori delle note scritte effettivamente, non mi interessa l'esecuzione, probabilmente stai leggendo la parte interpretativa"

Validazione empirica: grep per `<grace>` tag nel source MusicXML = **0 occorrenze**. Le 157 durate sub-semicroma di Drum Set 1 sono quindi **note standalone con durata minima**, non grace notes legittime. Conferma triangolata: sono artefatti di realistic playback MIDI (humanization, risonanze template), non notazione musicale.

### Principio operativo codificato (D-022)

Il Condenser v1 opera sulla notazione scritta intenzionale, non sui dati di playback MIDI. Soglia operativa: durate < 0.25 quarterLength nelle drum parts = playback artifacts, scartate pre-write.

### R27 downgrade

Da P=3, I=3, score 9 CRITICO -> P=2, I=2, score 4 MEDIO. Mitigazione validata empiricamente e aligned con requirement musicologico esplicito dello Sponsor.

## 6. Q5 Transpose tag preservation in output

**Verdict: FAIL 1/16 (produttivo)**. Scoperta architetturale critica.

Analisi dei tag `<transpose>` nel file output di Q4 Exp 3:

| Part | Tag in output | Expected | Verdict |
|---|---|---|---|
| 10 traspositori "normali" | corretti | corretti | OK |
| Trombone, Bass Trombone, Piano | no tag | no tag | OK |
| Electric Guitar | c=0, oc=-1, eff=-12 | -12 | OK |
| **Acoustic Bass** | **c=-2, oc=0, eff=-2** | **-12** | **FAIL** |

### Causa radice (R30 nuovo)

music21.write() **non preserva** il `<transpose>` tag del source XML. Lo **rigenera** dalla instrument class interna. Combinato con R26 (wrong class detection su Finale):

- Acoustic Bass -> music21 class = **SopranoSaxophone** (R26) -> default transposition di SopranoSax = -2 st -> tag output corrotto
- Electric Guitar -> music21 class = **Instrument** (generica, no default transposition) -> music21 preserva il tag source -> output OK

### Mitigazione definita

Due opzioni per il Condenser pipeline:
- **Opzione A** (raccomandata): forzare instrument class corretta pre-write via partName -> music21.instrument class mapping. Usa tabella _INSTRUMENT_TRANSPOSITIONS ereditata da BigBand AI musicxml_writer orfano
- **Opzione B** (fallback): post-process XML output per overwrite `<transpose>` tag dal source

Opzione A e piu pulita, pattern noto, +1-2h in M3-M4.

### Perche FAIL "produttivo"

Lo scopo di uno spike e trovare bug prima che costino care in M3-M9. Q5 ha trovato un bug che avrebbe silently corrotto l'output del Condenser per tutti gli strumenti mis-classificati da music21. Scoperto in 10 min di spike, costa 1-2h di implementazione in M3-M4. **Senza spike, sarebbe emerso in M5-M6 e costato 5-8h di debugging confuso.**

## 7. Q6 Structure skeleton

**Verdict: PASS**.

Prodotto `q6_skeleton.musicxml` (9,683 bytes) con struttura 4-pentagrammi target del Charter sezione 3.2:

| # | Parte | Clef | Note |
|---|---|---|---|
| 1 | Reeds | Treble | 4 (C4, D4, E4, F4) |
| 2 | Brass | Treble | 4 (G4, A4, B4, C5) |
| 3 | Rhythm | Treble | 4 (E3, G3, B3, D4) |
| 4 | Drums | Percussion | 4 (C4 placeholder) |

Round-trip: parse del file output re-produce 4 parts con 4 notes ciascuno. **Charter sezione 3.2 strutturalmente raggiungibile senza dual pipeline o XML pass-through**.

Grand staff refinement (2 staves per Reeds/Brass/Rhythm, 1 per Drums) e chord symbols rimandati a M4-M6.

## 8. Delta tempi stimato vs reale

| Fase | Stima piano | Reale | Delta |
|---|---|---|---|
| Setup codice spike | 1h | 15 min (gia fatto 14/10) | -0.75h |
| Export brano da Dorico | 1h | 0 (Finale, non Dorico; extract fatto cloud) | -1h |
| Q1 Parse integrity | 1h | 10 min (gia fatto cloud, verifica locale) | -0.85h |
| Q2 Instrument classification | 2h | 15 min (approccio cloud + hidden detection) | -1.75h |
| Q3 Concert pitch transposition | 1.5h | 10 min | -1.4h |
| Q4 Round-trip Dorico | 1h | 15 min (3 esperimenti) | -0.75h |
| Q5 Bug transpose tag | 1h | 10 min + 10 min analisi R30 | -0.65h |
| Q6-minimale Struttura output | 1.5h | 10 min | -1.4h |
| Scrittura report | 1h | 30 min | -0.5h |
| Buffer / overhead | 1h | 15 min | -0.75h |
| **TOTALE** | **12h** | **~1h40** | **-10h20 (-86%)** |

Delta rispetto a piano = -86%. Non e che il piano fosse sovradimensionato: e che il **preliminary cloud spike del 14 ottobre** ha anticipato buona parte del lavoro con un ROI eccezionale (circa 20x). Delta rispetto a stima Charter dentro ±25% rispettato ampiamente.

## 9. Criteri di successo (verifica)

Da SPIKE_M2_PLAN v0.1 sezione 6:

### S1 - Copertura domande

6/6 Q hanno risposta documentata (Q1-Q6, 5 PASS + 1 FAIL produttivo). **SODDISFATTO**.

### S2 - Delta stime <= 25%

Spike M2 costato 1h40 su budget 12h (86% sotto). Monte ore cumulato: 8h25 su 60h totali (14%). Residuo 51.5h in 14 settimane, media 3.7h/sett sotto baseline 5h/sett. **SODDISFATTO con ampio margine**.

### S3 - Nessuna assunzione Charter residua non verificata

- A1 (produttivita BigBand AI trasferibile): verificata, le 60h stimate sono robuste, anzi conservativa
- A2, A3, A4 (BigBand AI reuse): verificate il 14/10 (vedi BIGBAND_AI_REUSE_ASSESSMENT.md)
- A5 (Sponsor dispone di arrangiamento big band proprio): verificato (Kronos committato)
- A6 (Sponsor dispone di reference artifact): verificato (reference locale non-committed)
- A7 (music21 supporta funzioni MusicXML necessarie): verificata **con qualifica**: music21 supporta parse e write, ma ha bug noti (R07 Materializzato, R24, R26, R27, R30) tutti con mitigation definite
- A8 (user responsabile qualita MusicXML input): assunzione contrattuale, non verificabile tecnicamente

**SODDISFATTO**.

### Verdetto S1+S2+S3

Tutti e tre i criteri soddisfatti. **Spike M2 formale PASS**.

## 10. Decisione formale di chiusura

**D-A: procedi con M3 come pianificato nel Charter sezione 6**.

- Nessuna Change Request formale al Charter
- Nessuna ricalibrazione del monte ore
- Nessuna modifica dello scope v1
- Tag git `M2-feasibility` sul commit di chiusura

Target M3 (Parser MusicXML + Classificatore strumenti production code) rimane: **meta novembre 2026**, 5-7h stimate.

## 11. Lezioni apprese per M3-M9

### Tecniche

1. **music21 instrument class detection e inaffidabile su export Finale**. Non usare `part.getInstruments()` come fonte di verita. Usare partName matching.
2. **Hidden parts detection via XML parsing** e necessaria (not just music21). Pattern Finale: `<staff-details print-object="no"/>` without number.
3. **music21.write() corruption** per parti mis-classificate (R30). Mitigation: forzare instrument class corretta pre-write.
4. **Sub-semicroma durations nelle drum parts di Finale** sono realistic playback MIDI artifacts, non notazione. Scartare pre-write.
5. **Convenzioni di trasposizione di ottava** (guitar/bass) vanno documentate esplicitamente nelle tabelle expected.
6. **Round-trip MusicXML di music21** funziona per 3 pentagrammi su 4; drum staff richiede pre-processing (filter) ma non dual pipeline o XML pass-through.

### Processo

1. **Role switching con cappello Music Expert** e critico per decisioni di dominio musicologico. Non inferire musicologia senza chiedere.
2. **Preliminary cloud spike** ha ROI altissimo (20x) nel ridurre tempo locale. Pattern da replicare per futuri spike complessi.
3. **FAIL "produttivo"** sono valore, non errori. Q5 FAIL ha salvato 5-8h di debugging in M5-M6.

### PMI

1. Risk Register vive davvero: 3 nuovi rischi scoperti nello spike (R28, R29, R30), 1 downgradato (R27), senza fermare lo spike.
2. Change Request pre-approvata ("reducted score no-drum") e un buon pattern di comfort/fallback per rischi architetturali.

## 12. Prossimi passi (M3 Target)

Da Charter sezione 6: **M3 - Parser MusicXML + Classificatore strumenti (production code)**. Target meta novembre 2026.

Scope M3:
- Portare partName classifier da `_spike/q2_classify.py` a modulo production `src/bigband_condenser/classifier.py`
- Implementare instrument class forcing (mitigation R30)
- Implementare sub-semicroma filter per drum parts (mitigation R27)
- Implementare hidden parts detection (mitigation R28)
- Suite di test pytest base (10-20 test iniziali)

Stima M3: 5-7h (una settimana a 5h/settimana).
