# Changelog

All notable changes to the proof-engine launcher are documented here.

## [1.24.0] - 2026-04-19

### Changed
- **`postBuild` bumps `PROOF_ENGINE_TAG` to `v1.24.0`.** Companion to proof-engine v1.24.0 (`prove_holds()` theorem-mode verdict helper + proofengine.info migration + skim guide + Binder deps note + numpy scalar coercion). No launcher behavior changes — this tag exists to satisfy the cross-tag invariant (BINDER_LAUNCHER_TAG in proof-engine derives from `vMAJOR.MINOR.0` only, so every proof-engine minor release needs a matching launcher tag).

## [1.23.1] - 2026-04-18

### Fixed
- **Cell 3 robustness: `captured` is now assigned inside the `finally` block** (and pre-initialised to `""` before the `try`). Previously, if `exec(proof_text)` raised, `captured = proof_output.getvalue()` was unreachable — the user then saw cell 4 fail with an unhelpful `NameError: name 'captured' is not defined` that buried whatever the actual proof failure was. The exception still propagates from cell 3 (so Jupyter halts the run-all chain at the real error), but if the user manually re-runs cell 4 after a cell 3 failure, the partial output is now available and cell 4 falls through to "Verdict: UNKNOWN" instead of erroring. Surfaced by Playwright-driven smoke testing of v1.23.0.

## [1.23.0] - 2026-04-18

### Changed
- **`postBuild` bumps `PROOF_ENGINE_TAG` to `v1.23.0`.** Companion to proof-engine v1.23.0 (SKILL.md restructure: gotchas regrouped under 7 subheadings, Step 2 mid-section extracted to `references/research-workflow.md`, function signatures extracted to `references/scripts-api.md`). No launcher behavior changes — this tag exists to satisfy the cross-tag invariant (BINDER_LAUNCHER_TAG in proof-engine derives from `vMAJOR.MINOR.0` only).

### Post-tag fix (v1.23.0 force-moved 2026-04-18)
- Tag `v1.23.0` was force-moved onto the same commit shipped as `v1.23.1` (cell 3 robustness fix — `captured` now assigned inside `finally`). Both tags now resolve to the same image. The force-move is required because `BINDER_LAUNCHER_TAG` in proof-engine derives from `vMAJOR.MINOR.0` only; without it, every site-published Binder URL would still pull the buggy pre-fix image. See [1.23.1] below for the actual fix.

## [1.22.0] - 2026-04-18

### Added
- **Dual-mode capture: DOI and slug.** The server extension now captures both `?doi=<Zenodo DOI>` (existing minted-proof flow) and `?slug=<slug>&ref=<sha>` (new unminted-proof flow) on incoming requests. Slug mode fetches `proof.py` from `raw.githubusercontent.com/yaniv-golan/proof-engine/<sha>/site/proofs/<slug>/proof.py` — the trust anchor is the commit SHA embedded in the URL, so the executed bytes match the bytes rendered in "View proof source" on the proof's page at that commit. Enables one-click re-execution for the ~53 published proofs that have no DOI yet.
- Launcher notebook cells 1, 2, and 4 branch on `MODE ∈ {"doi", "slug"}`. Cell 2 exports a single `proof_script_name` variable so cell 3 no longer references mode-specific locals. Cell 4's back-link resolves via `doi-index.json` in DOI mode or directly from the captured slug in slug mode, and reports the pinned commit short-SHA instead of a Zenodo link.

### Changed
- **Extension renamed: `binder_doi_capture` → `binder_capture`.** Module, Python file, and the Jupyter Server extension JSON config all rename in lockstep. DOI regex unchanged; new validators: slug `^[a-z0-9-]{1,80}$`, ref `^[0-9a-f]{7,40}$`. DOI takes precedence if both query parameters are present on the same request.
- **`postBuild` bumps `PROOF_ENGINE_TAG` to `v1.22.0`.** The cloned `proof-engine` repo in the image now matches this launcher's minor version.

### Migration
- Companion to proof-engine v1.22.0 which emits `?slug=&ref=` URLs for unminted proofs. Published `doi.json` `binder_url` values continue to resolve (DOI path unchanged). A stale browser tab holding a Binder URL pointing at a pre-1.22.0 launcher image will fall back to the built-in example DOI rather than crash.

### Post-tag fix (v1.22.0 force-moved 2026-04-18)
- Cell 0's intro markdown was DOI-only ("re-runs the exact `proof.py` deposited to Zenodo") despite the underlying flow being dual-mode. Updated to describe both source paths (Zenodo for minted, GitHub raw + commit-SHA for unminted) and to point users at the correct re-verification path for each (`DOI_OVERRIDE` vs. clicking from the proof page). Tag `v1.22.0` was force-moved to the new commit because `BINDER_LAUNCHER_TAG` in the main repo derives from `vMAJOR.MINOR.0` only — within a minor we move the tag rather than patch-bump.

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
