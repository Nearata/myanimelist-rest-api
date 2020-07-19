from mal.spiders.utils import get_soup


class MoreInfo:
    def __init__(self, base_url, mal_id) -> None:
        self.base_url = base_url
        self.mal_id = mal_id

    def get(self):
        soup = get_soup(f"{self.base_url}/anime/{self.mal_id}/_/moreinfo")
        tags_decompose = soup.select(
            """
            .js-scrollfix-bottom-rel > div,
            .js-scrollfix-bottom-rel > a,
            .js-scrollfix-bottom-rel > h2
            """
        )

        for i in tags_decompose:
            i.decompose()

        return {
            "more_info": soup.select_one(".js-scrollfix-bottom-rel").get_text(strip=True)
        }
