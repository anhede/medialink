import os
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import final

from medialink.options import Options


class Media:
    path: Path
    title: str
    year: int | None

    def __init__(self, path: Path, guess: dict):
        self.path = path
        title = guess.get("title")
        if not title:
            title = path.stem
        year = guess.get("year")
        if not title or not path:
            raise ValueError("Media must have a title and a path")
        self.title = title
        self.year = year


class Collection(metaclass=ABCMeta):
    """Collections are composed of a single film or show. They are a complete
    collection of media which can be linked to a single folder"""

    @abstractmethod
    def create_link(self, parent_folder: Path, options: Options) -> None:
        """Create a hardlink and folder for this collection"""
        raise NotImplementedError("Subclasses must implement this method")


# Films are standalone media
@final
class Film(Media, Collection):
    """A standalone film"""

    def __init__(self, path: Path, guess: dict, options: Options):
        super().__init__(path, guess)
        if not self.year and options.require_film_year:
            raise ValueError("Film must have a year")

    def create_link(self, parent_folder: Path, options: Options) -> None:
        """Create a hardlink and folder for this film"""

        folder = parent_folder / f"{self.title} ({self.year})"
        link = folder / f"{self.title} ({self.year}){self.path.suffix}"
        if options.verbose:
            print(f"{self.path.name}\n\t----> {link.name}")
        if not options.dry_run:
            folder.mkdir(parents=True, exist_ok=True)
            os.link(self.path, link)

    def pprint(self) -> str:
        return f"{self.title} ({self.year})"


# Shows are composed of episodes in seasons and shows
@final
class Episode(Media):
    """An episode of a show"""

    season: int
    episode: int
    episode_title: str | None

    def __init__(self, path: Path, guess: dict):
        super().__init__(path, guess)
        season_guess = guess.get("season")
        episode_guess = guess.get("episode")
        episode_title_guess = guess.get("episode_title")
        if not season_guess:
            self.season = 1
        else:
            self.season = season_guess

        if not episode_guess:
            self.episode = 0
        else:
            self.episode = episode_guess

        self.episode_title = episode_title_guess  # allow for None

    def pprint(self) -> str:
        return f"\t\t{self.title} S{self.season:02}E{self.episode:02}"


@final
class Season:
    """A season of a show"""

    season: int
    episodes: list[Episode]

    def __init__(self, season: int):
        self.season = season
        self.episodes = []

    def add_episode(self, episode: Episode) -> None:
        self.episodes.append(episode)
        self.sort_episodes()

    def sort_episodes(self) -> None:
        self.episodes.sort(key=lambda x: x.episode)

    def pprint(self) -> str:
        s = f"\tSeason {self.season}\n"
        for episode in self.episodes:
            s += f"{episode.pprint()}\n"
        return s


@final
class Show(Collection):
    """A show"""

    title: str
    seasons: dict[int, Season]

    def __init__(self, title: str):
        self.title = title
        self.seasons = {}

    def sort_seasons(self) -> None:
        self.seasons = dict(sorted(self.seasons.items()))

    def add_episode(self, episode: Episode) -> None:
        if self.seasons.get(episode.season):
            self.seasons[episode.season].add_episode(episode)
        else:
            season = Season(episode.season)
            season.add_episode(episode)
            self.seasons[episode.season] = season
            self.sort_seasons()

    def create_link(self, parent_folder: Path, options: Options) -> None:
        """Create a hardlink and folder for this show"""
        # For each episode in each season, create a hardlink
        for season in self.seasons.values():
            for episode in season.episodes:
                folder = parent_folder / self.title / f"Season {season.season}"
                link = (
                    folder
                    / f"{episode.title} S{episode.season:02}E{episode.episode:02}{episode.path.suffix}"  # noqa: E501
                )
                if options.verbose:
                    print(f"{episode.path.name}\n\t----> {link.name}")
                if not options.dry_run:
                    folder.mkdir(parents=True, exist_ok=True)
                    os.link(episode.path, link)

    def pprint(self) -> str:
        s = f"{self.title}\n"
        for season in self.seasons.values():
            s += season.pprint()
        return s
