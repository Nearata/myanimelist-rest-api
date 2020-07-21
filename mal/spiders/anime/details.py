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
                    "english": english_helper(self.soup),
                    "japanese": japanese_helper(self.soup),
                    "synonyms": synonyms_helper(self.soup),
                },
                "information": {
                    "type": self.soup.find("span", string="Type:").find_next_sibling("a").get_text(),
                    "episodes": episodes_helper(self.soup),
                    "status": self.soup.find("span", string="Status:").next_sibling.strip(),
                    "aired": {
                        "from": aired_from_helper(self.soup),
                        "to": aired_to_helper(self.soup)
                    },
                    "premiered": premiered_helper(self.soup),
                    "producers": producers_helper(self.soup, self.none_found, self.base_url),
                    "licensors": licensors_helper(self.soup, self.none_found, self.base_url),
                    "studios": studios_helper(self.soup, self.none_found, self.base_url),
                    "source": source_helper(self.soup),
                    "genres": genres_helper(self.soup),
                    "duration": duration_helper(self.soup),
                    "rating": rating_helper(self.soup)
                },
                "statistics": {
                    "score": score_helper(self.soup),
                    "ranked": ranked_helper(self.soup),
                    "popularity": popularity_helper(self.soup),
                    "members": members_helper(self.soup),
                    "favorites": favorites_helper(self.soup)
                },
                "related_anime": {
                    "adaptation": adaptation_helper(self.soup),
                    "side_story": side_story_helper(self.soup),
                    "summary": summary_helper(self.soup),
                    "spin_off": spin_off_helper(self.soup),
                    "other": other_helper(self.soup),
                    "prequel": prequel_helper(self.soup),
                    "character": character_helper(self.soup),
                    "sequel": sequel_helper(self.soup)
                },
                "opening_theme": opening_theme_helper(self.soup),
                "ending_theme": ending_theme_helper(self.soup)
            }
        }
