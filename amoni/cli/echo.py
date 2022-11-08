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

__version__ = "0.0.11"

CLEAR_LINE = "\r\033[K"
EMOJI_ANIMATION = {"frames": ("⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"), "interval": 0.1}
ASCII_ANIMATION = {"frames": ("   ", ".  ", ".. ", "..."), "interval": 0.5}
DECORATIONS = {"error": "⛔", "done": "✨️"}


def _emojis_work():
    emojis = "".join(EMOJI_ANIMATION) + "".join(DECORATIONS.values())
    try:
        emojis.encode()
        return True
    except UnicodeEncodeError:
        return False


def _decorate(message, decoration):
    return f"{DECORATIONS[decoration]} {message}" if _emojis_work() else message


def error(message):
    typer.secho(_decorate(message, "error"), fg=typer.colors.RED, err=True)


def done():
    typer.secho(_decorate("Done!", "done"), fg=typer.colors.GREEN)


progress = partial(typer.secho, fg=typer.colors.CYAN)


def _animate(message, event):
    animation = EMOJI_ANIMATION if _emojis_work() else ASCII_ANIMATION
    while not event.is_set():
        for frame in animation["frames"]:
            progress(f"{frame} {message}", nl=False)
            time.sleep(animation["interval"])
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
