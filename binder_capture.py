"""Capture proof identity from the ?doi=... OR (?slug=...&ref=...) query on any
incoming HTTP request and persist it to /tmp sentinel files.

Binder's redirect chain from mybinder.org to hub.*.mybinder.org preserves the
query string on the first request that hits the user's Jupyter server, but
JupyterLab's SPA router strips it from window.location.search before the
launcher's JavaScript can read it. This Jupyter Server extension intercepts
every completed request, extracts a valid proof identifier from the query
string, and writes it to /tmp. The launcher notebook reads those files on
cell execution to decide which proof.py to fetch and execute.

Two mutually-exclusive capture modes:
- DOI mode:  ?doi=<Zenodo DOI>         → /tmp/binder_doi
- Slug mode: ?slug=<slug>&ref=<sha>    → /tmp/binder_slug + /tmp/binder_ref

DOI takes precedence if both are present on the same request.

Hook strategy: we replace the Tornado Application's ``log_function`` in
``web_app.settings``. That's the callable Tornado actually invokes at the
end of every request; reassigning ``serverapp.log_request`` after startup
does NOT work because Tornado has already captured the reference.

Sentinel files are intentionally in /tmp: volatile, user-scoped, no cleanup.
"""
import re

DOI_RE = re.compile(r"^10\.\d{4,9}/zenodo\.\d+$")
SLUG_RE = re.compile(r"^[a-z0-9-]{1,80}$")
REF_RE = re.compile(r"^[0-9a-f]{7,40}$")

DOI_FILE = "/tmp/binder_doi"
SLUG_FILE = "/tmp/binder_slug"
REF_FILE = "/tmp/binder_ref"


def _decode(raw) -> str:
    return raw.decode("ascii", errors="replace") if isinstance(raw, bytes) else raw


def _capture(handler):
    try:
        q = handler.request.query_arguments

        # DOI takes precedence if both are present.
        doi_args = q.get("doi", [])
        if doi_args:
            doi = _decode(doi_args[0])
            if DOI_RE.fullmatch(doi):
                with open(DOI_FILE, "w") as fh:
                    fh.write(doi)
                return

        slug_args = q.get("slug", [])
        ref_args = q.get("ref", [])
        if slug_args and ref_args:
            slug = _decode(slug_args[0])
            ref = _decode(ref_args[0])
            if SLUG_RE.fullmatch(slug) and REF_RE.fullmatch(ref):
                with open(SLUG_FILE, "w") as fh:
                    fh.write(slug)
                with open(REF_FILE, "w") as fh:
                    fh.write(ref)
    except Exception:
        # A broken capture must never break the server.
        pass


def _load_jupyter_server_extension(serverapp):
    """Replace the Tornado log_function so every completed request is inspected."""
    web_app = serverapp.web_app
    original = web_app.settings.get("log_function")

    def wrapped(handler):
        _capture(handler)
        if original is not None:
            return original(handler)

    web_app.settings["log_function"] = wrapped
    serverapp.log.info("binder_capture: log_function hook installed")


def _jupyter_server_extension_points():
    return [{"module": "binder_capture"}]
