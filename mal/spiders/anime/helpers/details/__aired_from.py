from datetime import datetime


def aired_from_helper(soup):
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
