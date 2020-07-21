from datetime import datetime


def aired_to_helper(soup):
    aired_to = soup.find("span", string="Aired:").next_sibling
    if not str(aired_to).strip() == "Not available" and aired_to.split("to")[1].strip() != "?":
        try:
            aired_to_date = datetime.strptime(
                aired_to.split("to")[1].strip(),
                "%b %d, %Y"
            ).date()
        except ValueError:
            aired_to_date = datetime.strptime(
                aired_to.split("to")[1].strip(),
                "%b, %Y"
            ).date()
        return str(aired_to_date)
    return None
