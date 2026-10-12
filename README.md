# Big Band Condenser

> **Status: early development (pre-release).** Project documents and the first implementation are being built in public. Nothing here is stable yet.

Big Band Condenser turns a big band score in MusicXML into a **condensed score** (a short score for study and analysis), also in MusicXML, ready to be opened and finalized in Dorico.

## What it does

Given a full big band score, the tool produces a condensed score with four fixed systems, all in concert pitch:

| System | Content | Staves |
|---|---|---|
| 1 | Reeds | Grand staff |
| 2 | Brass (trumpets, flugelhorns, trombones) | Grand staff |
| 3 | Rhythm section (piano, guitar, bass) with chord symbols | Grand staff |
| 4 | Drum set (slash and rhythmic notation, composer's directions preserved) | Single staff |

Design principles:

- **No note is lost.** Material is regrouped by section, not discarded.
- **Concert pitch** for every transposing instrument.
- **Deterministic:** same input, same output.
- Sections that play together are written as block chords; the Rhythm system distinguishes comping from tutti/shout passages.

## Scope of v1

In scope: MusicXML input, the four systems above, dynamics, articulations, text directions, chord symbols, a command line interface.

Out of scope for v1: PDF/image input (use an external OMR tool and check the result first), analytical annotations, automatic drum kicks generation, a web interface, non-big-band ensembles.

## Input requirements

You need a MusicXML file of the score. If you only have a PDF, convert it first with an OMR tool and review the output: errors in the input will carry over to the result. Exports from Dorico are the primary tested source.

## Planned usage

```bash
bigband-condenser input.musicxml --output condensed.musicxml
```

The command line interface is not implemented yet.

## Requirements

- Python 3.11+
- music21, Pydantic
- Dorico 5 or later (optional, to open and refine the output)

## Project documentation

Project management documents (Charter, Stakeholder Register, Risk Register, Change Log) are in [`docs/pmi/`](docs/pmi/). They are written in Italian. Italian readers: see `README.it.md` (in progress).

## Roadmap

1. Parser and instrument classification
2. Section condensing engine
3. Comping/shout detection, chord symbols, drums
4. Validators and test suite
5. CLI, user documentation, examples
6. v1.0.0 release (target: end of January 2027)

Possible later phases: web interface, OMR integration, automatic analysis, automatic drum kicks.

## License

This project is released under the MIT License. See [`LICENSE`](LICENSE) for details.

## Contributing

The project is in early development and not yet open to external contributions. The repository is currently private and will become public at the completion of milestone M1. Contribution guidelines will be published alongside the first public release.
