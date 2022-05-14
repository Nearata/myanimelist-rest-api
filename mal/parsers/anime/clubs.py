from re import match
from typing import Optional

from bs4 import BeautifulSoup

from ...const import MAL_URL


class Clubs:
    def __init__(self, soup: BeautifulSoup, base_url: str) -> None:
        self.soup = soup
        self.base_url = base_url

    def __call__(self) -> dict:
        data = []

        element = self.soup.find("h2", string="Related Clubs")
        if element and (siblings := element.find_next_siblings("div")):
            for i in siblings:
                data.append(
                    {
                        "name": anchor_element.get_text().strip()
                        if (anchor_element := i.find_next("a"))
                        else None,
                        "url": MAL_URL + anchor_element.get("href")
                        if anchor_element
                        else None,
                        "members": self.__get_members(member_element.get_text().strip())
                        if anchor_element
                        and (parent_element := anchor_element.parent)
                        and (member_element := parent_element.select_one(":last-child"))
                        else None,
                    }
                )

        return {"data": data}

    def __get_members(self, string: str) -> Optional[int]:
        regex = match(r"\d+", string)
        return int(regex.group()) if regex else None
