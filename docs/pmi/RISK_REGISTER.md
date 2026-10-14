---
document: Risk Register
document_id: RR-BBC-001
project: Big Band Condenser v1
version: 0.4
status: Draft
last_updated: 2026-10-14
language: it
changelog:
  - v0.4 (2026-10-14): R07 e R12 passati a "Materializzato" dopo evidenza empirica dallo spike cloud; aggiunti R26 (music21 instrument class inaffidabile su export Finale) e R27 (music21.write fallisce su drum sub-32th durations tipiche Finale, priorita critica); evidenze documentate in KRONOS_KAI_KAIROS_FINDINGS.md v0.2
  - v0.3 (2026-10-14): aggiornati R04/R05/R06 a stato "Non materializzato" o "Non applicabile v1" dopo verifica assunzioni Charter (vedi BIGBAND_AI_REUSE_ASSESSMENT.md); aggiunto R24 (bug music21 noti su transpose tag in parti multiple stessa classe strumento) con mitigazione gia ereditata da musicxml_writer orfano
  - v0.2 (2026-10-12): aggiunto R23 (qualita MusicXML in input da OMR o export sporchi) nella categoria Qualita; aggiornata sintesi
  - v0.1 (2026-10-12): prima emissione, 22 rischi
---

# Risk Register - Big Band Condenser v1

**Scala.** Probabilita (P) e Impatto (I) da 1 (basso) a 3 (alto). Punteggio = P x I (1-9). Priorita: 6-9 alta, 3-4 media, 1-2 bassa.
**Stato:** Aperto / In monitoraggio / Mitigato / Materializzato / Non materializzato / Non applicabile v1 / Chiuso.
**Responsabile:** salvo diversa indicazione, lo Sponsor/PM (cappello Risk Officer).

| ID | Categoria | Rischio | P | I | Punt. | Risposta e mitigazione | Stato |
|---|---|---|---|---|---|---|---|
| R01 | Pianificazione | La produttivita osservata su BigBand AI non si trasferisce e le 60 ore previste sono sottostimate | 2 | 3 | 6 | Verifica nelle prime 2 settimane (spike M2); ristimare con dati reali; se necessario Change Request su scope o data | Aperto |
| R02 | Pianificazione | La deadline del 31/01/2027 non viene rispettata | 2 | 2 | 4 | Buffer del 25% (circa 15 ore); monitoraggio settimanale di ore e milestone; priorita ai requisiti essenziali | Aperto |
| R03 | Pianificazione | Disponibilita dello Sponsor inferiore a 5 ore/settimana per impegni esterni | 2 | 2 | 4 | Sessioni brevi e frequenti; STATUS.md per ripartire senza perdere contesto; revisione del piano a ogni milestone | Aperto |
| R04 | Tecnico | ``shared/models.py`` di BigBand AI e troppo legato al flusso generativo per essere riusato | 2 | 1 | 2 | Verifica come prima attivita del primo sprint; in caso negativo copiare solo la parte generica o definire modelli nuovi | Non materializzato (verifica 14/10/2026: NoteData e MelodyData generiche e riusabili, WriteRequest specifica scartabile; vedi BIGBAND_AI_REUSE_ASSESSMENT.md sezione 2) |
| R05 | Tecnico | ``chord_scales.py`` non e utilizzabile come parser standalone | 2 | 1 | 2 | Isolare le dipendenze prima del riuso; alternativa: parser dedicato basato su ``music21.harmony`` | Non materializzato (verifica 14/10/2026: file autosufficiente, dipendenze solo stdlib + music21, parser robusto con fallback; vedi BIGBAND_AI_REUSE_ASSESSMENT.md sezione 3) |
| R06 | Tecnico | ``dorico_bridge/`` incompatibile con la versione di Dorico installata | 1 | 3 | 3 | Verifica precoce; il flusso primario resta l'importazione manuale del MusicXML, il bridge e facoltativo | Non applicabile v1 (verifica 14/10/2026: bridge WebSocket fuori scope v1, non verra usato; se mai riattivato in fase futura, R06 va riaperto; vedi BIGBAND_AI_REUSE_ASSESSMENT.md sezione 4.1) |
| R07 | Tecnico | music21 gestisce male scrittura multi-staff, slash notation o notazione di batteria | 2 | 3 | 6 | Spike precoce su questi tre casi; se necessario generare direttamente parti di XML mancanti | **Materializzato (verifica 14/10/2026 cloud spike: music21.write("musicxml") fallisce su Drum Set 1 battuta 3 con "Cannot convert 2048th duration to MusicXML". Mitigazione: adottare strategia XML pass-through per drum parts, ereditando il pattern di ``_fix_missing_transpose_tags`` da musicxml_writer orfano di BigBand AI; vedi KRONOS_KAI_KAIROS_FINDINGS.md sezioni 5 e 7)** |
| R08 | Tecnico | Il rilevatore comping/shout non converge sui casi borderline | 2 | 2 | 4 | Soglie parametrizzabili da CLI; metriche separate; override manuale; casi borderline documentati | Aperto |
| R09 | Tecnico | Chord symbols duplicati o in conflitto tra piano e chitarra | 2 | 1 | 2 | Regola di precedenza documentata (piano prima, chitarra come fallback); test dedicati | Aperto |
| R10 | Tecnico | Doubling nelle reeds (cambi di strumento) gestiti in modo errato | 2 | 2 | 4 | Trattare ogni parte come sequenza di strumenti; test con casi di doubling; classificazione per esecutore e non solo per strumento | Aperto |
| R11 | Tecnico | Assegnazione ambigua degli strumenti della sezione ritmica (piano, chitarra, basso) | 2 | 2 | 4 | Tabella di classificazione esplicita e documentata; parametro di override | Aperto |
| R12 | Tecnico | Differenze di esportazione MusicXML tra software (Dorico, Sibelius, Finale, MuseScore) | 3 | 2 | 6 | Dichiarare in v1 il supporto garantito per l'esportazione di Dorico; testare gli altri come best effort | **Materializzato (verifica 14/10/2026: file test case Kronos kai Kairos esportato da Finale v27.4, non Dorico. Il tool deve ora gestire Finale come primo caso di studio concreto. Charter sezione 13 va aggiornata in sessione futura per riflettere realta: Finale come primo tier supportato oltre Dorico. R26 e R27 scoperti sono conseguenze dirette)** |
| R13 | Qualita | Il materiale di test (MusicXML big band di proprieta dello Sponsor o di pubblico dominio) e insufficiente | 2 | 2 | 4 | Brani di test scritti apposta (anche brevi); eventuale uso del motore di BigBand AI per generare input controllati | Aperto |
| R14 | Qualita | Qualita musicale della condensed non adeguata, pur con output tecnicamente valido | 2 | 2 | 4 | Valutazione dello Sponsor su scala 1-5; convenzioni derivate dai reference; iterazioni brevi | Aperto |
| R15 | Scope | Scope creep (analisi, kick-over, interfaccia web, altri organici) | 3 | 3 | 9 | Scope Statement e Charter vincolanti; ogni richiesta passa per Change Request; idee in roadmap, non nel backlog attivo | Aperto |
| R16 | Scope | Modifiche non autorizzate a BigBand AI per comodita del nuovo progetto | 2 | 3 | 6 | Policy di sola lettura; eventuali modifiche via Change Request nel progetto donatore | Aperto |
| R17 | Legale | Reference di terzi o repertorio sotto copyright finiscono nel repository pubblico | 1 | 3 | 3 | Reference in cartella locale esclusa da Git (``.gitignore``); controllo pre-commit; test pubblici solo con materiale proprio o di pubblico dominio | Aperto |
| R18 | Risorse | I limiti d'uso del piano Claude Pro rallentano il lavoro nei periodi intensi | 2 | 2 | 4 | Sessioni focalizzate; contesto minimo nel Project; lavoro offline (test, documenti) nei periodi di limite; pianificare i task a piu alto consumo con anticipo | Aperto |
| R19 | Risorse | Errori o perdita di contesto dovuti al copia/incolla manuale e a sessioni distinte | 2 | 2 | 4 | STATUS.md a fine sessione; Claude Project con documenti autoritativi; commit frequenti; verifica con i test prima di procedere | Aperto |
| R20 | Costi | Superamento del budget di 200 EUR (cambi di piano o prezzi, spese impreviste) | 1 | 2 | 2 | Voci di spesa limitate al piano Pro; riserva di circa 120 EUR; nessun acquisto senza Change Request | Aperto |
| R21 | Fornitori | Anthropic modifica piani, limiti o prezzi durante il progetto | 1 | 2 | 2 | Documentazione e codice indipendenti dallo strumento; possibilita di proseguire con lavoro manuale | Aperto |
| R22 | Processo | L'overhead documentale (PMI, PDF, versioning) sottrae ore allo sviluppo | 2 | 2 | 4 | Documenti compatti; PDF solo ai milestone; Change Log solo per decisioni significative | Aperto |
| R23 | Qualita | Qualita MusicXML in input (da OMR o export sporchi di software terzi) genera output di bassa qualita che l'utente puo attribuire al tool | 2 | 2 | 4 | README chiaro sui requisiti di input; validator di input con messaggi diagnostici informativi; disclaimer sulla responsabilita della qualita del MusicXML sorgente (Charter sezione 11.8); supporto garantito per export Dorico, altri best effort (R12) | Aperto |
| R24 | Tecnico | Bug music21 noti (es. transpose tag omesso in parti multiple con stessa classe strumento) impattano la qualita dell'output MusicXML | 2 | 2 | 4 | Workaround XML post-processing gia ereditato da ``musicxml_writer.py`` di BigBand AI (funzione ``_fix_missing_transpose_tags``); test di regressione su parti multiple stessa classe strumento (es. Trumpet 1/2/3/4); monitorare issue tracker music21 per fix upstream | Aperto |
| R25 | Tecnico | La classificazione strumenti fallisce su organici non canonici (strumenti opzionali big band come corni F, flicorni, clarinetti doppiati dalle reeds, strumenti classici in context jazz) | 2 | 2 | 4 | Tabella classificazione per **categoria strumentale** (reed / brass / rhythm) basata su partName string matching, non su music21.instrument class hierarchy. Verifica Kronos 14/10/2026: approccio partName matching funziona 19/19 (100%) su organico non canonico (con soprano sax e 2 corni in F) | Aperto - prima evidenza positiva su Kronos |
| R26 | Tecnico | music21 ``instrument.*`` class detection NON e affidabile su export Finale (potenzialmente anche su altri software): tutti e 19 i parti di Kronos classificati con classi music21 completamente sbagliate (Soprano Sax -> Sampler, Trumpet -> AcousticGuitar, Acoustic Bass -> SopranoSaxophone, etc.). Causa: Finale esporta MIDI program numbers legati al template di playback, music21 li usa come fonte di classe strumentale | 3 | 2 | 6 | Il Condenser Instrument Classifier NON deve usare ``part.getInstruments()`` come fonte di verita. Usare partName testuale (string matching su "sax", "trumpet", "trombone", "horn", "piano", "bass", "guitar", "drum"). MIDI program solo come fallback estremo. Approccio verificato empiricamente al 100% su Kronos. Vedi KRONOS_KAI_KAIROS_FINDINGS.md sezione 3 | Aperto - mitigazione validata su Kronos |
| R27 | Tecnico | music21.write("musicxml") FALLISCE su durate drum sub-32th tipiche di export Finale (es. 2048th note usate per grace note flam o effetti ritmici drum-specifici). Errore riproducibile: "Cannot convert 2048th duration to MusicXML (too short)". Impatta direttamente Charter sezione 3.8 (preservazione drum notation con slash + rhythmic notation + text directions compositore) | 3 | 3 | 9 | **PRIORITA CRITICA**. Il Condenser output pipeline deve adottare strategia **XML pass-through** per le drum parts: non riscrivere via music21.write(), ma copiare le ``<measure>`` del drum staff direttamente dal source MusicXML al output tramite ``xml.etree.ElementTree`` o lxml. Il pattern e gia dimostrato nel ``musicxml_writer.py`` orfano di BigBand AI (funzione ``_fix_missing_transpose_tags`` fa XML post-process). Possibile Change Request su Charter sezione 3.8 per clarificare approccio architetturale. Vedi KRONOS_KAI_KAIROS_FINDINGS.md sezione 5 | Aperto - mitigazione definita, da implementare in M2/M3 |

## Sintesi

- **Priorita critica (9) in corso:** R15 (scope creep), **R27 (music21.write drum fail)** [NUOVO]
- **Alta priorita (6):** R01, R07 (ora Materializzato), R12 (ora Materializzato), R16, **R26 (music21 class detection)** [NUOVO]
- **Media priorita (3-4):** R02, R03, R08, R10, R11, R13, R14, R17, R18, R19, R22, R23, R24, R25
- **Bassa priorita (1-2):** R20, R21
- **Non materializzato:** R04, R05
- **Non applicabile v1:** R06

**Totale rischi tracciati:** 27 (23 aperti + 2 non materializzati + 1 non applicabile v1 + 1 nuovo priorita critica).

Il registro viene rivisto a ogni milestone e dopo ogni Change Request.
