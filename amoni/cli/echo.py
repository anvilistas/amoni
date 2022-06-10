# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni

from functools import partial

import typer

error = partial(typer.secho, fg=typer.colors.RED, err=True)
success = partial(typer.secho, fg=typer.colors.GREEN)
progress = partial(typer.secho, fg=typer.colors.CYAN)
done = partial(success, "Done! ✨️")
