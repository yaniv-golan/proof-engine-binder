# Changelog

All notable changes to the proof-engine launcher are documented here.

## [1.21.2] - 2026-04-18

### Changed
- **BREAKING (UX):** Launcher notebook rewritten from a single widget-driven cell to six transparent cells: DOI config, Zenodo fetch, execute, verdict. No widgets, no hidden orchestration — every step in an inspectable cell. Aligns with proof-engine's "don't trust, verify" value proposition.
- Source-code display moved to the proof page itself (in proof-engine `site/templates/proof.html`'s new "View proof source" section). The launcher is now execution-only — auditors inspect source on the page before clicking "Re-execute this proof yourself".
- Proof output streams live via a `Tee` stdout wrapper while simultaneously capturing to a buffer for verdict extraction. One exec per verification (previously: two via the widget observer pattern).
- Verdict extraction prefers the canonical `=== PROOF SUMMARY (JSON) ===` block and falls back to regex across legacy print formats — covers both current and older proofs in one pass.

### Removed
- `anywidget`-based DOIReader widget. The DOI is read directly from `/tmp/binder_doi` (preloaded by the existing `binder_doi_capture` server extension) with a clear comment to edit the variable for ad-hoc use. `anywidget` remains in `requirements.txt` for future cells; the core flow no longer imports it.

### Migration
- Tag `v1.21.0` is force-moved for the fourth time. Published `binder_url` values in `doi.json` files continue to resolve. No action required for proof pages or minted DOIs.
- Companion to proof-engine commit (Track 1) that adds inline source display to proof pages. Both should ship together for the coordinated UX to make sense.
