from typing import Literal, Optional, TypedDict

USER_AGENT = "trakt-to-sqlite"


class Show(TypedDict):
    type: Literal["show"]
    id: int  # ids.trakt, will be treated as primary key.
    title: str  # "Parks and Recreation"
    year: int  # 2009
    trakt_id: int  # 8546
    trakt_slug: str  # "parks-and-recreation"
    tvdb_id: int  # 84912
    imdb_id: str  # "tt1266020"
    tmdb_id: int  # 8592
    tvrage_id: int  # 21686


class Episode(TypedDict):
    type: Literal["episode"]
    id: int  # ids.trakt, will be treated as primary key.
    show_id: int  # Foreign Key
    season: int  # 2
    number: int  # 5
    title: str  # "Sister City"
    trakt_id: int  # 406221
    tvdb_id: int  # 1088061
    imdb_id: str  # "tt1504148"
    tmdb_id: int  # 397635
    tvrage_id: Optional[int]  # None


class CollectedEpisode(Episode):
    id: int  # Primary Key
    episode_id: int
    collected: bool  # False
    collected_at: float  # "2019-09-24T09:03:22.000Z"


class RatedEpisode(Episode):
    id: int  # Primary Key
    episode_id: int
    rating: int  # 9
    rated_at: float  # "2019-09-24T09:03:22.000Z"


class PlayedEpisode(Episode):
    id: int  # Primary Key
    episode_id: int
    total_plays: int  # 10
    last_watched_at: float  # "2019-09-24T09:03:22.000Z"


class Movie(TypedDict):
    type: Literal["movie"]
    id: int  # ids.trakt, will be treated as primary key.
    title: str  # "A Quiet Place"
    year: int  # 2018
    trakt_id: int  # 293955
    trakt_slug: str  # "a-quiet-place-2018"
    imdb_id: str  # "tt6644200"
    tmdb_id: int  # 447332


class CollectedMovie(Movie):
    id: int  # Primary Key
    movie_id: int
    collected: bool  # False
    collected_at: float  # "2019-09-24T09:03:22.000Z"


class RatedMovie(Movie):
    id: int  # Primary Key
    movie_id: int
    rating: int  # 9
    rated_at: float  # "2019-09-24T09:03:22.000Z"


class PlayedMovie(Movie):
    id: int  # Primary Key
    movie_id: int
    total_plays: int  # 10
    last_watched_at: float  # "2019-09-24T09:03:22.000Z"
