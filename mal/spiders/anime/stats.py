from re import search
from mal.spiders.utils import get_soup


class Stats:
    def __init__(self, base_url, mal_id) -> None:
        self.base_url = base_url
        self.mal_id = mal_id
        self.soup = get_soup(f"{self.base_url}/anime/{self.mal_id}/_/stats")

    def get(self):
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

    def __find_string(self, string):
        summary_selector = self.soup.select_one("#content > table td:last-child > .js-scrollfix-bottom-rel")
        return int(
            summary_selector.find("span", class_="dark_text", string=string).next_sibling.replace(",", "")
        )

    def __percentage(self, string):
        if string:
            return float(string.previous_sibling.replace("%", "").strip())
        return None

    def __votes(self, string):
        if string:
            regex = search(r"\d+", string.get_text())
            if regex:
                return int(regex.group())
            return None
        return None

    def __scores(self):
        selector = self.soup.select_one(".js-scrollfix-bottom-rel > table")
        return {
            str(number): {
                "percentage": self.__percentage(
                    selector.select_one(
                        f"tr:nth-child({index}) > td:last-child small"
                    )),
                "votes": self.__votes(
                    selector.select_one(
                        f"tr:nth-child({index}) > td:last-child small"
                    )
                )
            } for index, number in enumerate(reversed(range(1, 11)), 1)
        }
