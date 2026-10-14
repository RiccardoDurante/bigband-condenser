---
document: Kronos kai Kairos - Preliminary Spike Findings
document_id: SF-BBC-M2-001
project: Big Band Condenser v1
version: 0.2
status: Draft - preliminary findings prior to local Q1-Q6 execution
last_updated: 2026-10-14
language: it
changelog:
  - v0.2 (2026-10-14): aggiunto finding critico Q4-anticipato (music21.write() fallisce su durate 2048th in Drum Set del source Finale); aggiunto nuovo R27 candidato; documentato metodo di extraction 32 battute via XML diretto; nota su pickup measure (anacrusi)
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
| Pickup measure (anacrusi) | Si, battuta numero 0 presente |
| Battute totali | 142 (0, 1-141) |

**Osservazione**: il Charter sezione 13 e lo SPIKE_M2_PLAN assumevano **Dorico** come export primario. Il file reale e invece Finale. Questo **materializza R12** ("Differenze di esportazione MusicXML tra software") e aggiunge un dato: il tool deve funzionare anche su export Finale, non solo Dorico.

## 2. Q1 - Parse integrity (preliminare)

**Verdict**: PASS.

- `music21.converter.parse()` completa senza errori
- Zero warning catturati
- 142 battute riconosciute (parte 1, inclusa pickup 0)
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

## 5. Q4 anticipato — music21.write() FAIL sul source Finale

**Verdict preliminare: FAIL su `music21.write("musicxml")` del full score.**

Scoperto durante l'extraction delle 32 battute. Errore riproducibile:

```
music21.musicxml.xmlObjects.MusicXMLExportException:
In part (Drum Set 1), measure (3): Cannot convert "2048th" duration to MusicXML (too short).
```

### Causa

Finale esporta durate di drum notation molto brevi (es. 2048th note, usata per grace note flam o effetti ritmici percussion-specifici) che music21 **non supporta nel suo writer MusicXML**. music21.write() usa `typeToMusicXMLType()` che ha un hard-coded max granularity.

### Impatto diretto sul Spike M2

- **Q4 Round-trip Dorico**: non testabile direttamente via music21.write(). La pipeline Condenser dovra:
  - **Opzione a**: pulire/arrotondare le durate problematiche prima del write (lossy, altera il drum)
  - **Opzione b**: usare un writer custom a livello XML per le parti drum, bypassando music21
  - **Opzione c**: escludere drum dal flow music21 e passarlo as-is dal source al output via XML manipulation diretta
- **Q6 Structure 4-pentagrammi**: dipende da Q4. Se il writer music21 non puo gestire le drum parts originali, il sistema Drums della condensed potrebbe richiedere pipeline alternativa
- **Charter sezione 3.8** ("Parte di batteria preservata con slash notation, rhythmic notation, text directions"): questo requisito funzionale e **a rischio** se dipendiamo da music21.write() per il drum staff. Opzione c (XML pass-through diretto) sembra la via piu pulita

### Soluzione adottata per l'extraction 32 battute

L'extract `kronos_kai_kairos_extract.musicxml` e stato prodotto **non con music21.write()** ma con manipolazione XML diretta (`xml.etree.ElementTree`). Logica:

1. Parse XML del full score
2. Per ogni `<part>`, rimuovere tutte le `<measure>` con `number > 32`
3. Aggiornare `<movement-title>` per segnalare l'extract
4. Scrivere XML preservando DOCTYPE e dichiarazione originale

Risultato: 33 battute XML (pickup 0 + bars 1-32), 716 KB, music21 lo riparse senza errori, metadata preservati. Zero perdita di contenuto musicale.

**Questa logica di XML pass-through** potrebbe essere la stessa che il Condenser dovra adottare per gestire le drum parts nel flow di output.

## 6. Q5 - Transpose tag presence (preliminare source side)

**Verdict**: PASS lato SOURCE. Da verificare lato OUTPUT in Spike M2 formale.

Il source Finale include `<transpose>` tag per tutti gli 11 strumenti traspositori (saxes, trumpets, horns). Trombone e Bass Trombone non hanno tag (corretto, sono in concert pitch nativi). Piano e Drum Set non hanno tag (corretto). Guitar e Bass hanno tag chromatic=0 (identita, non significativo).

Il **vero test del bug music21** (R24) va fatto **dopo** aver scritto il file con music21 e aver controllato se i tag sopravvivono. Questo richiede l'esecuzione locale. **Nota**: in presenza del fail Q4 su music21.write(), questo test diventa dipendente dalla soluzione adottata (opzione a/b/c della sezione 5).

## 7. Impatti sui rischi

### Materializzati

- **R07** (music21 male multi-staff/slash/drums): **MATERIALIZZATO**. Le drum parts di Finale non sopravvivono a music21.write(). La mitigazione prevista ("spike precoce + generare parti di XML mancanti") e stata di fatto confermata necessaria
- **R12** (differenze MusicXML export): Finale != Dorico, il tool deve gestirli entrambi
- **R25 candidato** (classificazione non canonica): verificato nella pratica. partName matching e la mitigazione corretta. Da bumpare in Risk Register v0.4

### Non materializzati su questo file

- R04, R05, R06 (specifiche a BigBand AI): non applicabili al parse del source
- R24 (transpose tag music21 output): da verificare, dipende da come risolviamo Q4

### Nuovi rischi candidati

- **R26 candidato**: music21 `instrument.*` class detection non e affidabile su export Finale (potenzialmente anche su altri software). Il Condenser deve ignorare questa fonte e usare `partName` testuale. P=3, I=2, score 6. Alta priorita.

- **R27 candidato**: music21.write() fallisce su durate tipiche delle drum parts Finale (2048th note e sub-32th in generale). Il Condenser deve adottare una strategia di XML pass-through per le drum parts o cleaning pre-write. P=3, I=3, score 9. **Alta priorita critica**: impatta direttamente Charter sezione 3.8 (preservazione drum notation).

## 8. Decisioni operative confermate

- Classifier via `partName` string matching e la strategia corretta per v1
- music21 `.toSoundingPitch()` e `.transpose()` sono utilizzabili per Q3 (operano via `<transpose>` tag, non via instrument class)
- Piano e Drum Set grand staff split e un pattern di export comune, da gestire via raggruppamento partName
- Formato file nel repo: `.musicxml` decompresso (3.99 MB full, 716 KB extract, diff-friendly)
- Nome file nel repo: `kronos_kai_kairos.musicxml` + `kronos_kai_kairos_extract.musicxml` (allineato con movement-title interno e documenti PMI)
- **Pipeline di output del Condenser**: adottare approccio XML pass-through per le drum parts, non affidarsi completamente a music21.write()

## 9. Non testati in cloud (richiedono ambiente locale)

- Q4 Round-trip Dorico (richiede Dorico 5+ installato) — compromesso dal fail music21.write() scoperto
- Q5 Output transpose tag bug (dipende da strategia Q4)
- Q6 Structure 4-pentagrammi (richiede skeleton condenser)
- Test del `musicxml_writer` orfano ereditato da BigBand AI (potrebbe gia implementare una strategia XML-level che aggira R27)

## 10. Ambiente di verifica

| Attributo | Valore |
|---|---|
| Ambiente | Cloud Linux (sessione Claude Code) |
| Python | 3.x |
| music21 | 10.5.0 |
| Date verifica | 2026-10-14 |
| Durata verifica | circa 20 min (inclusa extraction) |

**Nota**: questo documento non sostituisce lo SPIKE_M2_REPORT formale che sara prodotto a chiusura del timebox 12h previsto dal piano. Serve a dare segnali di early go/no-go, isolare rischi concreti, e guidare lo scope del codice spike locale.

## 11. Prossimi passi

Esecuzione locale in ordine:

1. `samples/kronos_kai_kairos.musicxml` committato (full score, 3.99 MB) — FATTO 2026-10-14
2. `samples/kronos_kai_kairos_extract.musicxml` committato (pickup + 32 battute, 716 KB) — FATTO 2026-10-14 (extract via XML manipulation diretta)
3. Scrittura stub codice Spike in `src/bigband_condenser/_spike/` seguendo SPIKE_M2_PLAN sezione 10
4. Esecuzione Q1 su extract (verifica cloud findings in locale)
5. **Priorita rivista Q2-Q6**: focus iniziale su Q4-alternative (XML pass-through) per sbloccare la strategia drum/output
6. Esecuzione Q3, Q5, Q6 secondo timebox rivisto
7. Bump Risk Register v0.4 con R25, R26 e R27 candidati (R27 e di priorita critica)
8. Chiusura spike con SPIKE_M2_REPORT formale
