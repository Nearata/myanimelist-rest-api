from datetime import datetime
from mal.spiders.utils import get_soup


def get_details(mal_id):
    soup = get_soup(f"https://myanimelist.net/anime/{mal_id}")

    def str_to_int(soup):
        return int("".join(filter(str.isdigit, [s for s in soup])))

    def trailer():
        trailer = soup.select_one(".video-promotion > .promotion")
        if trailer:
            return trailer.get("href")
        return None

    def synopsis():
        synopsis = soup.select_one("span[itemprop=description]")
        if synopsis:
            return synopsis.text.strip()
        return None

    def background():
        background = soup.select_one("span[itemprop=description]").parent
        for i in background.select("h2, span, div"):
            i.decompose()

        if not background.text.lower().startswith("no background"):
            return background.text
        return None

    def english():
        english = soup.find("span", string="English:")
        if english:
            return english.next_sibling.strip()
        return None

    def japanese():
        japanese = soup.find("span", string="Japanese:")
        if japanese:
            return japanese.next_sibling.strip()
        return None

    def synonyms():
        synonyms = soup.find("span", string="Synonyms:")
        if synonyms:
            return [
                i.strip()
                for i in synonyms.next_sibling.split(",")
            ]
        return []

    def episodes():
        episdes = soup.find("span", string="Episodes:").next_sibling
        if episdes.strip() != "Unknown":
            return int(episdes)
        return None

    def status():
        return soup.find("span", string="Status:").next_sibling.strip()

    def aired_from():
        aired_from = soup.find("span", string="Aired:").next_sibling
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

    def aired_to():
        aired_to = soup.find("span", string="Aired:").next_sibling
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

    def premiered():
        premiered = soup.find("span", string="Premiered:")
        if premiered.next_sibling.strip() != "?":
            return premiered.parent.find("a").text
        return None

    def producers():
        producers = soup.find("span", string="Producers:")
        if "none found" not in producers.next_sibling.strip().lower():
            return [
                {
                    "name": i.text,
                    "url": f"https://myanimelist.net{i.get('href')}",
                    "mal_id": str_to_int(i.get("href").split("/"))
                } for i in producers.find_next_siblings("a")
            ]
        return []

    def licensors():
        if "none found" not in soup.find(
                "span", string="Licensors:").next_sibling.strip().lower():
            return [
                {
                    "name": i.text,
                    "url": f"https://myanimelist.net{i.get('href')}",
                    "mal_id": str_to_int(i.get("href").split("/"))
                } for i in soup.find(
                    "span", string="Licensors:").find_next_siblings("a")
            ]
        return []

    def studios():
        studios = soup.find("span", string="Studios:")
        if "none found" not in studios.next_sibling.strip().lower():
            return [
                {
                    "name": i.text,
                    "url": f"https://myanimelist.net{i.get('href')}",
                    "mal_id": str_to_int(i.get("href").split("/"))
                } for i in studios.find_next_siblings("a")
            ]
        return []

    def source():
        source = soup.find("span", string="Source:")
        if source:
            return source.next_sibling.strip()
        return None

    def genres():
        genres = soup.find("span", string="Genres:")
        if genres:
            return [
                {
                    "name": i.text,
                    "mal_id": str_to_int(i.get("href").split("/"))
                } for i in genres.find_next_siblings("a")
            ]
        return []

    def duration():
        duration = soup.find("span", string="Duration:").next_sibling.strip()
        if duration != "Unknown":
            return str_to_int(duration)
        return None

    def rating():
        rating = soup.find("span", string="Rating:").next_sibling.strip()
        if rating.lower() != "none":
            return rating
        return None

    def score():
        score = soup.find("span", itemprop="ratingValue")
        if score:
            return float(score.text)
        return None

    def ranked():
        try:
            return int(soup.find(
                "span",
                string="Ranked:").next_sibling.replace("#", "").strip())
        except ValueError:
            return None
        return None

    def popularity():
        try:
            return int(soup.find(
                "span",
                string="Popularity:").next_sibling.replace("#", "").strip())
        except ValueError:
            return None
        return None

    def members():
        try:
            return int(soup.find(
                "span",
                string="Members:").next_sibling.replace(",", "").strip())
        except ValueError:
            return None
        return None

    def favorites():
        try:
            return int(soup.find(
                "span",
                string="Favorites:").next_sibling.replace(",", "").strip())
        except ValueError:
            return None
        return None

    def adaptation():
        adaptation = soup.find("td", string="Adaptation:")
        if adaptation:
            return [
                {
                    "title": i.text,
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in adaptation.next_sibling.select("a")
            ]
        return []

    def side_story():
        side_story = soup.find("td", string="Side story:")
        if side_story:
            return [
                {
                    "title": i.text,
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in side_story.next_sibling.select("a")
            ]
        return []

    def summary():
        summary = soup.find("td", string="Summary:")
        if summary:
            return [
                {
                    "title": i.text,
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in summary.next_sibling.select("a")
            ]
        return []

    def spin_off():
        spin_off = soup.find("td", string="Spin-off:")
        if spin_off:
            return [
                {
                    "title": i.text,
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in spin_off.next_sibling.select("a")
            ]
        return []

    def other():
        other = soup.find("td", string="Other:")
        if other:
            return [
                {
                    "title": i.text,
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in other.next_sibling.select("a")
            ]
        return []

    def prequel():
        prequel = soup.find("td", string="Prequel:")
        if prequel:
            return [
                {
                    "title": i.text,
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in prequel.next_sibling.select("a")
            ]
        return []

    def character():
        character = soup.find("td", string="Character:")
        if character:
            return [
                {
                    "title": i.text,
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in character.next_sibling.select("a")
            ]
        return []

    def sequel():
        sequel = soup.find("td", string="Sequel:")
        if sequel:
            return [
                {
                    "title": i.text,
                    "type": i.get("href").split("/")[1],
                    "mal_id": int(i.get("href").split("/")[2])
                } for i in sequel.next_sibling.select("a")
            ]
        return []

    def opening_theme():
        opening_theme = soup.select("div.opnening > span.theme-song")
        if opening_theme:
            return [
                {
                    "title": opening.text.strip()
                } for opening in opening_theme
            ]
        return []

    def ending_theme():
        ending_theme = soup.select("div.ending > span.theme-song")
        if ending_theme:
            return [
                {
                    "title": ending.text.strip()
                } for ending in ending_theme
            ]
        return []

    details = {
        "title": soup.select_one("h1").text,
        "image": soup.select_one("img.ac").get("src"),
        "trailer": trailer(),
        "synopsis": synopsis(),
        "background": background(),
        "alternative_titles": {
            "english": english(),
            "japanese": japanese(),
            "synonyms": synonyms(),
        },
        "information": {
            "type": soup.find(
                "span", string="Type:").find_next_sibling("a").text,
            "episodes": episodes(),
            "status": status(),
            "aired": {
                "from": aired_from(),
                "to": aired_to()
            },
            "premiered": premiered(),
            "producers": producers(),
            "licensors": licensors(),
            "studios": studios(),
            "source": source(),
            "genres": genres(),
            "duration": duration(),
            "rating": rating()
        },
        "statistics": {
            "score": score(),
            "ranked": ranked(),
            "popularity": popularity(),
            "members": members(),
            "favorites": favorites()
        },
        "related_anime": {
            "adaptation": adaptation(),
            "side_story": side_story(),
            "summary": summary(),
            "spin_off": spin_off(),
            "other": other(),
            "prequel": prequel(),
            "character": character(),
            "sequel": sequel()
        },
        "opening_theme": opening_theme(),
        "ending_theme": ending_theme()
    }

    return {
        "details": details
    }
