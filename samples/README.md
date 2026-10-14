# samples/

Big Band MusicXML files used as test cases for Big Band Condenser.

## Policy

- Only MusicXML files composed by the Sponsor or files in genuine public domain can live here.
- No third-party copyrighted material, even for private testing (see project Charter section 12.1 and Risk Register R17).
- Each file must have an associated license declaration (either a dedicated `.LICENSE` file next to it, or an entry in this README).

## Current samples

### kronos_kai_kairos.musicxml

- **Composer**: Riccardo Durante
- **Title**: Kronos kai Kairos
- **Duration**: approx. 6 minutes
- **Ensemble**: 17-instrument non-canonical big band
  - Reeds: Soprano sax, Alto sax, 2 Tenor sax, Baritone sax
  - Brass: 4 Trumpet, 2 Horn in F, Trombone, Bass Trombone
  - Rhythm: Electric Guitar, Piano, Bass
  - Drums
- **License**: CC-BY 4.0 (see `kronos_kai_kairos.LICENSE` and `LICENSE-CC-BY-4.0.txt`)
- **Role in project**: primary test case for Spike M2 feasibility validation; see `docs/pmi/SPIKE_M2_PLAN.md`.

### kronos_kai_kairos_extract.musicxml

- Same metadata as above, extract of approximately 32 bars for faster development iteration during Spike M2.
- Same license (CC-BY 4.0).

## File format

All test samples are MusicXML files (`.musicxml`), exported from Steinberg Dorico 5+.

If you want to contribute a sample:

1. Confirm you have full copyright on the piece or that the piece is in genuine public domain in your jurisdiction.
2. Choose a permissive license (CC-BY 4.0 or CC0 recommended).
3. Add a `<filename>.LICENSE` file next to the MusicXML with attribution and license text reference.
4. Add an entry in the "Current samples" section above.
5. Open a pull request.
