# Global variable to store the proxy base URL
# This will be set when the server starts
_PROXY_BASE_URL = None


def setup_myst():
    import os
    import sys
    import logging

    log = logging.getLogger(__name__)

    # This is the path suffix that jupyter-server-proxy adds
    PATH_INFO = "myst-build/"

    def _get_cmd(port, base_url="/"):
        global _PROXY_BASE_URL

        # Store the proxy base URL for use in rewrite_response
        _PROXY_BASE_URL = base_url

        # Default to cwd, but can be overridden with JUPYTER_MYST_BUILD_PROXY_DIR env var
        default_dir = os.environ.get("JUPYTER_MYST_BUILD_PROXY_DIR", os.getcwd())
        if not os.path.isabs(default_dir):
            default_dir = os.path.abspath(default_dir)

        # base_url from jupyter-server-proxy includes the full path:
        # - Local: "/myst-build/"
        # - JupyterHub: "/user/{username}/myst-build/"
        # We need to strip our path_info to get the jupyter server base
        jupyter_base_url = base_url.rstrip("/")
        if jupyter_base_url.endswith("/" + PATH_INFO.rstrip("/")):
            # Remove "/myst-build" from the end
            jupyter_base_url = jupyter_base_url[: -(len(PATH_INFO.rstrip("/")) + 1)]
        if not jupyter_base_url:
            jupyter_base_url = "/"

        log.info(f"Starting static server on port {port} in directory: {default_dir}")
        log.info(
            f"base_url from proxy: {base_url}, jupyter_base_url: {jupyter_base_url}"
        )

        static_server = os.path.join(os.path.dirname(__file__), "static_server.py")
        return [sys.executable, static_server, str(port), default_dir, jupyter_base_url]

    return {
        "command": _get_cmd,
        "timeout": 60,
        "absolute_url": False,
        "path_info": PATH_INFO,
        "launcher_entry": {
            "title": "MyST Build",
            "icon_path": os.path.join(os.path.dirname(__file__), "logo-square.svg"),
        },
    }
