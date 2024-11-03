"""
GENERATE
Generate the media linked library
"""

from pathlib import Path

import click

import medialink.messages as msg
from medialink.media_classes import Film, Show
from medialink.options import Options


def generate_library(
    target: Path, films: list[Film], shows: list[Show], options: Options
) -> None:
    film_target = target / "films"
    show_target = target / "shows"
    generate_films(film_target, films, options)
    generate_shows(show_target, shows, options)


def generate_films(target: Path, films: list[Film], options: Options) -> None:
    if options.verbose:
        click.echo(msg.INTENT_TARGET_FILMS.format(film_target=target.absolute()))
    for film in films:
        try:
            film.create_link(target, options)
        except FileExistsError:
            if options.verbose:
                click.echo(f"Skipping {film.title}, file already exists")


def generate_shows(target: Path, shows: list[Show], options: Options) -> None:
    if options.verbose:
        click.echo(msg.INTENT_TARGET_SHOWS.format(show_target=target.absolute()))
    for show in shows:
        try:
            show.create_link(target, options)
        except FileExistsError:
            if options.verbose:
                click.echo(f"Skipping {show.title}, file already exists")
