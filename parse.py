from itertools import repeat

from trakt import (
    Episode,
    EpisodeRow,
    HistoryEpisode,
    HistoryEpisodeRow,
    HistoryMovie,
    HistoryMovieRow,
    Movie,
    MovieRow,
    Season,
    Show,
    ShowRow,
)


class Commons:
    def episode_to_episode_row(self, entry: Episode, show_id: int) -> EpisodeRow:
        return {
            "type": "episode",
            "id": entry["ids"]["trakt"],
            "show_id": show_id,
            "season": entry["season"],
            "number": entry["number"],
            "title": entry["title"],
            "trakt_id": entry["ids"]["trakt"],
            "tvdb_id": entry["ids"]["tvdb"],
            "imdb_id": entry["ids"]["imdb"],
            "tmdb_id": entry["ids"]["tmdb"],
            "tvrage_id": entry["ids"]["tvrage"],
        }

    def show_to_show_row(self, entry: Show) -> ShowRow:
        return {
            "type": "show",
            "id": entry["ids"]["trakt"],
            "title": entry["title"],
            "year": entry["year"],
            "trakt_id": entry["ids"]["trakt"],
            "trakt_slug": entry["ids"]["slug"],
            "tvdb_id": entry["ids"]["tvdb"],
            "imdb_id": entry["ids"]["imdb"],
            "tmdb_id": entry["ids"]["tmdb"],
            "tvrage_id": entry["ids"]["tvrage"],
        }

    def multiple_seasons_to_list_episode_row(self, entry: list[Season]) -> list[EpisodeRow]:
        # return list(map(self.season_to_episode_rows, entry)) # Gives 2D list.
        start: list[EpisodeRow] = []
        return sum(list(map(self.season_to_list_episode_row, entry)), start)

    def season_to_list_episode_row(self, entry: Season) -> list[EpisodeRow]:
        show_id = entry["ids"]["trakt"]
        episodes: list[Episode] = entry["episodes"]
        return list(map(self.episode_to_episode_row, episodes, repeat(show_id)))

    def movie_to_movie_row(self, entry: Movie) -> MovieRow:
        return {
            "type": "movie",
            "id": entry["ids"]["trakt"],
            "title": entry["title"],
            "year": entry["year"],
            "trakt_id": entry["ids"]["trakt"],
            "trakt_slug": entry["ids"]["slug"],
            "imdb_id": entry["ids"]["imdb"],
            "tmdb_id": entry["ids"]["tmdb"],
        }


class History:
    # Parse API Data, history_episodes to sqlite rows.
    def entry_to_history_episode_row(self, entry: HistoryEpisode) -> HistoryEpisodeRow:
        return {
            "id": entry["id"],
            "type": "episode",
            "media_id": entry["episode"]["ids"]["trakt"],
            "watched_at": entry["watched_at"],
        }

    def entry_to_episode(self, entry: HistoryEpisode) -> Episode:
        return entry["episode"]

    def entry_to_show(self, entry: HistoryEpisode) -> Show:
        return entry["show"]

    def get_show_id_from_entry(self, entry: HistoryEpisode) -> int:
        return entry["show"]["ids"]["trakt"]

    def handle_history_episode_entry(
        self,
        entry: HistoryEpisode,
    ) -> tuple[HistoryEpisodeRow, EpisodeRow, ShowRow]:
        c = Commons()
        h_ep_row = self.entry_to_history_episode_row(entry)
        show_id = self.get_show_id_from_entry(entry)
        ep_row = c.episode_to_episode_row(self.entry_to_episode(entry), show_id)
        s_row = c.show_to_show_row(self.entry_to_show(entry))
        return (h_ep_row, ep_row, s_row)

    # Parse API Data, history_movies to sqlite rows.
    def entry_to_history_movie_row(self, entry: HistoryMovie) -> HistoryMovieRow:
        return {
            "id": entry["id"],
            "type": "movie",
            "media_id": entry["movie"]["ids"]["trakt"],
            "watched_at": entry["watched_at"],
        }

    def entry_to_movie(self, entry: HistoryMovie) -> Movie:
        return entry["movie"]

    def handle_history_movie_entry(
        self,
        entry: HistoryMovie,
    ) -> tuple[HistoryMovieRow, MovieRow]:
        c = Commons()
        h_m_row = self.entry_to_history_movie_row(entry)
        m_row = c.movie_to_movie_row(self.entry_to_movie(entry))
        return (h_m_row, m_row)
