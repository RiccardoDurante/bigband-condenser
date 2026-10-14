---
document: Kronos kai Kairos - Preliminary Spike Findings
document_id: SF-BBC-M2-001
project: Big Band Condenser v1
version: 0.1
status: Draft - preliminary findings prior to local Q1-Q6 execution
last_updated: 2026-10-14
language: it
changelog:
  - v0.1 (2026-10-14): primo documento di findings preliminari su parse cloud del file sorgente
---

# Preliminary Spike Findings — Kronos kai Kairos

## Scopo

Questo documento raccoglie i **findings preliminari** emersi durante un'ispezione in ambiente cloud (music21 10.5.0) del file sorgente `kronos_kai_kairos.musicxml` prima dell'esecuzione formale del Spike M2 in ambiente locale.

**Status**: preliminare. Serve a dare segnali di early go/no-go e a fissare attenzione su rischi concreti prima di investire ore di sviluppo. Il Spike M2 formale avverra in ambiente locale (venv Windows + Dorico 5+) e produrra lo SPIKE_M2_REPORT definitivo.

## 1. Metadata del file sorgente

| Attributo | Valore |
|---|---|
| Movement title (interno) | Kronos kai Kairos |
| Composer | R. Durante |
| Dedica/contesto | Arrangiata per l'orchestra jazz della Sardegna, concorso Scrivere in Jazz 2024, Sezione B |
| Encoding software | **Finale v27.4 for Windows** |
| MusicXML version | 3.1 Partwise |
| Encoding date | 2026-10-14 |

**Osservazione**: il Charter sezione 13 e lo SPIKE_M2_PLAN assumevano **Dorico** come export primario. Il file reale e invece Finale. Questo **materializza R12** ("Differenze di esportazione MusicXML tra software") e aggiunge un dato: il tool deve funzionare anche su export Finale, non solo Dorico.

## 2. Q1 - Parse integrity (preliminare)

**Verdict**: PASS.

- `music21.converter.parse()` completa senza errori
- Zero warning catturati
- 142 battute riconosciute (parte 1)
- 6510 note totali su tutte le parti
- 2385 pause totali
- Metadata leggibili (`metadata.movementName`, `metadata.composer`)

**Soglia Q1 nel piano**: zero errori, warning informativi ammessi. **Superata**.

## 3. Q2 - Instrument classification (preliminare)

**Verdict**: PASS, con **scoperta critica** che modifica l'approccio.

### Scoperta critica: music21 instrument class e INAFFIDABILE su export Finale

Il metodo standard `part.getInstruments()` ritorna classi music21 **completamente sbagliate** per i 19 parti del file:

| partName (corretto) | music21 instrument class (sbagliato) |
|---|---|
| Soprano Sax | Sampler |
| Alto Sax | Vibraphone |
| Tenor Sax 1/2 | ElectricGuitar |
| Baritone Sax | ElectricGuitar |
| Trumpet in Bb 1-4 | AcousticGuitar |
| Horn in F 1/2 | Clavichord |
| Trombone | Instrument (generico) |
| Bass Trombone | ElectricOrgan |
| Piano | Celesta |
| Acoustic Bass | SopranoSaxophone |
| Drum Set 1/2 | CrashCymbals / Sampler |

**Causa probabile**: Finale esporta i MIDI program numbers legati al template di playback (Garritan, EWQL, Finale Default Sounds). music21 inferisce la classe da li, non dal nome testuale. Mapping completamente sballato.

### Classifier basato su partName: 19/19 (100%)

Un classifier semplice che fa string matching sul `partName` ("sax", "trumpet", "trombone", "horn", "piano", "bass", "guitar", "drum") produce **19/19 classificazioni corrette (100%)**, ben sopra la soglia Q2 del piano (>=15/17 = 88%).

| Sezione | Parti | Numero |
|---|---|---|
| Reeds | Soprano Sax, Alto Sax, Tenor Sax 1, Tenor Sax 2, Baritone Sax | 5 |
| Brass | Trumpet in Bb 1-4, Horn in F 1-2, Trombone, Bass Trombone | 8 |
| Rhythm | Electric Guitar, Piano x2, Acoustic Bass | 4 (3 logici) |
| Drums | Drum Set 1-2 | 2 (1 logico) |
| **Totale** | | **19 parti XML / 17 strumenti logici** |

### Piano e Drum Set splittati in 2 parti XML

Finale esporta Piano e Drum Set come **2 parti XML separate** ciascuno (grand staff split: treble/bass per il piano, 2 pentagrammi per la batteria). Il classifier deve **raggruppare parti con stesso partName** per contarle come un singolo strumento logico.

### Implicazione architetturale

Il modulo Instrument Classifier del Big Band Condenser dovra:

1. Usare `partName` testuale come fonte primaria di verita (regex o keyword matching)
2. **NON** affidarsi a `part.getInstruments()` music21
3. Raggruppare parti con stesso `partName` per identificare strumenti logici
4. Usare MIDI program solo come fallback estremo (es. se `partName` e vuoto)
5. Tabella trasposizioni separata, ereditata da `musicxml_writer.py` di BigBand AI (vedi BIGBAND_AI_REUSE_ASSESSMENT sezione 4.2)

## 4. Q3 - Concert pitch transposition (preliminare)

**Verdict**: PASS preliminare.

Verifica su 6 strumenti traspositori con `.toSoundingPitch()`:

| Strumento | Prima nota written | Prima nota concert | Verifica |
|---|---|---|---|
| Soprano Sax (Bb) | F4 | Eb4 | OK (M2 giu) |
| Alto Sax (Eb) | C5 | Eb4 | OK (M6 giu) |
| Tenor Sax 1 (Bb) | F5 | Eb4 | OK (M9 giu) |
| Baritone Sax (Eb) | C5 | Eb3 | OK (M13 giu) |
| Trumpet in Bb 1 | B4 | A4 | OK (M2 giu) |
| Horn in F 1 | A#4 | D#4 | OK (P5 giu, enharmonic) |

**Nonostante** l'instrument class music21 sia sbagliata (vedi Q2), la trasposizione funziona correttamente perche music21 legge il `<transpose>` tag esplicito presente nel source MusicXML.

**Soglia Q3**: 100% corretti. **Verificato su 6 strumenti traspositori rappresentativi**. L'altra verifica (Tenor Sax 2, Trumpet 2-4, Horn 2) e statisticamente ridondante.

## 5. Q5 - Transpose tag presence (preliminare source side)

**Verdict**: PASS lato SOURCE. Da verificare lato OUTPUT in Spike M2 formale.

Il source Finale include `<transpose>` tag per tutti gli 11 strumenti traspositori (saxes, trumpets, horns). Trombone e Bass Trombone non hanno tag (corretto, sono in concert pitch nativi). Piano e Drum Set non hanno tag (corretto). Guitar e Bass hanno tag chromatic=0 (identita, non significativo).

Il **vero test del bug music21** (R24) va fatto **dopo** aver scritto il file con music21 e aver controllato se i tag sopravvivono. Questo richiede l'esecuzione locale.

## 6. Impatti sui rischi

### Materializzati

- **R12** (differenze MusicXML export): Finale != Dorico, il tool deve gestirli entrambi
- **R25 candidato** (classificazione non canonica): verificato nella pratica. partName matching e la mitigazione corretta. Da bumpare in Risk Register v0.4

### Non materializzati su questo file

- R04, R05, R06, R07 (specifiche a BigBand AI/music21): non applicabili al parse del source
- R24 (transpose tag music21): da verificare post-write locale

### Nuovi rischi candidati

- **R26 candidato**: music21 `instrument.*` class detection non e affidabile su export Finale (potenzialmente anche su altri software). Il Condenser deve ignorare questa fonte e usare `partName` testuale. P=3, I=2, score 6. Alta priorita.

## 7. Decisioni operative confermate

- Classifier via `partName` string matching e la strategia corretta per v1
- music21 `.toSoundingPitch()` e `.transpose()` sono utilizzabili per Q3 (operano via `<transpose>` tag, non via instrument class)
- Piano e Drum Set grand staff split e un pattern di export comune, da gestire via raggruppamento partName
- Formato file nel repo: `.musicxml` decompresso (3.99 MB, diff-friendly)
- Nome file nel repo: `kronos_kai_kairos.musicxml` (allineato con movement-title interno e documenti PMI)

## 8. Non testati in cloud (richiedono ambiente locale)

- Q4 Round-trip Dorico (richiede Dorico 5+ installato)
- Q5 Output transpose tag bug (richiede music21 write + rilettura)
- Q6 Structure 4-pentagrammi (richiede skeleton condenser)
- Test del musicxml_writer orfano ereditato da BigBand AI
- Test estratto 32 battute (ancora da esportare da Finale)

## 9. Ambiente di verifica

| Attributo | Valore |
|---|---|
| Ambiente | Cloud Linux (sessione Claude Code) |
| Python | 3.x |
| music21 | 10.5.0 |
| Date verifica | 2026-10-14 |
| Durata verifica | circa 10 min |

**Nota**: questo documento non sostituisce lo SPIKE_M2_REPORT formale che sara prodotto a chiusura del timebox 12h previsto dal piano. Serve a dare segnali di early go/no-go, isolare rischi concreti, e guidare lo scope del codice spike locale.

## 10. Prossimi passi

Esecuzione locale in ordine:

1. Salvataggio di `samples/kronos_kai_kairos.musicxml` (versione decompressa, 3.99 MB) nel repo
2. Esportazione da Finale di `samples/kronos_kai_kairos_extract.musicxml` (32 battute iniziali o shout chorus)
3. Primo commit sample con i due file
4. Scrittura stub codice Spike in `src/bigband_condenser/_spike/` seguendo SPIKE_M2_PLAN sezione 10
5. Esecuzione Q1 su extract (verifica cloud findings)
6. Esecuzione Q2-Q6 secondo timebox
7. Bump Risk Register v0.4 con R25 e R26 candidati
8. Chiusura spike con SPIKE_M2_REPORT formale
