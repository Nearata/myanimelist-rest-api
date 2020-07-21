from datetime import datetime
from mal.spiders.utils import get_soup


class Details:
    def __init__(self, base_url, mal_id) -> None:
        self.base_url = base_url
        self.soup = get_soup(f"{base_url}/anime/{mal_id}")
        self.none_found = "none found"

    def get(self):
        for i in self.soup.select("h1 > .h1-title > span[itemprop=name]"):
            i.br.decompose()
            i.span.decompose()

        anime_title = self.soup.select_one("h1 > .h1-title > span").get_text()

        return {
            "details": {
                "title": anime_title,
                "image": self.soup.find("img", alt=anime_title).get("data-src"),
                "trailer": self.__trailer(),
                "synopsis": self.__synopsis(),
                "background": self.__background(),
                "alternative_titles": {
                    "english": self.__english(),
                    "japanese": self.__japanese(),
                    "synonyms": self.__synonyms(),
                },
                "information": {
                    "type": self.soup.find("span", string="Type:").find_next_sibling("a").get_text(),
                    "episodes": self.__episodes(),
                    "status": self.soup.find("span", string="Status:").next_sibling.strip(),
                    "aired": {
                        "from": self.__aired_from(),
                        "to": self.__aired_to()
                    },
                    "premiered": self.__premiered(),
                    "producers": self.__producers(),
                    "licensors": self.__licensors(),
                    "studios": self.__studios(),
                    "source": self.__source(),
                    "genres": self.__genres(),
                    "duration": self.__duration(),
                    "rating": self.__rating()
                },
                "statistics": {
                    "score": self.__score(),
                    "ranked": self.__ranked(),
                    "popularity": self.__popularity(),
                    "members": self.__members(),
                    "favorites": self.__favorites()
                },
                "related_anime": {
                    "adaptation": self.__adaptation(),
                    "side_story": self.__side_story(),
                    "summary": self.__summary(),
                    "spin_off": self.__spin_off(),
                    "other": self.__other(),
                    "prequel": self.__prequel(),
                    "character": self.__character(),
                    "sequel": self.__sequel()
                },
                "opening_theme": self.__opening_theme(),
                "ending_theme": self.__ending_theme()
            }
        }

    def __trailer(self):
        trailer = self.soup.select_one(".video-promotion > .promotion")
        if trailer:
            return trailer.get("href")
        return None

    def __synopsis(self):
        synopsis = self.soup.select_one("span[itemprop=description]")
        if synopsis:
            return synopsis.get_text(strip=True)
        return None

    def __background(self):
        background = self.soup.select_one("span[itemprop=description]").parent
        for i in background.select("h2, span, div"):
            i.decompose()

        if not background.get_text().lower().startswith("no background"):
            return background.get_text()
        return None

    def __english(self):
        english = self.soup.find("span", string="English:")
        if english:
            return english.next_sibling.strip()
        return None

    def __japanese(self):
        japanese = self.soup.find("span", string="Japanese:")
        if japanese:
            return japanese.next_sibling.strip()
        return None

    def __synonyms(self):
        synonyms = self.soup.find("span", string="Synonyms:")
        if synonyms:
            return [
                i.strip()
                for i in synonyms.next_sibling.split(",")
            ]
        return []

    def __episodes(self):
        episdes = self.soup.find("span", string="Episodes:").next_sibling
        if episdes.strip() != "Unknown":
            return int(episdes)
        return None

    def __aired_from(self):
        aired_from = self.soup.find("span", string="Aired:").next_sibling
        if aired_from.strip() != "Not available":
            try:
                aired_from_date = datetime.strptime(
                    aired_from.split("to")[0].strip(),
                    "%b %d, %Y"
                ).date()
            except ValueError:
                aired_from_date = datetime.strptime(
                    aired_from.split("to")[0].strip(),
                    "%b, %Y"
                ).date()
            return str(aired_from_date)
        return None

    def __aired_to(self):
        aired_to = self.soup.find("span", string="Aired:").next_sibling
        if aired_to.split("to")[1].strip() != "?":
            try:
                aired_to_date = datetime.strptime(
                    aired_to.split("to")[1].strip(),
                    "%b %d, %Y"
                ).date()
            except ValueError:
                aired_to_date = datetime.strptime(
                    aired_to.split("to")[1].strip(),
                    "%b, %Y"
                ).date()
            return str(aired_to_date)
        return None

    def __premiered(self):
        premiered = self.soup.find("span", string="Premiered:")
        if premiered.next_sibling.strip() != "?":
            return premiered.parent.find("a").get_text()
        return None
    
    def __producers(self):
        producers = self.soup.find("span", string="Producers:")
        if self.none_found not in producers.next_sibling.strip().lower():
            return [
                {
                    "name": i.get_text(),
                    "url": f"{self.base_url}{i.get('href')}",
                    "mal_id": self.__str_to_int(i.get("href").split("/"))
                } for i in producers.find_next_siblings("a")
            ]
        return []

    def __licensors(self):
        if self.none_found not in self.soup.find(
                "span", string="Licensors:").next_sibling.strip().lower():
            return [
                {
                    "name": i.get_text(),
                    "url": f"{self.base_url}{i.get('href')}",
                    "mal_id": self.__str_to_int(i.get("href").split("/"))
                } for i in self.soup.find(
                    "span", string="Licensors:").find_next_siblings("a")
            ]
        return []

    def __studios(self):
        studios = self.soup.find("span", string="Studios:")
        if self.none_found not in studios.next_sibling.strip().lower():
            return [
                {
                    "name": i.get_text(),
                    "url": f"{self.base_url}{i.get('href')}",
                    "mal_id": self.__str_to_int(i.get("href").split("/"))
                } for i in studios.find_next_siblings("a")
            ]
        return []

    def __source(self):
        source = self.soup.find("span", string="Source:")
        if source:
            return source.next_sibling.strip()
        return None

    def __genres(self):
        genres = self.soup.find("span", string="Genres:")
        if genres:
            return [
                {
                    "name": i.get_text(),
                    "mal_id": self.__str_to_int(i.get("href").split("/"))
                } for i in genres.find_next_siblings("a")
            ]
        return []

    def __duration(self):
        duration = self.soup.find("span", string="Duration:").next_sibling.strip()
        if duration != "Unknown":
            return self.__str_to_int(duration)
        return None

    def __rating(self):
        rating = self.soup.find("span", string="Rating:").next_sibling.strip()
        if rating.lower() != "none":
            return rating
        return None

    def __score(self):
        score = self.soup.find("span", itemprop="ratingValue")
        if score:
            return float(score.get_text())
        return None

    def __ranked(self):
        try:
            return int(self.soup.find(
                "span",
                string="Ranked:").next_sibling.replace("#", "").strip())
        except ValueError:
            return None
        return None

    def __popularity(self):
        try:
            return int(self.soup.find(
                "span",
                string="Popularity:").next_sibling.replace("#", "").strip())
        except ValueError:
            return None
        return None

    def __members(self):
        try:
            return int(self.soup.find(
                "span",
                string="Members:").next_sibling.replace(",", "").strip())
        except ValueError:
            return None
        return None

    def __favorites(self):
        try:
            return int(self.soup.find(
                "span",
                string="Favorites:").next_sibling.replace(",", "").strip())
        except ValueError:
            return None
        return None

    def __adaptation(self):
        adaptation = self.soup.find("td", string="Adaptation:")
        if adaptation:
            return [
                {
                    "title": i.get_text(),
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in adaptation.next_sibling.select("a")
            ]
        return []

    def __side_story(self):
        side_story = self.soup.find("td", string="Side story:")
        if side_story:
            return [
                {
                    "title": i.get_text(),
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in side_story.next_sibling.select("a")
            ]
        return []

    def __summary(self):
        summary = self.soup.find("td", string="Summary:")
        if summary:
            return [
                {
                    "title": i.get_text(),
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in summary.next_sibling.select("a")
            ]
        return []

    def __spin_off(self):
        spin_off = self.soup.find("td", string="Spin-off:")
        if spin_off:
            return [
                {
                    "title": i.get_text(),
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in spin_off.next_sibling.select("a")
            ]
        return []

    def __other(self):
        other = self.soup.find("td", string="Other:")
        if other:
            return [
                {
                    "title": i.get_text(),
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in other.next_sibling.select("a")
            ]
        return []

    def __prequel(self):
        prequel = self.soup.find("td", string="Prequel:")
        if prequel:
            return [
                {
                    "title": i.get_text(),
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in prequel.next_sibling.select("a")
            ]
        return []

    def __character(self):
        character = self.soup.find("td", string="Character:")
        if character:
            return [
                {
                    "title": i.get_text(),
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in character.next_sibling.select("a")
            ]
        return []

    def __sequel(self):
        sequel = self.soup.find("td", string="Sequel:")
        if sequel:
            return [
                {
                    "title": i.get_text(),
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in sequel.next_sibling.select("a")
            ]
        return []

    def __opening_theme(self):
        opening_theme = self.soup.select("div.opnening > span.theme-song")
        if opening_theme:
            return [
                {
                    "title": opening.get_text(strip=True)
                } for opening in opening_theme
            ]
        return []

    def __ending_theme(self):
        ending_theme = self.soup.select("div.ending > span.theme-song")
        if ending_theme:
            return [
                {
                    "title": ending.get_text(strip=True)
                } for ending in ending_theme
            ]
        return []

    def __str_to_int(self, string):
        return int("".join(filter(str.isdigit, [s for s in string])))
