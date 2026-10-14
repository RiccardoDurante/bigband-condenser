---
document: Project Status
project: Big Band Condenser v1
updated: 2026-10-14 16:30 (CEST)
session: 2026-10-14 (Fase A verifica assunzioni + Fase B pianificazione spike)
---

# Project Status

## Milestone corrente

**M1 - Project Initiation Baseline**: COMPLETATO E RILASCIATO
**M2 - Spike di fattibilita**: IN PIANIFICAZIONE
Tag git: ``M1-initiation`` su commit ``2abfee7``.
Piano operativo: ``docs/pmi/SPIKE_M2_PLAN.md`` v0.1.

## Task completati nella sessione del 14 ottobre 2026

### Fase A - Verifica assunzioni Charter (cappello Researcher)

- Lettura read-only di 3 target in BigBand AI (``shared/models.py``, ``knowledge/chord_scales.py``, ``dorico_bridge/``)
- Verdetti:
  - A2 (``shared/models.py``): B - copia selettiva NoteData e MelodyData
  - A3 (``chord_scales.py``): B - copia integrale, uso parziale v1 (parser come validator)
  - A4 scissa:
    - A4.1 Bridge WebSocket: D - fuori scope v1
    - A4.2 ``musicxml_writer.py`` orfano: **A - riuso diretto** (scoperta inattesa, saving 8-12h)
- Totale saving confermato: 12.5-19 ore rispetto a scrittura da zero
- Nessuna modifica al progetto donatore (vincolo Charter rispettato)
- Prodotto ``docs/pmi/BIGBAND_AI_REUSE_ASSESSMENT.md`` v0.1
- Bump Risk Register v0.3: R04/R05 Non materializzato, R06 Non applicabile v1, nuovo R24 (bug music21 transpose tag)
- Bump CHANGE_LOG v0.5 con D-017 e D-018
- Commit e push su GitHub

### Fase B - Pianificazione spike M2 (cappello Business Analyst)

- Discussione estesa su test case: scartato uso di reference sotto copyright (vincolo legale), scartato pubblico dominio reale (quasi inesistente per big band), scelto brano proprio dello Sponsor
- Test case definito: "Kronos kai Kairos" composto da Riccardo Durante, 6 min, 17 strumenti organico non canonico, licenza CC-BY 4.0
- Scope spike Lettura B+: 6 Q (Q1-Q5 tecniche + Q6-minimale struttura output)
- Timebox 12h totali (10h spike + 2h overhead) in 2 settimane calendario
- Deliverable: SPIKE_M2_REPORT + codice spike in ``src/bigband_condenser/_spike/`` + decisione formale finale
- Criteri successo: S1 copertura + S2 delta <= 25% + S3 nessuna assunzione residua
- R25 candidato registrato come osservazione nel piano (bump Risk Register rimandato a sessione M2)
- Prodotto ``docs/pmi/SPIKE_M2_PLAN.md`` v0.1
- Bump CHANGE_LOG v0.6 con D-019

## Task pendenti - priorita per prossima sessione

1. **Setup samples/**: README, file LICENSE CC-BY 4.0 per Kronos, placeholder per i due MusicXML
2. **Export brano da Dorico** (azione Sponsor fuori sessione): estratto 32 battute + brano intero, salvare in ``samples/``
3. Primo commit samples (il brano entra nel repo pubblico)
4. Scrittura stub code dello spike in ``src/bigband_condenser/_spike/`` con README esplicativo
5. Esecuzione Q1 (parse integrity) su estratto 32 battute
6. Procedere Q2-Q6 secondo timebox

## Decisioni importanti registrate oggi

- D-017: Verifica assunzioni Charter completata, nota tecnica BIGBAND_AI_REUSE_ASSESSMENT.md
- D-018: Risk Register v0.3 con R04/R05 Non materializzato, R06 Non applicabile v1, nuovo R24
- D-019: Piano operativo spike M2 con test case Kronos kai Kairos CC-BY 4.0

## Rischi emersi in sessione

- **R04, R05 declassati** a "Non materializzato" (verifica assunzioni positiva)
- **R06 declassato** a "Non applicabile v1" (bridge WebSocket fuori scope v1)
- **R24 aggiunto**: bug music21 noti su transpose tag parti multiple stessa classe strumento (mitigato da workaround ereditato)
- **R25 candidato**: classificazione fallisce su organici non canonici (es. corni F in Kronos). Osservazione nel SPIKE_M2_PLAN. Bump Risk Register rimandato a sessione M2.

## Debito tipografico PDF (gia tracciato nelle sessioni precedenti)

Rinviato a refresh pre-tesi CAPM: correzioni B (``\footnotesize`` in longtable), C (``\titlespacing``), tabella Budget Charter sezione 7. Nessun impatto operativo per adesso.

## Prossimo passo consigliato (dalla prossima sessione)

**Cappello Doc Writer** per setup ``samples/`` (README + LICENSE CC-BY 4.0 per Kronos).

Poi, in parallelo o successivamente: **Sponsor fuori sessione** esporta i due MusicXML da Dorico (estratto + intero).

Quando entrambi disponibili: **cappello Developer** per primo commit samples + scrittura stub codice spike.

Durata stimata prossima sessione: 1h-1h30 (setup repo + commit samples, non ancora codice spike).

## Monte ore consumato in sessione

Sessione del 14 ottobre 2026, circa 2h00min (15:30 - 17:30 CEST ca.).

Monte ore cumulato (12-13-14 ottobre): ~6.5h su budget 60h (11% del totale).
Monte ore residuo: ~53.5h in ~14 settimane (~3.8h/settimana medie, sotto baseline 5h/settimana).

Osservazione: sessione lunga ma produttiva. Fase A ha consolidato le fondamenta del piano (saving 12.5-19h confermati). Fase B ha pianificato M2 con disciplina PMI (timebox hard, criteri binari, scope esplicitamente escluso), riducendo rischio R15 scope creep.

## Nota di sessione

Discussione estesa su copyright (reference artifact Schneider, standard jazz, pubblico dominio) prima di arrivare alla soluzione pulita "composizione dello Sponsor". Discussione preziosa dal punto di vista PMI/Risk, perche ha chiarito definitivamente i vincoli legali del test corpus (coerenza Charter §12.1 e §12.2, R17).

Approccio role-switching single-chat ha funzionato bene con cambio esplicito da Researcher a Business Analyst a meta sessione. Entrambi i cappelli hanno prodotto deliverable coerenti con la definizione minimalista di ROLES.md.
