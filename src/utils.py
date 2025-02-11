from bs4 import BeautifulSoup
import bs4
import logging
from .types import CharacterInfo, Definitions, RelatedCharacters
from .exceptions import ElementIsMissingException


def get_sections(soup: BeautifulSoup) -> dict[str, bs4.element.Tag | None]:
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


def parse_soup(soup: BeautifulSoup) -> dict[str, CharacterInfo | Definitions | RelatedCharacters]:
    # Parse all sections
    character_info_section: bs4.element.Tag | None = soup.select_one(
        "body main div.zdict div.res_c_center "  # Locate position in general layout
        "div.entry_title table"  # Select the character information table
    )
    definitions_section: bs4.element.Tag | None = soup.select_one(
        "body main div.zdict div.res_c_center "  # Locate position in general layout
        "div.homograph-entry div.dictionaries.zdict"  # Select dictionary entries container
    )
    related_characters_section: bs4.element.Tag | None = soup.select_one(
        "body main div.zdict div.res_c_right"  # Locate position in general layout
    )

    # Collate data
    character_info: CharacterInfo = parse_character_info_section(character_info_section)
    definitions: Definitions = parse_definitions_section(definitions_section)
    related_character: RelatedCharacters = parse_related_characters_section(related_characters_section)

    return {
        'character_info': character_info,
        'definitions': definitions,
        'related_character': related_character,
    }


def parse_character_info_section(info_card: bs4.element.Tag | None) -> CharacterInfo:
    parsed_info: CharacterInfo = {}

    try:
        if info_card is None:
            raise ElementIsMissingException()

        # Extract image source
        img_tag = info_card.select_one("td.ziif_d_l img")
        if img_tag and img_tag.get("src"):
            parsed_info["img_src"] = img_tag["src"]

        # Extract character data
        character_info_tables = info_card.select("td:not(.ziif_d_l) table table")

        for table in character_info_tables:
            trs = table.find_all("tr", recursive=False)
            if len(trs) != 2:
                continue

            title_tds: list[bs4.element.Tag] = trs[0].find_all("td", recursive=False)
            value_tds: list[bs4.element.Tag] = trs[1].find_all("td", recursive=False)
            if len(title_tds) != len(value_tds):
                continue

            for title_td, value_td in zip(title_tds, value_tds):
                title: str = title_td.get_text(strip=True)
                classes: list[str] = value_td.get("class", [])
                value: str = ""

                if "z_bs2" in classes or "z_jfz" in classes:
                    # Special case: multiple title-value pairs inside <p> elements
                    for p in value_td.find_all("p", recursive=False):
                        span: bs4.element.Tag | None = p.find("span")
                        if span:
                            span_title = span.get_text(strip=True)
                            span.extract()
                        else:
                            span_title = ""

                        span_value = p.get_text(separator=", ", strip=True)

                        if span_title and span_value:
                            parsed_info[span_title] = span_value
                else:
                    value = value_td.get_text(separator=", ", strip=True)

                    if title and value:
                        parsed_info[title] = value

        return parsed_info

    except ElementIsMissingException as e:
        logging.error(e)
        return {}


def parse_definitions_section(definitions_card: bs4.element.Tag) -> dict[str, list[dict[str, list[str]]]]:
    pass


def parse_related_characters_section(side_card: bs4.element.Tag) -> dict[str, list[str]]:
    pass
