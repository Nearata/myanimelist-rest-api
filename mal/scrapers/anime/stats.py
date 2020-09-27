from re import search

from bs4 import BeautifulSoup


class Stats:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def __call__(self) -> dict:
        return {
            "summary": {
                "watching": self.__find_string("Watching:"),
                "completed": self.__find_string("Completed:"),
                "on_hold": self.__find_string("On-Hold:"),
                "dropped": self.__find_string("Dropped:"),
                "plan_to_watch": self.__find_string("Plan to Watch:"),
                "total": self.__find_string("Total:")
            },
            "scores": self.__scores()
        }

    def __find_string(self, string: str) -> int:
        summary_selector = self.soup.select_one("#content > table td:last-child > .js-scrollfix-bottom-rel")
        return int(
            summary_selector.find("span", class_="dark_text", string=string).next_sibling.replace(",", "")
        )

    def __percentage(self, string: BeautifulSoup) -> float:
        return float(string.previous_sibling.replace("%", "").strip()) if string else None

    def __votes(self, string: BeautifulSoup) -> int:
        if string:
            regex = search(r"\d+", string.get_text())
            return int(regex.group()) if regex else None
        return None

    def __scores(self) -> dict:
        selector = self.soup.select_one(".js-scrollfix-bottom-rel > table")
        return {
            str(number): {
                "percentage": self.__percentage(
                    selector.select_one(
                        f"tr:nth-child({index}) > td:last-child small"
                    )
                ),
                "votes": self.__votes(
                    selector.select_one(
                        f"tr:nth-child({index}) > td:last-child small"
                    )
                )
            } for index, number in enumerate(reversed(range(1, 11)), 1)
        }
