---
document: Project Charter
document_id: PC-BBC-001
project: Big Band Condenser v1
version: 0.4
status: Draft - in attesa di approvazione dello Sponsor
last_updated: 2026-10-12
language: it
changelog:
  - v0.4 (2026-10-12): aggiornato riferimento scope statement (ora PROJECT_SCOPING_SUMMARY.md del 12 ottobre 2026); formalizzata scelta licenza MIT come deliverable M1
  - v0.3 (2026-10-12): generalizzato il vincolo sui reference artifact di terzi; ricalibrate stime (60 h, 5 h/sett.); aggiunti budget, ambiente tecnico, modello di lavoro e deadline
  - v0.2 (2026-10-12): input MusicXML con OMR a carico dell'utente; roadmap fasi future
  - v0.1 (2026-10-12): bozza iniziale
---

# Project Charter - Big Band Condenser v1

## 1. Scopo e giustificazione

**Problema.** Arrangiatori, direttori, studenti di composizione e analisti che lavorano su partiture big band hanno spesso bisogno di una *condensed score* (particella analitica) per studio e analisi. Realizzarla a mano richiede molto tempo e competenze specifiche di lettura di partitura e di convenzioni jazz.

**Soluzione.** Una pipeline software open source che trasforma automaticamente una partitura big band in MusicXML in una condensed score in MusicXML, pronta per l'importazione e la revisione finale in Dorico.

**Giustificazione.** Non risultano strumenti pubblici dedicati alla condensazione automatica di partiture big band secondo le convenzioni jazz. Il progetto riusa inoltre infrastruttura già sviluppata e testata (progetto BigBand AI Assistant), riducendo tempi e rischi.

## 2. Obiettivi

1. **Tecnico.** Pipeline che, dato un MusicXML big band, produce un MusicXML condensed con 4 sistemi (Reeds, Brass, Rhythm, Drums), in concert pitch, senza perdere informazioni musicali.
2. **Qualita.** Validator con metriche interpretabili e separate, suite di test (target 100-150 test), documentazione tecnica e architetturale.
3. **Rilascio.** Repository open source con documentazione utente, tecnica e di project management.

## 3. Requisiti di alto livello

**Funzionali**

1. Input: MusicXML di partitura big band (organico canonico di 17 strumenti, con varianti: flicorni, doubling nelle reeds). La conversione da PDF/immagini e fuori scope: e a carico dell'utente tramite strumenti OMR esterni.
2. Output: MusicXML con 4 sistemi fissi: Reeds (doppio pentagramma), Brass (doppio pentagramma), Rhythm (doppio pentagramma con chord symbols), Drums (pentagramma singolo).
3. Trasposizione in concert pitch di tutti gli strumenti traspositori.
4. Nessuna nota persa: tutte le note vengono riorganizzate per sezione.
5. Preservazione di dinamiche, accenti, legature, articolazioni e text directions.
6. Distinzione automatica tra sezioni *comping* (Rhythm: ritmo semplificato + basso melodico) e *shout/tutti* (Rhythm: armonia densa).
7. Estrazione dei chord symbols dalla parte di piano/chitarra e riposizionamento sul rigo Rhythm, in notazione jazz standard.
8. Parte di batteria preservata (slash notation, rhythmic notation, text directions del compositore).
9. MusicXML di output valido secondo la specifica W3C.
10. Importabile in Dorico senza errori.

**Non funzionali**

- Determinismo: stesso input, stesso output.
- Stack coerente con BigBand AI: Python 3.11+, music21, Pydantic.
- Documentazione completa e riusabile da terzi; licenza open source esplicita.

## 4. Confini dello scope

**Incluso:** quanto elencato nei requisiti (sezione 3) e nel ``PROJECT_SCOPING_SUMMARY.md`` del 12 ottobre 2026.

**Escluso (v1):**

- Conversione PDF/immagine -> MusicXML
- Analisi funzionale con numeri romani, box analitici, frecce motiviche, annotazioni didattiche
- Cross-reference automatiche tra sistemi
- Generazione automatica dei kick-over di batteria (in v1 si copiano dalla parte originale, se presenti)
- Font, impaginazione e scelte tipografiche fini (demandate a Dorico)
- Suonabilita pianistica dell'output
- Interfaccia web o grafica
- Repertorio non big band; voci cantate; tecniche estese contemporanee
- Repertorio sotto copyright nel corpus di test pubblico

## 5. Deliverable

**Principale:** ``bigband-condenser v1.0.0``, pipeline invocabile da CLI.

**Collaterali:**

- Repository pubblico con codice sorgente
- README utente (problema, installazione, uso, esempi)
- Documentazione tecnica (architettura, moduli, convenzioni di condensazione)
- Documentazione di project management: Charter, Stakeholder Register, Risk Register, WBS, RACI, Change Log, Lessons Learned
- Suite di test (unitari e di integrazione)
- Almeno 3 esempi dimostrativi (input e output) su repertorio di pubblico dominio o composizioni dello Sponsor
- Licenza open source **MIT** (decisa in M1; vedi file ``LICENSE`` nel repository root)

## 6. Tempi e milestone

Deadline target: **31 gennaio 2027** (circa 15 settimane dal 12 ottobre 2026).

Sforzo stimato: **60 ore**. Disponibilita: **5 ore/settimana** di base, con possibilita di incrementi. Capacita di base nel periodo: circa 75 ore, quindi buffer di circa 15 ore (25%).

| Milestone | Descrizione | Target indicativo |
|---|---|---|
| M1 | Baseline di avvio: Charter, Stakeholder Register, Risk Register depositati nel repo | Ottobre 2026 |
| M2 | Spike di fattibilita su un MusicXML dello Sponsor | Fine ottobre 2026 |
| M3 | Parser MusicXML e classificatore strumenti | Meta novembre 2026 |
| M4 | Condensatore di sezione funzionante su una sezione | Fine novembre 2026 |
| M5 | Pipeline end-to-end su un brano di test | Meta dicembre 2026 |
| M6 | Comping/shout, chord symbols e batteria completati | Fine dicembre 2026 |
| M7 | Validator e suite di test completati | Meta gennaio 2027 |
| M8 | CLI, documentazione utente, esempi | Fine gennaio 2027 |
| M9 | Documentazione PMI finale, Lessons Learned, release v1.0.0 | 31 gennaio 2027 |

Le date sono indicative e verranno consolidate nella WBS. Il compito di generazione dei PDF di documentazione e il primo task operativo in VS Code.

## 7. Budget

Tetto massimo: **200 EUR** (strumenti AI, abbonamenti, eventuali altre spese).

| Voce | Stima |
|---|---|
| Claude Pro (circa 4 mesi) | circa 75-80 EUR |
| Python, music21, Pydantic, VS Code, Git/GitHub, Pandoc, MiKTeX | 0 EUR |
| Dorico (gia in possesso dello Sponsor) | 0 EUR |
| Riserva | circa 120 EUR |

Nessun software OMR a pagamento e previsto (fuori scope). Il consumo di Claude Pro e soggetto a limiti d'uso, che costituiscono un vincolo operativo (vedi Risk Register).

## 8. Modello di lavoro e ruoli

Il progetto e autodiretto. Sponsor, Project Manager e Developer coincidono nella stessa persona, che indossa cappelli diversi in momenti diversi.

I ruoli funzionali (Business Analyst, Tech Lead, Developer, QA, Music Expert, Researcher, Doc Writer, Risk Officer) non sono entita autonome: sono contesti di lavoro che lo Sponsor/PM attiva dichiarandoli all'inizio di una sessione con Claude Pro, usando un Claude Project come memoria persistente del progetto (approccio *role-switching in single chat*).

- L'esecuzione tecnica (comandi, test, commit) e svolta dallo Sponsor in VS Code, con copia/incolla di codice e output tra IDE e chat.
- Lo stato tra sessioni e affidato a ``STATUS.md``, ``CHANGE_LOG.md`` e ai commit Git.
- Qualunque proposta di modifica di scope, deliverable, stack o architettura segue il processo di Change Request: motivazione, impatto su scope/tempo/rischi, raccomandazione, decisione dello Sponsor, registrazione nel Change Log.

## 9. Stakeholder principali

Vedi ``STAKEHOLDER_REGISTER.md``.

## 10. Rischi di alto livello

Vedi ``RISK_REGISTER.md``. Principali: produttivita stimata non trasferibile, riuso del codice BigBand AI non immediato, limiti di music21 su notazione di batteria e multi-staff, limiti d'uso del piano Pro, scope creep.

## 11. Assunzioni (da verificare entro le prime 2 settimane)

1. La produttivita dimostrata su BigBand AI e trasferibile a questo progetto (60 ore di sforzo).
2. ``shared/models.py`` di BigBand AI e sufficientemente generico da essere riusato.
3. ``knowledge/chord_scales.py`` contiene un parser di chord symbols jazz utilizzabile in modo indipendente.
4. ``dorico_bridge/`` e compatibile con la versione di Dorico installata.
5. Lo Sponsor dispone di almeno un arrangiamento big band proprio esportabile in MusicXML.
6. Lo Sponsor dispone di reference artifact (propri o di terzi, ad uso privato) sufficienti a definire le convenzioni di condensazione.
7. music21 supporta le funzioni MusicXML necessarie in lettura e scrittura.
8. L'utente finale dispone del MusicXML della partitura; la sua qualita e responsabilita dell'utente. Errori provenienti da OMR esterno si propagano all'output senza costituire un difetto del tool.

## 12. Vincoli

1. Eventuali reference artifact di terzi protetti da copyright sono usati solo come riferimento privato dello Sponsor per definire le convenzioni di condensazione: non vengono distribuiti, non entrano in repository o dataset pubblici, non vengono elaborati da servizi con conservazione dei dati. Il materiale pubblicabile e solo di composizione dello Sponsor o di pubblico dominio.
2. Il corpus di test pubblico e limitato a composizioni dello Sponsor o repertorio di pubblico dominio.
3. Stack: Python 3.11+, music21, Pydantic.
4. Budget massimo 200 EUR; deadline target 31 gennaio 2027; circa 5 ore/settimana.
5. BigBand AI Assistant e un progetto donatore in sola lettura: nessuna modifica senza Change Request.

## 13. Ambiente tecnico

VS Code (IDE), Python 3.11+, music21, Pydantic, pytest, Git e GitHub, Pandoc con MiKTeX (generazione PDF), Dorico 5 o successivo (test di importazione), Claude Pro con Claude Project dedicato.

## 14. Gestione documentale

- Documenti di lavoro in Markdown in ``docs/pmi/``, versionati con Git.
- Version block in testa a ogni documento; decisioni di alto livello nel ``CHANGE_LOG.md``.
- PDF generati con Pandoc ai milestone e archiviati in ``docs/pmi/releases/<data>_<milestone>/``.
- Lingua: documenti PMI in italiano; README, architettura, commenti nel codice e messaggi di commit in inglese; ``README.it.md`` per i lettori italiani.

## 15. Roadmap - fasi future (non impegnate)

- **Fase B - Web Interface:** interfaccia web per utenti non tecnici (upload, elaborazione, download).
- **Fase C - Integrazione OMR:** accettare PDF in input.
- **Fase D - Analisi musicale automatica:** numeri romani, analisi formale, collegamenti motivici.
- **Fase E - Generazione automatica dei kick-over di batteria.**

Ciascuna fase richiederebbe un Charter separato.

## 16. Autorita

- **Sponsor:** approva Charter, Change Request di scope, deliverable finali.
- **Project Manager:** pianificazione, WBS, assegnazione del lavoro ai ruoli, Change Control tecnico a basso impatto, gestione operativa dei rischi.

## 17. Approvazione

| | |
|---|---|
| Approvato da | Riccardo Durante (Sponsor) |
| Data | 2026-10-12 |
| Firma | [firma elettronica - approvazione in sessione del 12 ottobre 2026] |
