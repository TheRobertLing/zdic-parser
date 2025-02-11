import pytest
from src.scraper import ZDicCharacterParser
import bs4
from test_utils import (
    fetch_character_html,
    fetch_character_info_section,
    fetch_definitions_section,
    fetch_related_characters_section,
)
from test_data import (
    fetch_character_html_data,
    fetch_character_info_section_data,
)
from src.types import (
    CharacterInfo,
    Definitions,
    RelatedCharacters,
    ParsedSections
)
from src.parser import (
    parse_html,
    parse_character_info_section,
    parse_definitions_section,
    parse_related_characters_section
)


test_characters = "蔡徐坤鸡你太美𫮃𬺓𬙋耰𩾌𬙊𬶋𬶍𬭚𬭛陎𫵷鱲䲘鱣纕鸊鸏乾幹個豐餜餛闍淼溼擣𢷬蹵躕樐㯭艣艪"


@pytest.mark.parametrize("character", list(fetch_character_html_data))
def test_parse_html(character: str):
    html: str = fetch_character_html(character)

    # Sanity check to just confirm that the utility function actually returned something valid
    assert "<html " in html, "fetch_character_html failed: No valid HTML returned"

    parsed: ParsedSections = parse_html(html)
    assert 'character_info' in parsed, f"Missing key character_info in {parsed}"
    assert 'definitions' in parsed, f"Missing key definitions in {parsed}"
    assert 'related_character' in parsed, f"Missing key related_character in {parsed}"
    assert isinstance(parsed['character_info'], dict)
    assert isinstance(parsed['definitions'], dict)
    assert isinstance(parsed['related_character'], dict)


@pytest.mark.parametrize("character, expected_keys", fetch_character_info_section_data.items())
def test_character_info_section(character: str, expected_keys: dict[str, bool]):
    html: str = fetch_character_html(character)

    # Sanity check to just confirm that the utility function actually returned something valid
    assert "<html " in html, "fetch_character_html failed: No valid HTML returned"

    section: bs4.element.Tag | None = fetch_character_info_section(html)

    # If this ever fails, it most likely means zdic's structure changed
    assert section is not None, f"Zdic's structure must've changed if you see this"

    parsed_data: CharacterInfo = parse_character_info_section(section)

    # Use for loop to confirm existence of key-value pairs
    for key, value in expected_keys.items():
        assert (key in parsed_data) == value, f"Key '{key}' presence mismatch for character '{character}'"


@pytest.mark.parametrize("character", list(test_characters))
def test_parse_definitions_section(character):
    html: str = fetch_character_html(character)

    # Sanity check to just confirm that the utility function actually returned something valid
    assert "<html " in html, "fetch_character_html failed: No valid HTML returned"

    section: bs4.element.Tag | None = fetch_definitions_section(html)

    # If this ever fails, it most likely means zdic's structure changed
    assert section is not None, f"Zdic's structure must've changed if you see this"


@pytest.mark.parametrize("character", list(test_characters))
def test_related_characters_section(character):
    html: str = fetch_character_html(character)

    # Sanity check to just confirm that the utility function actually returned something valid
    assert "<html " in html, "fetch_character_html failed: No valid HTML returned"

    section: bs4.element.Tag | None = fetch_related_characters_section(html)

    # If this ever fails, it most likely means zdic's structure changed
    assert section is not None, f"Zdic's structure must've changed if you see this"

