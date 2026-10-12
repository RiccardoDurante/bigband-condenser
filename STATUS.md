---
document: Project Status
project: Big Band Condenser v1
updated: 2026-10-12 23:00 (CEST)
session: 2026-10-12 (M1 baseline)
---

# Project Status

## Milestone corrente

**M1 - Project Initiation Baseline**: COMPLETATO
Tag git: ``M1-initiation`` su commit ``2abfee7``.

## Task completati nella sessione del 12 ottobre 2026

- Setup ambiente locale (Python 3.13.14, Git, VSCode, Pandoc 3.12.1, MiKTeX 25.12, GitHub CLI 2.102)
- Repository ``bigband-condenser`` creato in locale e su GitHub (privato)
- Scaffolding tecnico: struttura cartelle, ``.gitignore``, ``LICENSE`` (MIT), ``pyproject.toml``, config VSCode
- Virtual environment Python attivato con install editable (music21, pydantic, pytest, ruff, mypy)
- 6 documenti baseline M1 depositati:
  - ``docs/pmi/PROJECT_SCOPING_SUMMARY.md`` v1.0
  - ``docs/pmi/CHARTER.md`` v0.4
  - ``docs/pmi/STAKEHOLDER_REGISTER.md`` v0.2
  - ``docs/pmi/RISK_REGISTER.md`` v0.2 (23 rischi)
  - ``docs/pmi/CHANGE_LOG.md`` v0.2 (14 decisioni di avvio)
  - ``README.md`` v0.2 (inglese, root)
- Due commit (``5a85449`` scaffolding, ``2abfee7`` M1 baseline) pushati su ``origin/main``
- Tag ``M1-initiation`` pushato su ``origin``

## Task pendenti - priorita per prossima sessione

1. ``scripts/build_pdfs.ps1`` script PowerShell per generazione PDF via Pandoc
2. ``templates/pmi_template.tex`` template LaTeX minimo per rendering PMI
3. Prima generazione PDF di tutti i documenti M1 in ``docs/pmi/releases/2026-10-12_M1/``
4. Verifica assunzione A2 Charter: ``shared/models.py`` di BigBand AI riusabile (ispezione lettura)
5. Verifica assunzione A3 Charter: ``knowledge/chord_scales.py`` riuso standalone
6. Pianificazione feasibility spike M2 con un MusicXML dello Sponsor
7. Decisione su D-014: passaggio del repo da privato a pubblico (dopo PDF di release)

## Decisioni importanti registrate oggi

- D-013: Licenza MIT (vedi ``LICENSE``)
- D-014: Repo privato in Initiating, pubblico a M1 completato - NOTA: M1 e completato dal 12/10 ma il passaggio pubblico e rimandato alla prossima sessione dopo la generazione dei PDF, per avere una prima apparizione pubblica piu curata

## Rischi emersi in sessione

Nessuno nuovo. Correzioni al Risk Register:
- Aggiunto R23 (qualita MusicXML in input da OMR o export sporchi) nella categoria Qualita, P=2 I=2

## Prossimo passo consigliato (dalla prossima sessione)

Produrre ``scripts/build_pdfs.ps1`` e ``templates/pmi_template.tex``, generare la prima release PDF di M1, valutare il passaggio del repo a pubblico. Stima: 1-2 ore.

Prima di iniziare: dichiarare il cappello attivo (Tech Lead per lo script PowerShell e LaTeX; Doc Writer per il template).

## Monte ore consumato in sessione

Sessione del 12 ottobre 2026, circa 2h40min (21:22 - 23:00 CEST).
Monte ore totale consumato: ~2.7h su budget 60h (4.5% del totale).
Monte ore residuo: ~57.3h in 14 settimane (circa 4.1h/settimana medi, dentro il baseline 5h/settimana).

## Nota di sessione

Setup lungo per diagnosi graduale di PATH Windows, installer winget, encoding PowerShell con heredoc, pager git. Nessun blocco serio, nessun rework. Review PMI dei 4 documenti pre-salvataggio ha prodotto 2 correzioni Charter, 2 correzioni Stakeholder Register, 1 aggiunta Risk Register, 2 aggiunte Change Log, 3 correzioni README. Tutte applicate, nessun debito aperto in uscita.
