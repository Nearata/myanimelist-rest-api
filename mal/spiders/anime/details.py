from datetime import datetime
from mal.spiders.utils import get_soup
from mal.spiders.anime.helpers.details import *


class Details:
    none_found = "none found"

    def __init__(self, base_url, mal_id) -> None:
        self.base_url = base_url
        self.mal_id = mal_id
        self.soup = get_soup(f"{base_url}/anime/{mal_id}")

    def get(self):
        for i in self.soup.select("h1 > .h1-title > span[itemprop=name]"):
            if i.br:
                i.br.decompose()
            if i.span:
                i.span.decompose()

        anime_title = self.soup.select_one("h1 > .h1-title > span").get_text()

        return {
            "details": {
                "title": anime_title,
                "image": self.soup.find("img", alt=anime_title).get("data-src"),
                "trailer": trailer_helper(self.soup),
                "synopsis": synopsis_helper(self.soup),
                "background": background_helper(self.soup),
                "alternative_titles": {
                    "english": self.__alternative_titles_helper("English:"),
                    "japanese": self.__alternative_titles_helper("Japanese:"),
                    "synonyms": synonyms_helper(self.soup),
                },
                "information": {
                    "type": self.soup.find("span", string="Type:").find_next_sibling("a").get_text(),
                    "episodes": episodes_helper(self.soup),
                    "status": self.soup.find("span", string="Status:").next_sibling.strip(),
                    "aired": {
                        "from": self.__information_aired_helper(0),
                        "to": self.__information_aired_helper(1)
                    },
                    "premiered": premiered_helper(self.soup),
                    "producers": producers_helper(self.soup, self.none_found, self.base_url),
                    "licensors": licensors_helper(self.soup, self.none_found, self.base_url),
                    "studios": studios_helper(self.soup, self.none_found, self.base_url),
                    "source": self.__alternative_titles_helper("Source:"),
                    "genres": genres_helper(self.soup),
                    "duration": duration_helper(self.soup),
                    "rating": rating_helper(self.soup)
                },
                "statistics": {
                    "score": score_helper(self.soup),
                    "ranked": self.__statistics_helper("Ranked:", "#"),
                    "popularity": self.__statistics_helper("Popularity:", "#"),
                    "members": self.__statistics_helper("Members:"),
                    "favorites": self.__statistics_helper("Favorites:")
                },
                "related_anime": {
                    "adaptation": self.__related_anime_helper("Adaptation:"),
                    "side_story": self.__related_anime_helper("Side story:"),
                    "summary": self.__related_anime_helper("Summary:"),
                    "spin_off": self.__related_anime_helper("Spin-off:"),
                    "other": self.__related_anime_helper("Other:"),
                    "prequel": self.__related_anime_helper("Prequel:"),
                    "character": self.__related_anime_helper("Character:"),
                    "sequel": self.__related_anime_helper("Sequel:")
                },
                "opening_theme": self.__theme_song_helper("opnening"),
                "ending_theme": self.__theme_song_helper("ending")
            }
        }

    def __related_anime_helper(self, string):
        related_anime = self.soup.find("td", string=string)
        if related_anime:
            return [
                {
                    "title": i.get_text(),
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in related_anime.next_sibling.select("a")
            ]
        return []

    def __theme_song_helper(self, string):
        theme_song = self.soup.select(f"div.{string} > span.theme-song")
        if theme_song:
            return [
                {
                    "title": i.get_text(strip=True)
                } for i in theme_song
            ]
        return []

    def __statistics_helper(self, field, replace=","):
        try:
            return int(self.soup.find("span", string=field).next_sibling.replace(replace, "").strip())
        except ValueError:
            return None

    def __alternative_titles_helper(self, field_name):
        field = self.soup.find("span", string=field_name)
        if field:
            return field.next_sibling.strip()
        return None

    def __information_aired_helper(self, index):
        aired = self.soup.find("span", string="Aired:").next_sibling

        if aired.strip() == "Not available":
            return None

        if index == 1 and aired.split("to")[index].strip() == "?":
            return None

        try:
            return str(datetime.strptime(aired.split("to")[index].strip(), "%b %d, %Y").date())
        except ValueError:
            return str(datetime.strptime(aired.split("to")[index].strip(), "%b, %Y").date())
