from mal.spiders.utils import get_soup


def get_moreinfo(mal_id):
    soup = get_soup(f"https://myanimelist.net/anime/{mal_id}/_/moreinfo")

    tags_decompose = soup.select(
        """
        .js-scrollfix-bottom-rel > div,
        .js-scrollfix-bottom-rel > a,
        .js-scrollfix-bottom-rel > h2
        """
    )

    for i in tags_decompose:
        i.decompose()

    moreinfo = soup.select_one(".js-scrollfix-bottom-rel")

    return {
        "more_info": moreinfo.get_text(strip=True)
    }
