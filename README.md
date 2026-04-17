# proof-engine-binder

Binder launcher for [proof-engine](https://github.com/yaniv-golan/proof-engine) proofs.

## What is this?

Each proof in the main repo is published to Zenodo as a citable artifact. This repo provides the runtime — a pinned Python environment and a launcher notebook — that lets anyone re-run any published proof in the browser with one click.

Proof pages emit a URL of the form:

```
https://mybinder.org/v2/gh/yaniv-golan/proof-engine-binder/v1.21.0?urlpath=lab%2Ftree%2Flauncher.ipynb%23doi%3D10.5281%2Fzenodo.XXXXXXX
```

The tag `v1.21.0` is immutable and pinned to proof-engine `v1.21.0`. Each proof-engine minor release gets its own launcher tag (`v1.22.0`, etc.), and published `binder_url` values in `doi.json` always reference a tag — never a branch. That way a proof minted under 1.21 continues to resolve to the exact same launcher image forever.

A mutable `v1.21` **branch** is also maintained as a "latest compatible within 1.21" alias for ad-hoc use (e.g. if someone wants to test a patched launcher manually), but it is never the target of any `binder_url`.

## Don't put proofs here

This repo intentionally has no proof content. Proofs live in the main repo and are published to Zenodo. See [`yaniv-golan/proof-engine`](https://github.com/yaniv-golan/proof-engine).
