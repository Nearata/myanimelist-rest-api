from datetime import datetime
from re import findall
from re import match
from re import sub
from mal.spiders.utils import get_soup


def get_episodes(mal_id, page_number):
    if page_number == 1:
        page_url = f"https://myanimelist.net/anime/{mal_id}/_/episode"
    else:
        page_url = f"https://myanimelist.net/anime/{mal_id}/_/episode?offset={page_number}00"

    soup = get_soup(page_url)
    selector = soup.select("table.ascend .episode-list-data")

    def title_romanji(string):
        regex = sub(r"\s\(.*?\)", "", string)
        if regex:
            return regex
        return None

    def title_jap(string):
        pattern = r"[^a-zA-Z!-@#$%^&*(),.?\":{}|<>\s].*[^)]"
        regex = findall(pattern, string)
        if regex:
            return "".join(regex)
        return None

    def number(string):
        regex = match(r"\d+", string)
        if regex:
            return int(regex.group())
        return None

    def aired(string):
        regex = match(
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s?(\d{1,2})?(,)\s(\d{4})",
            string
        )
        if regex:
            return str(datetime.strptime(regex.group(), "%b %d, %Y").date())
        return None

    def filler_recap(string):
        regex = match(r"(filler|recap)", string.lower())
        if regex:
            return True
        return False

    episodes = [
        {
            "title": i.select_one(".episode-title > a").get_text(),
            "title_romanji": title_romanji(
                i.select_one(".episode-title > span").get_text()
            ),
            "title_japanese": title_jap(
                i.select_one("td.episode-title > span").get_text()
            ),
            "number": number(i.select_one("td.episode-number").get_text()),
            "aired": aired(i.select_one("td.episode-aired").get_text()),
            "filler": filler_recap(
                i.select_one(".episode-title > span").get_text()
            ),
            "recap": filler_recap(
                i.select_one(".episode-title > span").get_text()
            )
        } for i in selector
    ]

    return {
        "episodes": episodes
    }
