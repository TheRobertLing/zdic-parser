import bs4.element
from bs4 import BeautifulSoup


def get_sections(soup: BeautifulSoup) -> dict[str, bs4.element.Tag]:
    """
    Utility for getting the sections where the important information is stored.
    May break if the website structure changes. Hopefully it doesn't change.
    """

    # Table where non definition details are contained
    info_card: bs4.element.Tag = soup.select_one("body main div.zdict div.res_c_center "
                                                 "div.shiyi_content.res_c_center_content div.entry_title table")

    # Area where definitions are contained
    definitions_card: bs4.element.Tag = soup.select_one("body main div.zdict div.res_c_center "
                                                        "div.shiyi_content.res_c_center_content div.homograph-entry "
                                                        "div.dictionaries.zdict")

    # Area where homophones, same radical characters and same stroke count characters are stored
    side_card: bs4.element.Tag = soup.select_one("body main div.zdict div.res_c_right")

    return {
        'info_card': info_card,
        'definitions_card': definitions_card,
        'side_card': side_card
    }
