from re import match
from mal.spiders.utils import get_soup


def get_clubs(mal_id):
    soup = get_soup(f"https://myanimelist.net/anime/{mal_id}/_/clubs")
    selector = soup.select(".js-scrollfix-bottom-rel > .borderClass")

    def members(string):
        regex = match(r"\d+", string)
        if regex:
            return int(regex.group())
        return None

    clubs = [
        {
            "name": i.select_one("a").text.strip(),
            "url": f"https://myanimelist.net{i.select_one('a').get('href')}",
            "members": members(i.select_one("small").text)

        } for i in selector
    ]

    return {
        "clubs": clubs
    }
