import os
import sys
import tempfile


def effective_access(*args, **kwargs):
    if 'effective_ids' not in kwargs:
        try:
            kwargs['effective_ids'] = os.access in os.supports_effective_ids
        except AttributeError:
            pass

    return os.access(*args, **kwargs)


def determine_pid_directory():
    if sys.platform == "win32":
        return tempfile.gettempdir()

    uid = os.geteuid() if hasattr(os, "geteuid") else os.getuid()

    paths = [
        "/run/user/%s/" % uid,
        "/var/run/user/%s/" % uid,
        "/run/",
        "/var/run/",
    ]

    for path in paths:
        if effective_access(path, os.W_OK | os.X_OK):
            return path

    return tempfile.gettempdir()