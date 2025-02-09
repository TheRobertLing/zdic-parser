from bs4 import BeautifulSoup
import bs4


def get_sections(soup: BeautifulSoup) -> dict[str, bs4.element.Tag | None]:
    """
    Utility for getting the sections where the important information is stored.
    May break if the website structure changes. Hopefully it doesn't change.
    """

    info_card: bs4.element.Tag | None = soup.select_one(
        "body main div.zdict div.res_c_center "
        "div.shiyi_content.res_c_center_content div.entry_title table"
    )

    definitions_card: bs4.element.Tag | None = soup.select_one(
        "body main div.zdict div.res_c_center "
        "div.shiyi_content.res_c_center_content div.homograph-entry "
        "div.dictionaries.zdict"
    )

    side_card: bs4.element.Tag | None = soup.select_one("body main div.zdict div.res_c_right")

    return {
        'info_card': info_card,
        'definitions_card': definitions_card,
        'side_card': side_card
    }
