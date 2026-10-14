---
document: Spike M2 Plan
document_id: SP-BBC-M2-001
project: Big Band Condenser v1
version: 0.1
status: Draft - pronto per esecuzione
last_updated: 2026-10-14
language: it
changelog:
  - v0.1 (2026-10-14): prima emissione, piano operativo spike M2 con test case Kronos kai Kairos
---

# Spike M2 Plan - Big Band Condenser v1

## 1. Scopo e definizione di spike

Spike (metodologia agile) = esperimento time-boxed per **ridurre incertezza**, non per produrre deliverable finali. Lo spike M2 risponde a domande specifiche sulla fattibilita tecnica del Condenser, usando codice sperimentale che **non entrera in produzione**.

Lo spike M2 non e M3/M4/M5: non produce un Condenser funzionante, produce **evidenze** per decidere se il piano Charter regge o va ricalibrato.

Riferimento Charter: sezione 6 milestone M2 "Spike di fattibilita su un MusicXML dello Sponsor".

## 2. Domande dello spike

Lo spike deve rispondere a 6 domande binarie. Risposte accettabili: SI / NO / PARZIALE (con descrizione specifica di cosa manca).

### Q1 - Parse integrity

music21 riesce a leggere il MusicXML di "Kronos kai Kairos" senza errori ne warning critici?

- Criterio: ``music21.converter.parse()`` ritorna uno ``Score`` object valido
- Metriche: numero di parti riconosciute, numero di battute, numero totale di note
- Soglia accettabile: zero errori; warning informativi ammessi se non impattano struttura

### Q2 - Instrument classification

Il tool classifica correttamente gli strumenti di "Kronos kai Kairos" nelle 4 sezioni Charter (Reeds / Brass / Rhythm / Drums)?

- Criterio: per ciascuno dei 17 strumenti del brano, verdetto corretto manualmente verificato
- Metriche: accuratezza (classificazioni corrette / 17), elenco strumenti mis-classificati
- Soglia accettabile: >= 15/17 corretti (circa 88%); verra evidenziato se corni F sono gestiti come Brass come atteso

### Q3 - Concert pitch transposition

La trasposizione in concert pitch funziona su tutti gli strumenti traspositori del brano?

- Strumenti traspositori attesi in Kronos: Soprano sax (Bb), Alto sax (Eb), 2 Tenor sax (Bb), Baritone sax (Eb), 4 Trumpet (Bb), 2 Horn in F (F)
- Criterio: per ciascun strumento traspositore, confronto manuale di 5-10 note tra written e concert pitch
- Metriche: numero strumenti con trasposizione corretta / numero strumenti traspositori attesi
- Soglia accettabile: 100% corretti; qualunque errore e bloccante

### Q4 - Round-trip Dorico

music21 scrive un MusicXML che Dorico riapre senza errori strutturali?

- Criterio: load Kronos, trasposizione concert, save con music21, reload del nuovo file in Dorico 5+, verifica apertura senza error dialog
- Metriche: SI / NO + eventuali warning Dorico
- Soglia accettabile: Dorico apre il file; warning tipografici ammessi se contenuto musicale integro

### Q5 - Bug music21 noto (transpose tag)

Il bug noto di music21 (omissione tag ``<transpose>`` in parti multiple stessa classe strumento) si manifesta anche nel nostro caso?

- Riferimento: BIGBAND_AI_REUSE_ASSESSMENT.md sezione 4.2 (musicxml_writer orphan di BigBand AI con workaround ``_fix_missing_transpose_tags``)
- Strumenti test: 2 Tenor sax, 4 Trumpet, 2 Horn in F (tutti classi music21 stessa famiglia)
- Criterio: dopo save con music21, grep nel file XML per ``<transpose>`` in ogni parte traspositoria
- Metriche: tag presente / tag omesso per ciascuna parte potenzialmente affetta
- Soglia accettabile: se bug si manifesta, workaround ereditato risolve

### Q6-minimale - Struttura output 4-pentagrammi

Il tool riesce a produrre un MusicXML output con **struttura** 4 pentagrammi (Reeds grand staff, Brass grand staff, Rhythm grand staff, Drums single staff), anche con contenuto musicale **placeholder** (es. copia di 1 nota per sezione)?

- Criterio: file output ha esattamente 4 parti, numero pentagrammi corretto per parte (2+2+2+1), struttura MusicXML valida W3C
- Metriche: SI / NO + descrizione eventuali devianze
- Soglia accettabile: SI anche con contenuto musicale banale; la **qualita** del contenuto non e in scope M2

**Nota**: Q6-minimale valida la "struttura di output" prevista Charter §3.2. La logica di condensazione musicale vera arriva a M4-M5-M6, non in M2.

## 3. Test case

### Primario (iterazione sviluppo)

**File**: ``samples/kronos_kai_kairos_extract.musicxml``

- Estratto di "Kronos kai Kairos" composto da Riccardo Durante
- Durata: ~32 battute (primo chorus o shout chorus, da scegliere in fase di export)
- Dimensione file attesa: ~100-300 KB
- Scopo: iterazione rapida durante sviluppo spike (parse/transpose/save sotto 1 secondo)

### Validazione finale

**File**: ``samples/kronos_kai_kairos.musicxml``

- Brano intero "Kronos kai Kairos"
- Durata: 6 minuti (~180-240 battute)
- Dimensione file attesa: 0.5-2 MB
- Scopo: test di validazione finale su file realistico completo

### Organico (comune a entrambi)

17 strumenti, non canonici rispetto a big band standard:

| Sezione Charter | Strumenti di Kronos |
|---|---|
| Reeds | Soprano sax, Alto sax, 2 Tenor sax, Baritone sax (5 totali) |
| Brass | 4 Trumpet, 2 Horn in F, Trombone, Bass Trombone (8 totali) |
| Rhythm | Electric Guitar, Piano, Bass (3 totali) |
| Drums | Drum (1 totale) |

**Osservazioni rilevanti per spike**:

- **1 Soprano sax invece di 2 Alto sax**: deviazione dal 5-sax standard (2A/2T/1B). Testa tolleranza a composizione reeds non canonica.
- **2 Horn in F**: strumenti non standard big band jazz, presi da tradizione classica/concert band. Testa classificazione per **categoria strumentale** (ottoni) non per nome standard. Candidato nuovo rischio R25 (vedi sezione 8).
- **1 Trombone + 1 Bass Trombone invece di 3+1 canonici**: tromboni ridotti. Testa tolleranza a numero variabile per sezione (coerente con R10, R11).

### Licenza

Entrambi i file: **CC-BY 4.0**, autore Riccardo Durante.

File di licenza associato: ``samples/kronos_kai_kairos.LICENSE`` con testo CC-BY 4.0 + attribution line.

## 4. Timebox e scope operativo

**Timebox hard**: 12 ore totali, cosi distribuite:

| Attivita | Ore stimate | Dettaglio |
|---|---|---|
| Setup codice spike | 1h | Cartella ``src/bigband_condenser/_spike/`` con ``README.md``, file Python stub, test fixtures |
| Export brano da Dorico (2 file) | 1h | Estratto 32 battute + brano intero, verifica apertura in Dorico |
| Q1 Parse integrity | 1h | Load + inspection stream music21, note metriche |
| Q2 Instrument classification | 2h | Scrivere classifier naive, iterare su strumenti del brano, valutare mis-classifications |
| Q3 Concert pitch transposition | 1.5h | Applicare transpose, verificare manualmente 5-10 note per strumento traspositore |
| Q4 Round-trip Dorico | 1h | Save, reload in Dorico, verifica errori strutturali |
| Q5 Bug transpose tag | 1h | Grep XML, verificare presenza/assenza tag ``<transpose>`` per parti multiple stessa classe |
| Q6-minimale Struttura output | 1.5h | Scrivere skeleton condenser che produce struttura 4 pentagrammi con contenuto placeholder |
| Scrittura report | 1h | ``docs/pmi/SPIKE_M2_REPORT.md`` con risposte Q, metriche, conclusioni |
| Buffer / overhead | 1h | Debug imprevisto, riprese, decisioni |

**Totale**: 12 ore in 2 settimane calendario (fine ottobre 2026 secondo Charter).

**Criterio di stop forzato**: dopo 10h di lavoro effettivo sul codice spike (escludendo scrittura report), chiudere lo spike. Produrre report anche se parzialmente incompleto. Spike NON e lo sviluppo finale.

**Scope creep protection**: durante lo spike, qualunque tentazione di "migliorare" la logica di condensazione musicale va **differita a M4-M6**. Lo spike produce struttura (Q6) non qualita musicale.

## 5. Deliverable M2

### D1 - Report

**File**: ``docs/pmi/SPIKE_M2_REPORT.md``

Struttura attesa:

- Riepilogo esecutivo (1 paragrafo)
- Risposta a ciascuna Q (Q1-Q6) con metriche quantitative
- Problemi incontrati e come sono stati risolti (o non risolti)
- Delta tempo stimato vs reale per ciascuna Q
- Lezioni apprese per M3-M9
- Verdetto finale: ``PASS`` / ``PASS con riserve`` / ``FAIL - serve Change Request``

### D2 - Codice spike

**Directory**: ``src/bigband_condenser/_spike/``

Convenzione:

- Cartella **separata** da ``src/bigband_condenser/`` top-level
- Contiene ``README.md`` che dice esplicitamente "codice sperimentale, da riscrivere in M3-M8 come production code"
- File Python piccoli e monofunzionali: ``parse_test.py``, ``classify_test.py``, ``transpose_test.py``, ``roundtrip_test.py``, ``bug_check.py``, ``structure_test.py``
- Nessun test automatico pytest in questa fase (test manuali guidati)
- Il codice NON e importato dal namespace principale ``bigband_condenser`` (resta isolato)

Il codice spike **non viene mantenuto** dopo M2. Serve solo come traccia storica di cosa e stato esplorato. Potra essere spostato in ``docs/pmi/releases/<data>_M2/spike_code/`` come snapshot archiviato o rimosso definitivamente a discrezione.

### D3 - Decisione formale

Alla fine di M2, scrivere nel CHANGE_LOG una entry D-NNN con una delle tre decisioni:

- **D-A** Procedere con M3 come pianificato (nessuna modifica Charter)
- **D-B** Procedere con M3 ma con ricalibrazione (modifica Charter sezione 6 milestone target e/o stima ore)
- **D-C** Fermare o pivotare il progetto (Change Request formale con motivazione)

## 6. Criteri di successo

Lo spike M2 e dichiarato **PASS** se tutti e tre i criteri sono soddisfatti:

### S1 - Copertura domande

Tutte le 6 Q (Q1-Q5 + Q6-minimale) hanno risposta documentata, anche negativa. Una Q senza risposta e un fallimento di copertura.

### S2 - Delta stime <= 25%

Il delta tra stima Charter (60 ore totali v1) e stima refined post-spike e <= ±25%. Se > 25%, serve Change Request formale per rivedere il piano prima di procedere a M3.

### S3 - Nessuna assunzione Charter residua non verificata

Dopo lo spike, le assunzioni A1 (produttivita BigBand AI trasferibile) e A7 (music21 supporta funzioni MusicXML necessarie) devono avere evidenza concreta di verifica. Le altre (A2/A3/A4) sono gia verificate in BIGBAND_AI_REUSE_ASSESSMENT.md.

Se **tutti e tre** soddisfatti: tag git ``M2-feasibility`` sul commit finale.
Se almeno uno non soddisfatto: M2 "chiuso con riserve", richiede Change Request documentata.

## 7. Rischi specifici per lo spike

Rischi gia nel Risk Register che sono **particolarmente rilevanti** per M2:

- **R01** (produttivita non trasferibile): lo spike e la prima misura reale di produttivita, dati concreti alla chiusura
- **R07** (music21 male multi-staff/slash/drums): Kronos ha drums per 6 minuti, test rappresentativo
- **R10** (doubling reeds): soprano sax e un cambio rispetto allo standard, test di flessibilita
- **R11** (classificazione ritmica ambigua): Kronos ha piano + guitar + bass, test di distinzione
- **R12** (differenze export MusicXML): Kronos esportato da Dorico, baseline del tool
- **R24** (bug music21 transpose tag): Q5 e il check esplicito

## 8. Osservazione per Risk Register futuro (candidato R25)

Durante lo scoping di questo spike e emerso un rischio non ancora formalizzato:

**R25 candidato**: La classificazione strumenti falisce o produce risultati errati su organici non canonici (strumenti opzionali big band come corni F, flicorni, clarinetti doppiati dalle reeds, strumenti classici in context jazz).

- Scenario esempio: Kronos ha 2 Horn in F. Un classifier naive basato su nome standard big band jazz non li riconoscerebbe.
- Mitigazione proposta: tabella classificazione per **categoria strumentale** (reed / brass / rhythm) basata su music21.instrument class hierarchy, non su nome string match
- Priorita: P=2, I=2, score 4 (media)

**Decisione**: non bumpiamo il Risk Register in questa sessione. Il bump sara fatto in sessione successiva insieme a potenziali altri rischi emersi durante lo spike M2 stesso. Registrato qui come osservazione pending.

## 9. Vincoli operativi

- **BigBand AI read-only**: nessuna modifica al progetto donatore durante lo spike. Classi riusabili (NoteData, MelodyData, musicxml_writer orfano) vengono **copiate** nel Condenser con attribuzione, mai importate live.
- **Scope v1**: lo spike NON produce logica di condensazione musicale completa. Q6 valida solo la **struttura** output.
- **Charter §12.1 reference artifact privato**: nessun reference artifact di terzi (es. partiture di maestri sotto copyright) viene elaborato durante lo spike. Kronos e opera dello Sponsor, CC-BY 4.0.
- **Timebox hard 12h**: nessun stretch oltre timebox senza Change Request formale.

## 10. Prossimi passi operativi

Nella prossima sessione, in ordine:

1. **Setup samples/** (cappello Doc Writer): README, licenza CC-BY 4.0, placeholder per i due MusicXML
2. **Export brano da Dorico** (azione Sponsor fuori sessione): esportare estratto 32 battute e brano intero, salvarli in ``samples/``, verificare apertura
3. **Primo commit samples** (cappello Developer): aggiungere brano al repo, commit, push
4. **Scrivere stub code dello spike** (cappello Developer): cartella ``src/bigband_condenser/_spike/``, file Python base
5. **Eseguire Q1** (cappello QA + Developer): parse integrity + metriche
6. **Procedere con Q2-Q6** secondo timebox

Il piano SPIKE_M2_PLAN v0.1 e la baseline. Modifiche saranno tracciate con bump di versione (v0.2 se cambia scope, v0.3 se cambiano criteri).
