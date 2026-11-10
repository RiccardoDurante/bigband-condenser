# STATUS — Big Band Condenser

**Aggiornato al:** 2026-11-10 21:17 CET
**Sessione corrente:** QA — TK-Reeds-01 partial (coalesce + filter), known limitation

## Milestones

- [x] M0 Scoping
- [x] M1 Initiation Baseline
- [x] M2 Preprocessing + Classifier
- [x] M3 Dependencies locked
- [x] M4 Reeds condenser (visual gate PASS)
- [x] M5 Brass condenser (visual gate PASS)
- [x] M6 Rhythm condenser con slash-style awareness (visual gate PASS)
- [x] M7 Drums condenser (43/43 notes PASS strict)
- [x] M8 CLI orchestrator `bbcondenser`
- [x] M9 Validator unificato (--validate, --report, --tolerance, soglia 2%)
- [x] M10-preview Layout landscape + compact labels (D-040, D-041)
- [x] TK-Reeds-01 — Reeds fidelity bug: risolto parzialmente (D-042)
- [ ] M10 PDF orizzontale via LilyPond (**prossima sessione**)
- [ ] M10 PDF orizzontale via LilyPond
- [ ] M11 User docs
- [ ] M12 Docs PMI finali
- [ ] v1.0.0 release

## Prossima sessione: QA deep-dive Reeds m72-m111

**Osservazione chiave:** in 59/142 bars il validator riporta missing ≈ extra
(pattern simmetrico). Esempi: m82 5.0/5.0, m94 3.33/3.33, m99 7.5/7.5,
m104 7.0/7.0. Simmetria = tipico bug di **ottava** o **trasposizione**.

**Ipotesi da verificare (in ordine di probabilità):**
1. Cambio key signature a m72 non applicato uniformemente ai sax
2. Doubling instrument switch (sax → clarinet/flute) con trasposizione diversa
3. Algoritmo split 2+3 pitch-based che "swappa" note tra voice 1 e voice 2
4. `toSoundingPitch()` applicato in modo inconsistente nel condenser

**Approccio proposto:**
1. Script diagnostico che per m72-m85 dumpa per ogni voce source note+ottava,
   e per ogni output note+ottava, affiancate
2. Isolare 2-3 bars sentinella e capire quale delle 4 ipotesi è vera
3. Fix mirato nel reeds condenser
4. Rigenerazione + validation: target `PASS*` o `PASS strict` su Reeds

**Stima:** 2-4h.

## Budget

- Ore consumate: ~36h / 60h
- Residuo: ~24h
- Settimane a deadline 31 gen 2027: ~11
- Stima realistica rimasta (Reeds fix + M10 PDF + M11 + M12 + release): 15-18h
- Buffer: 6-9h — **comodo**

## Rischi attivi

- **R-NEW-01 (basso):** Dorico può ignorare `font-size` MusicXML e
  mostrare labels più grandi. Mitigation: se M10 PDF usa LilyPond invece di
  Dorico export, il font è rispettato nativamente. Verificare al M10.
- **R-NEW-02 (medio):** Reeds fidelity bug (TK-Reeds-01). Non blocca il
  tool da un punto di vista funzionale (l'output musicale resta leggibile),
  ma impedisce il PASS validation. Target: risolvere prossima sessione.

## Artifatti sessione

- `src/bigband_condenser/validator.py` (nuovo)
- `src/bigband_condenser/page_layout.py` (nuovo)
- `src/bigband_condenser/cli.py` (esteso: --validate, --report, --tolerance)
- `samples/preview_condensed_full.musicxml` (output di reference)
- `samples/validation_report.txt` (report di reference)
