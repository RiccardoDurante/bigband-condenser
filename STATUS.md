---
document: Project Status
project: Big Band Condenser v1
updated: 2026-10-13 22:00 (CEST)
session: 2026-10-13 (M1 release + PDF pipeline)
---

# Project Status

## Milestone corrente

**M1 - Project Initiation Baseline**: COMPLETATO + RILASCIATO IN PDF
Tag git: ``M1-initiation`` su commit ``2abfee7``.
Release PDF: ``docs/pmi/releases/2026-10-12_M1/`` (6 PDF, 971 KB totali).

## Task completati nella sessione del 13 ottobre 2026

- Rimosso file untracked spurio (``h origin M1-initiation``, dump accidentale di git show)
- Aggiornato MiKTeX package database (``mpm --update-db``)
- Creato Roles Register minimalista ``docs/pmi/ROLES.md`` v0.1 (8 ruoli, "cosa fa / cosa non fa"), scheletro per bump v0.2 post-WBS
- Bumpato CHANGE_LOG.md a v0.3 con D-015 (creazione Roles Register)
- Creato script ``scripts/build_pdfs.ps1`` (PowerShell, Pandoc + MiKTeX wrapper, parametri Milestone/Date/Files/DryRun)
- Creato ``templates/pmi_template.tex`` (LaTeX template, Pandoc 3.x compatibile, identita visuale Big Band Condenser)
- Debug template: patch 1 per contatore ``none`` (Pandoc 3.x table helpers); patch 2 per numerazione sezioni duplicata (secnumdepth = -1)
- Generata prima release PDF di M1 in ``docs/pmi/releases/2026-10-12_M1/`` con 6 PDF

## Task pendenti - priorita per prossima sessione

1. Verifica assunzione A2 Charter: ``shared/models.py`` di BigBand AI riusabile (ispezione lettura)
2. Verifica assunzione A3 Charter: ``knowledge/chord_scales.py`` riuso standalone
3. Verifica assunzione A4 Charter: ``dorico_bridge/`` compatibilita Dorico installato
4. Pianificazione feasibility spike M2 con un MusicXML dello Sponsor
5. Avvio spike M2 (prototipo minimale su MusicXML tuo, target fine ottobre)

## Decisioni importanti registrate oggi

- D-015: Creazione Roles Register minimalista v0.1, bump v0.2 completo rimandato post-WBS (CHANGE_LOG v0.3)
- NOTA su D-014 (passaggio repo privato -> pubblico): valutata in sessione, scelta posticipare fino a dopo che la prima release PDF sia stabile e verificata. Possibile passaggio pubblico in prossima sessione dopo verifica assunzioni Charter.

## Debito tipografico PDF (rinviato a fase stampa tesi)

Durante il refresh pre-tesi CAPM, applicare al template ``templates/pmi_template.tex`` queste tre correzioni rinviate (non critiche per leggibilita, utili per eleganza tipografica):

1. **Correzione B - Font ridotto in longtable**: la tabella Risk Register (23 rischi x 8 colonne) occupa 12 pagine. Aggiungere ``\AtBeginEnvironment{longtable}{\footnotesize}`` dopo il blocco calc. Risultato atteso: Risk Register in 5-6 pagine, altre tabelle (Charter milestone, budget, Change Log) piu compatte.

2. **Correzione C - Spazio tra titolo sezione e paragrafo**: titoli attualmente stretti al paragrafo che segue. Aggiungere:

3. **Charter tabella Budget sezione 7**: la riga "Python, music21, Pydantic, VS Code, Git/GitHub, Pandoc, MiKTeX" va a capo male. Valutare se forzare larghezza colonne con ``tabularx`` esplicito o se spezzare la riga nel sorgente Markdown.

Rimandate perche prive di impatto su contenuto o accessibilita; valore solo di eleganza. Costo stimato: 15-30 minuti di patch + 2-3 iterazioni di rebuild per fine-tuning.

## Rischi emersi in sessione

Nessuno nuovo. R23 (qualita MusicXML in input) gia aggiunto in sessione del 12/10.
Nota operativa su R22 (overhead documentale): tempo oggi usato per PDF pipeline (~90 min) e investimento one-off, non ricorrente. Rebuild PDF di sessioni successive sara di 30-60 secondi.

## Prossimo passo consigliato (dalla prossima sessione)

**Primo passo**: cappello Researcher (o Tech Lead), verifica delle 3 assunzioni Charter su codice BigBand AI (A2, A3, A4). Durata stimata: 30-45 min di lettura codice.

**Secondo passo**: pianificazione spike M2 (feasibility su un MusicXML tuo). Richiede che tu identifichi un brano big band tuo esportato in MusicXML, che useremo come primo test case.

**Terzo passo** (opzionale, se tempo): avvio spike M2 con parser MusicXML + classificazione strumenti.

## Monte ore consumato in sessione

Sessione del 13 ottobre 2026, circa 1h30min (21:20 - 22:00 CEST ca.).
Monte ore totale consumato (cumulato 12-13 ottobre): circa 4.0-4.5h su budget 60h (circa 7-7.5% del totale).
Monte ore residuo: circa 55-56h in 14-15 settimane.

Analisi onesta: la sessione di oggi ha speso quasi un'ora in debug template LaTeX (contatore ``none`` + numerazione sezioni). Nessun grosso rework, nessuna perdita di tempo evitabile, pero evidenzia che il piano "PDF pipeline in 30 min" era ottimistico. Nessun impatto strutturale sul budget 60h.

## Nota di sessione

Produttivita buona, nessun blocco serio. Debug LaTeX tipico del primo build con template custom: il blocco di debug delle tabelle Pandoc 3.x (contatore ``none``) e un gotcha noto. Documentato in CHANGE_LOG se mai dovessimo ricostruire da zero.
