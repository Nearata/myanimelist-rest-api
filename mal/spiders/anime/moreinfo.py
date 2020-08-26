from bs4 import BeautifulSoup


class MoreInfo:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def get(self) -> dict:
        tags_decompose = self.soup.select(
            """
            .js-scrollfix-bottom-rel > div,
            .js-scrollfix-bottom-rel > a,
            .js-scrollfix-bottom-rel > h2
            """
        )

        for i in tags_decompose:
            i.decompose()

        return {
            "more_info": self.soup.select_one(".js-scrollfix-bottom-rel").get_text().strip()
        }
