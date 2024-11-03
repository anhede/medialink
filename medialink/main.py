from pathlib import Path

from medialink.generate import generate_films, generate_library, generate_shows
from medialink.options import Options
from medialink.scan import scan


def main(
    source: Path, target: Path, target_films: Path, target_shows: Path, options: Options
) -> None:
    films, shows = scan(source, options)
    if target:
        generate_library(target, films, shows, options)
    if target_films:
        generate_films(target_films, films, options)
    if target_shows:
        generate_shows(target_shows, shows, options)
