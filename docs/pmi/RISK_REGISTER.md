---
document: Risk Register
document_id: RR-BBC-001
project: Big Band Condenser v1
version: 0.2
status: Draft
last_updated: 2026-10-12
language: it
changelog:
  - v0.2 (2026-10-12): aggiunto R23 (qualita MusicXML in input da OMR o export sporchi) nella categoria Qualita; aggiornata sintesi
  - v0.1 (2026-10-12): prima emissione, 22 rischi
---

# Risk Register - Big Band Condenser v1

**Scala.** Probabilita (P) e Impatto (I) da 1 (basso) a 3 (alto). Punteggio = P x I (1-9). Priorita: 6-9 alta, 3-4 media, 1-2 bassa.
**Stato:** Aperto / In monitoraggio / Mitigato / Chiuso.
**Responsabile:** salvo diversa indicazione, lo Sponsor/PM (cappello Risk Officer).

| ID | Categoria | Rischio | P | I | Punt. | Risposta e mitigazione | Stato |
|---|---|---|---|---|---|---|---|
| R01 | Pianificazione | La produttivita osservata su BigBand AI non si trasferisce e le 60 ore previste sono sottostimate | 2 | 3 | 6 | Verifica nelle prime 2 settimane (spike M2); ristimare con dati reali; se necessario Change Request su scope o data | Aperto |
| R02 | Pianificazione | La deadline del 31/01/2027 non viene rispettata | 2 | 2 | 4 | Buffer del 25% (circa 15 ore); monitoraggio settimanale di ore e milestone; priorita ai requisiti essenziali | Aperto |
| R03 | Pianificazione | Disponibilita dello Sponsor inferiore a 5 ore/settimana per impegni esterni | 2 | 2 | 4 | Sessioni brevi e frequenti; STATUS.md per ripartire senza perdere contesto; revisione del piano a ogni milestone | Aperto |
| R04 | Tecnico | ``shared/models.py`` di BigBand AI e troppo legato al flusso generativo per essere riusato | 2 | 1 | 2 | Verifica come prima attivita del primo sprint; in caso negativo copiare solo la parte generica o definire modelli nuovi | Aperto |
| R05 | Tecnico | ``chord_scales.py`` non e utilizzabile come parser standalone | 2 | 1 | 2 | Isolare le dipendenze prima del riuso; alternativa: parser dedicato basato su ``music21.harmony`` | Aperto |
| R06 | Tecnico | ``dorico_bridge/`` incompatibile con la versione di Dorico installata | 1 | 3 | 3 | Verifica precoce; il flusso primario resta l'importazione manuale del MusicXML, il bridge e facoltativo | Aperto |
| R07 | Tecnico | music21 gestisce male scrittura multi-staff, slash notation o notazione di batteria | 2 | 3 | 6 | Spike precoce su questi tre casi; se necessario generare direttamente parti di XML mancanti | Aperto |
| R08 | Tecnico | Il rilevatore comping/shout non converge sui casi borderline | 2 | 2 | 4 | Soglie parametrizzabili da CLI; metriche separate; override manuale; casi borderline documentati | Aperto |
| R09 | Tecnico | Chord symbols duplicati o in conflitto tra piano e chitarra | 2 | 1 | 2 | Regola di precedenza documentata (piano prima, chitarra come fallback); test dedicati | Aperto |
| R10 | Tecnico | Doubling nelle reeds (cambi di strumento) gestiti in modo errato | 2 | 2 | 4 | Trattare ogni parte come sequenza di strumenti; test con casi di doubling; classificazione per esecutore e non solo per strumento | Aperto |
| R11 | Tecnico | Assegnazione ambigua degli strumenti della sezione ritmica (piano, chitarra, basso) | 2 | 2 | 4 | Tabella di classificazione esplicita e documentata; parametro di override | Aperto |
| R12 | Tecnico | Differenze di esportazione MusicXML tra software (Dorico, Sibelius, Finale, MuseScore) | 3 | 2 | 6 | Dichiarare in v1 il supporto garantito per l'esportazione di Dorico; testare gli altri come best effort | Aperto |
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

## Sintesi

- **Alta priorita (6-9):** R01, R07, R12, R15, R16
- **Media priorita (3-4):** R02, R03, R06, R08, R10, R11, R13, R14, R17, R18, R19, R22, R23
- **Bassa priorita (1-2):** R04, R05, R09, R20, R21

Il registro viene rivisto a ogni milestone e dopo ogni Change Request.
