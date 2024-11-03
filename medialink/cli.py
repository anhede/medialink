#!/usr/bin/env python
"""
CLI
Handles user input and runs the correct commands
"""

from pathlib import Path

import click

import medialink.messages as msg
from medialink.main import main
from medialink.options import Options


@click.command()
@click.argument(
    "source",
    required=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        path_type=Path,
    ),
)
@click.argument(
    "target",
    required=False,
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
        path_type=Path,
    ),
)
@click.option(
    "-tf",
    "--target-films",
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
        path_type=Path,
    ),
    help=msg.HELP_TARGET_FILMS,
)
@click.option(
    "-ts",
    "--target-shows",
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
        allow_dash=False,
        path_type=Path,
    ),
    help=msg.HELP_TARGET_SHOWS,
)
@click.option("-d", "--dry-run", is_flag=True, help=msg.HELP_DRY_RUN)
@click.option("-v", "--verbose", is_flag=True, help=msg.HELP_VERBOSE)
@click.version_option()
@click.help_option()
def cli(
    source: Path,
    target: Path,
    target_films: Path,
    target_shows: Path,
    verbose: bool,
    dry_run: bool,
) -> None:
    """Scan SOURCE for films and/or shows and populate TARGET with a linked library"""
    options = Options(verbose, dry_run)
    ValidateInputs(target, target_films, target_shows)
    main(source, target, target_films, target_shows, options)


def ValidateInputs(target: Path, target_films: Path, target_shows: Path) -> None:
    if not target and not target_films and not target_shows:
        raise click.UsageError(msg.ERROR_NO_TARGET)

    if target and (target_films or target_shows):
        raise click.UsageError(msg.ERROR_TARGET_CONFLICT)


if __name__ == "__main__":
    cli()
