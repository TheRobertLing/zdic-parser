import logging

import bs4
from bs4 import BeautifulSoup

from .types import CharacterInfo, Definitions, ParsedSections
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
    "同音字": "homophones",
    "同部首": "same_radical",
    "同笔画": "same_stroke_count",
    "同筆畫": "same_stroke_count",
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

    # Collate data
    character_info: CharacterInfo = parse_character_info_section(character_info_section)
    definitions: Definitions = parse_definitions_section(definitions_section)

    return {
        "character_info": character_info,
        "definitions": definitions,
    }


def parse_character_info_section(info_card: bs4.element.Tag) -> CharacterInfo:
    if info_card is None:
        raise ElementIsMissingException()

    parsed_info: CharacterInfo = {}

    # Extract image source
    img_tag: bs4.element.Tag | None = info_card.select_one("td.ziif_d_l img")
    if img_tag and img_tag.get("src"):
        parsed_info["img_src"] = img_tag["src"]

    # Extract character data
    character_info_tables: list[bs4.element.Tag] = info_card.select("td:not(.ziif_d_l) table table")

    for table in character_info_tables:
        trs: list[bs4.element.Tag] = table.find_all("tr", recursive=False)
        if len(trs) != 2:
            continue

        title_tds: list[bs4.element.Tag] = trs[0].find_all("td", recursive=False)
        value_tds: list[bs4.element.Tag] = trs[1].find_all("td", recursive=False)

        if len(title_tds) != len(value_tds):
            continue

        for title_td, value_td in zip(title_tds, value_tds):
            title:str = title_td.get_text(strip=True)
            classes: list[str] = value_td.get("class", [])

            if "z_bs2" in classes or "z_jfz" in classes:
                # Handle cases where multiple title-value pairs exist inside <p> elements
                for p in value_td.find_all("p", recursive=False):
                    span: bs4.element.Tag = p.find("span")
                    span_title: str = span.get_text(strip=True) if span else ""
                    if span:
                        span.extract()

                    span_value: str = p.get_text(separator=", ", strip=True)

                    if span_title and span_value:
                        parsed_info[keys[span_title]] = span_value
            else:
                value: str = value_td.get_text(separator=", ", strip=True)

                if title and value:
                    parsed_info[keys[title]] = value

    return parsed_info


def parse_definitions_section(definitions_card: bs4.element.Tag) -> Definitions:
    if definitions_card is None:
        raise ElementIsMissingException()

    parsed_info: Definitions = {"simple_defs": {}}

    # Get simple definitions
    simple_defs: bs4.element.Tag | None = definitions_card.select_one("div.content.definitions.jnr")
    if simple_defs:
        # Extract Chinese definitions
        dicpy_list = simple_defs.select("p > span.dicpy")
        if dicpy_list:
            # Necessary filter for certain edge cases
            filtered_dicpy: list[bs4.element.Tag] = [span for span in dicpy_list if span.find("span", {"class": "ptr"})]

            for dicpy in filtered_dicpy:
                # Key is the pinyin/zhuyin pair for an entry
                key: str = dicpy.get_text(separator=", ", strip=True)
                key_parent: bs4.element.Tag | None = dicpy.find_parent("p")
                if key_parent:
                    def_list: bs4.element.Tag | None = key_parent.find_next_sibling("ol")
                    if def_list and (def_list.find_all("li") or def_list.find_all("p")):
                        # Case 1: Definitions use <ol> with <li> e.g. most properly formatted pages
                        li_defs = [li.text.strip() for li in def_list.find_all("li")]

                        # Case 2: Definitions use <ol> with <p> e.g. the entry for 佚
                        p_tag = def_list.find("p")
                        if p_tag:
                            li_defs.append(p_tag.text.strip("◎ \u3000"))

                        # Check key doesn't exist already, otherwise append definitions
                        if key not in parsed_info["simple_defs"]:
                            parsed_info["simple_defs"][key] = []

                        parsed_info["simple_defs"][key].extend(li_defs)
                    else:
                        # Case 3: <p> element is not nested inside <ol> or <ol> does not exist e.g. the entry for 杉
                        p_tag: bs4.element.Tag | None = key_parent.find_next_sibling("p")
                        if p_tag and not (p_tag.find("strong") and "其它字义" in p_tag.find("strong").text):
                            if key not in parsed_info["simple_defs"]:
                                parsed_info["simple_defs"][key] = []

                            parsed_info["simple_defs"][key].append(p_tag.text.strip("◎ \u3000"))

        # Extract non-Chinese definitions
        other_defs: bs4.element.Tag | None = simple_defs.find("div", {"class": "enbox"})
        if other_defs:
            for p in other_defs.find_all("p", recursive=False):
                span: bs4.element.Tag | None = p.find("span")
                span_title: str = span.get_text(strip=True) if span else ""

                if span:
                    span.extract()

                definition_text = p.get_text(separator=", ", strip=True)

                if span_title not in parsed_info["simple_defs"]:
                    parsed_info["simple_defs"][span_title] = []
                parsed_info["simple_defs"][span_title].append(definition_text)

    return parsed_info
