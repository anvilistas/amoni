# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
import time
from contextlib import contextmanager
from functools import partial
from threading import Event, Thread

import typer

__version__ = "0.0.5"

CLEAR_LINE = "\r\033[K"
ANIMATION = ("⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾")
ANIMATION_INTERVAL = 0.1


error = partial(typer.secho, fg=typer.colors.RED, err=True)
success = partial(typer.secho, fg=typer.colors.GREEN)
progress = partial(typer.secho, fg=typer.colors.CYAN)
done = partial(success, "Done! ✨️")


def _animate(message, event):
    while not event.is_set():
        for frame in ANIMATION:
            progress(f"{frame} {message}", nl=False)
            time.sleep(ANIMATION_INTERVAL)
            progress(CLEAR_LINE, nl=False)


@contextmanager
def working(message):
    """Prints a working message"""
    event = Event()
    kwargs = {"message": message, "event": event}
    thread = Thread(target=_animate, kwargs=kwargs)
    thread.start()

    try:
        yield
    finally:
        event.set()
        thread.join()
