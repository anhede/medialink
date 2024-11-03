"""
SCAN
Scan folders for media files
"""

from pathlib import Path

import click
from guessit import guessit  # type: ignore

from medialink.media_classes import Episode, Film, Show
from medialink.options import Options


def scan(source: Path, options: Options) -> tuple[list[Film], list[Show]]:
    media = get_media_files(source, options)
    films, shows = sort_media_files(media)
    if options.verbose:
        click.echo(
            f"Found {len(films)} films and {len(shows)} shows with a total of"
            f" {len(media)} video files"
        )
    return films, shows


def get_media_files(source: Path, options: Options) -> list[Film | Episode]:
    # Get valid video formats
    videoformats = []
    with open(Path(__file__).parent / "videoformats.txt") as file:
        for line in file:
            videoformats.append(line.strip())

    # Scan source folder and all subfolders for media files
    media = []
    for path in source.rglob("*"):
        if path.is_file() and path.suffix[1:] in videoformats:
            media_type = create_media_object(path, options)
            if media_type:
                if options.verbose:
                    click.echo(f"Found {type(media_type).__name__} {path.name}")
                media.append(media_type)
            elif options.verbose:
                click.echo(f"Skipping {path.name}, unable to determine media type")
    return media


def create_media_object(path: Path, options: Options) -> Film | Episode | None:
    try:
        guess = guessit(path.name)
        if guess["type"] == "movie":
            return Film(path, guess, options)
        if guess["type"] == "episode":
            return Episode(path, guess)
        else:
            return None
    except KeyError:
        return None
    except ValueError:
        return None


def sort_media_files(media: list[Film | Episode]) -> tuple[list[Film], list[Show]]:
    films = []
    shows: dict[str, Show] = dict()
    for item in media:
        if isinstance(item, Film):
            films.append(item)
        elif isinstance(item, Episode):
            # Check if show already exists
            if shows.get(item.title):
                shows[item.title].add_episode(item)
            else:
                show = Show(item.title)
                show.add_episode(item)
                shows[item.title] = show
    return films, list(shows.values())


if __name__ == "__main__":
    media = get_media_files(
        Path("/home/copper/medialink/empty-media-lib"), Options(True, False)
    )
    films, shows = sort_media_files(media)
    print("FILMS ----------------")
    for film in films:
        print(film.pprint())
    print("SHOWS ----------------")
    for show in shows:
        print(show.pprint())

    click.echo(
        f"Found {len(films)} films and {len(shows)} shows with a total of"
        f" {len(media)} video files"
    )
