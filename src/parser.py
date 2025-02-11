from bs4 import BeautifulSoup
import bs4
import logging
from .types import CharacterInfo, Definitions, RelatedCharacters, ParsedSections
from .exceptions import ElementIsMissingException

# Key map
keys: dict[str, str] = {
    "拼音": "pinyin",
    "注音": "zhuyin",
    "部首": "radical",
    "部外": "non_radical_stroke_count",
    "总笔画": "total_stroke_count",
    "總筆畫": "total_stroke_count",
    "繁体": "simple_trad",
    "繁體": "simple_trad",
    "简体": "simple_trad",
    "簡體": "simple_trad",
    "异体字": "variant_characters",
    "異體字": "variant_characters",
    "统一码": "unicode",
    "統一碼": "unicode",
    "字形分析": "character_structure",
    "笔顺": "stroke_order",
    "筆順": "stroke_order",
    "五笔": "wubi",
    "五筆": "wubi",
    "仓颉": "cangjie",
    "倉頡": "cangjie",
    "郑码": "zhengma",
    "鄭碼": "zhengma",
    "四角": "sijiao",
}


def parse_html(html: str) -> ParsedSections:
    # Create soup
    soup = BeautifulSoup(html, "lxml")

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
        "character_info": character_info,
        "definitions": definitions,
        "related_character": related_character,
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
                            parsed_info[keys[span_title]] = span_value
                else:
                    value = value_td.get_text(separator=", ", strip=True)

                    if title and value:
                        parsed_info[keys[title]] = value

        return parsed_info

    except ElementIsMissingException as e:
        logging.error(e)
        return {}


def parse_definitions_section(definitions_card: bs4.element.Tag) -> dict[str, list[dict[str, list[str]]]]:
    return {}


def parse_related_characters_section(side_card: bs4.element.Tag) -> dict[str, list[str]]:
    return {}
