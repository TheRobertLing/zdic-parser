import bs4
import pandas as pd
import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://www.zdic.net/han{mode}/{character}"
DATA_FILE = "data.xlsx"
df = pd.read_excel(DATA_FILE, sheet_name="Sheet1")


def fetch_character_html(character: str, mode: str = "s", timeout: int = 5) -> str:
    """
    Basically the scraper.search() method, but without the field assignment for testing purposes.
    """
    if mode not in ("s", "t"):
        raise ValueError("mode must be either 's' (Simplified Chinese) or 't' (Traditional Chinese).")

    full_url = BASE_URL.format(mode=mode, character=character)
    response = httpx.get(full_url, timeout=timeout)
    response.raise_for_status()
    return response.text


def fetch_character_info_section(html: str) -> bs4.element.Tag | None:
    soup = BeautifulSoup(html, "lxml")
    return soup.select_one(
        "body main div.zdict div.res_c_center "  # Locate position in general layout
        "div.entry_title table"  # Select the character information table
    )


def fetch_definitions_section(html: str) -> bs4.element.Tag | None:
    soup = BeautifulSoup(html, "lxml")
    return soup.select_one(
        "body main div.zdict div.res_c_center "  # Locate position in general layout
        "div.homograph-entry div.dictionaries.zdict"  # Select dictionary entries container
    )

def get_random_data(number: int = 50, seed: int = 1, mode: str = "Simplified") -> list[str]:
    """ Fetches sample data from data.xlsx for test """
    return [character.strip() for character in df[mode].dropna().sample(n=number, random_state=seed).tolist()]
