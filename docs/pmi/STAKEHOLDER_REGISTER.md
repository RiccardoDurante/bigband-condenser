---
document: Stakeholder Register
document_id: SR-BBC-001
project: Big Band Condenser v1
version: 0.2
status: Draft
last_updated: 2026-10-12
language: it
changelog:
  - v0.2 (2026-10-12): rinominata prima colonna da "Interesse / aspettativa" a "Aspettativa / stake" per evitare collisione con asse di valutazione; S10 BigBand AI portato da Media/Media a Media/Alta e ricollocato nel quadrante "Media influenza, Alto interesse"
  - v0.1 (2026-10-12): prima emissione
---

# Stakeholder Register - Big Band Condenser v1

## 1. Nota sui ruoli multipli

Sponsor, Project Manager, Developer e primo utente del tool coincidono nella stessa persona. Sono pero cappelli distinti, con interessi che possono entrare in conflitto: lo Sponsor vuole chiudere nei tempi, il PM vuole contenere i rischi, il Developer vuole codice pulito, lo studente CAPM vuole applicare il metodo con completezza. Il Change Log e il luogo in cui questi conflitti vengono esplicitati e risolti.

## 2. Registro

| ID | Stakeholder | Tipo | Aspettativa / stake | Influenza | Interesse | Strategia di gestione |
|---|---|---|---|---|---|---|
| S01 | Sponsor | Interno | Approva Charter, Change Request di scope e deliverable; fornisce tempo e budget | Alta | Alta | Gestire da vicino: revisione a ogni milestone |
| S02 | Project Manager | Interno | Pianifica, coordina, controlla; garantisce disciplina PMI | Alta | Alta | Gestire da vicino: STATUS.md a ogni sessione |
| S03 | Developer / utente primario | Interno | Strumento utile al proprio lavoro di analisi e arrangiamento | Alta | Alta | Gestire da vicino: criteri di accettazione condivisi |
| S04 | Ruoli funzionali (BA, Tech Lead, Developer, QA, Music Expert, Researcher, Doc Writer, Risk Officer) | Interno (contesti di lavoro in Claude) | Output coerente con scope e vincoli del progetto | Media | Alta | Dichiarare il ruolo a inizio sessione; Claude Project come memoria; escalation allo Sponsor per ogni cambio di scope |
| S05 | Utenti futuri open source (arrangiatori, studenti di jazz, direttori di big band) | Esterno | Strumento affidabile, documentato, installabile | Bassa | Media | Tenere informati: README chiaro, esempi, issue tracker |
| S06 | Community Python / contributori potenziali | Esterno | Codice leggibile, test, linee guida di contribuzione | Bassa | Bassa | Monitorare: CONTRIBUTING e licenza chiara |
| S07 | Manutentori di music21 | Esterno (dipendenza) | Uso corretto della libreria; stabilita delle API | Media | Bassa | Monitorare: versione fissata, test di regressione |
| S08 | Steinberg (Dorico) | Esterno (piattaforma) | Importazione MusicXML corretta; compatibilita con Remote Control API | Media | Bassa | Monitorare: verifica su versione installata |
| S09 | Anthropic (fornitore Claude Pro) | Esterno (fornitore) | Rispetto dei limiti d'uso del piano; variazioni di piani e prezzi | Media | Bassa | Monitorare: consumo, alternativa di lavoro a basso consumo |
| S10 | Progetto BigBand AI Assistant (progetto donatore) | Interno (dipendenza) | Resta stabile; nessuna modifica non autorizzata | Media | Alta | Sola lettura; modifiche solo via Change Request |
| S11 | Comunita PMI / CAPM | Esterno | Eventuale studio del progetto come caso applicato | Bassa | Bassa | Tenere informati: documentazione PMI pubblicata nel repo |

## 3. Matrice influenza / interesse

- **Alta influenza, alto interesse (gestire da vicino):** S01, S02, S03
- **Media influenza, alto interesse (tenere informati e coinvolti):** S04, S10
- **Media influenza, basso interesse (mantenere soddisfatti, monitorare):** S07, S08, S09
- **Bassa influenza (tenere informati / monitorare):** S05, S06, S11

## 4. Note

- I titolari di diritti su materiale musicale di terzi non sono stakeholder del progetto, perche nessun materiale di terzi viene distribuito o elaborato pubblicamente (vedi vincolo 1 del Charter).
- Il registro viene riesaminato a ogni milestone; nuovi stakeholder (ad esempio contributori reali) vengono aggiunti con una riga e una voce nel Change Log.
