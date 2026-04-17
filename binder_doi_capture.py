"""Capture ?doi=<Zenodo DOI> from any incoming HTTP request to /tmp/binder_doi.

Binder's redirect chain from mybinder.org to hub.*.mybinder.org preserves the
query string on the first request that hits the user's Jupyter server, but
JupyterLab's SPA router strips it from window.location.search before the
launcher widget's JavaScript can read it. This Jupyter Server extension
intercepts every completed request, extracts a valid Zenodo DOI from ?doi=,
and writes it to /tmp/binder_doi. The launcher widget reads that file on
cell execution to pre-populate the DOI input.

Hook strategy: we replace the Tornado Application's ``log_function`` in
``web_app.settings``. That's the callable Tornado actually invokes at the
end of every request; reassigning ``serverapp.log_request`` after startup
does NOT work because Tornado has already captured the reference.

DOI_FILE is intentionally in /tmp: volatile, user-scoped, no cleanup needed.
"""
import re

DOI_RE = re.compile(r"^10\.\d{4,9}/zenodo\.\d+$")
DOI_FILE = "/tmp/binder_doi"


def _capture_doi(handler):
    try:
        args = handler.request.query_arguments.get("doi", [])
        if not args:
            return
        raw = args[0]
        doi = raw.decode("ascii", errors="replace") if isinstance(raw, bytes) else raw
        if DOI_RE.fullmatch(doi):
            with open(DOI_FILE, "w") as fh:
                fh.write(doi)
    except Exception:
        # A broken capture must never break the server.
        pass


def _load_jupyter_server_extension(serverapp):
    """Replace the Tornado log_function so every completed request is inspected."""
    web_app = serverapp.web_app
    original = web_app.settings.get("log_function")

    def wrapped(handler):
        _capture_doi(handler)
        if original is not None:
            return original(handler)

    web_app.settings["log_function"] = wrapped
    serverapp.log.info("binder_doi_capture: log_function hook installed")


def _jupyter_server_extension_points():
    return [{"module": "binder_doi_capture"}]
