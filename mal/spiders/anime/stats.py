from re import search
from mal.spiders.utils import get_soup


def get_stats(mal_id):
    soup = get_soup(f"https://myanimelist.net/anime/{mal_id}/_/stats")

    def findString(text):
        summarySelector = soup.select_one(
            "#content > table td:last-child > .js-scrollfix-bottom-rel")
        return int(
            summarySelector.find(
                "span", class_="dark_text", string=text
            ).next_sibling.replace(",", "")
        )

    summary = {
        "watching": findString("Watching:"),
        "completed": findString("Completed:"),
        "on_hold": findString("On-Hold:"),
        "dropped": findString("Dropped:"),
        "plan_to_watch": findString("Plan to Watch:"),
        "total": findString("Total:")
    }

    def percentage(string):
        if string:
            return float(string.previous_sibling.replace("%", "").strip())
        return None

    def votes(string):
        if string:
            regex = search(r"\d+", string.text)
            if regex:
                return int(regex.group())
            return None
        return None

    def scores():
        selector = soup.select_one(".js-scrollfix-bottom-rel > table")
        return {
            str(number): {
                "percentage": percentage(
                    selector.select_one(
                        f"tr:nth-child({index}) > td:last-child small"
                    )),
                "votes": votes(
                    selector.select_one(
                        f"tr:nth-child({index}) > td:last-child small"
                    )
                )
            } for index, number in enumerate(reversed(range(1, 11)), 1)
        }

    return {
        "summary": summary,
        "scores": scores()
    }
