import pytest
import bs4

from test_utils import (
    fetch_character_html,
    fetch_character_info_section,
    fetch_definitions_section,
)
from test_data import (
    fetch_character_html_data,
    fetch_character_info_section_data,
    fetch_definitions_section_data_1,
    fetch_definitions_section_data_2,
)

from src.types import (
    CharacterInfo,
    Definitions,
    ParsedSections,
)
from src.parser import (
    parse_html,
    parse_character_info_section,
    parse_definitions_section,
)


class TestParser:
    @pytest.mark.parametrize("character", list(fetch_character_html_data))
    def test_parse_html(self, character: str):
        # Sanity check to just confirm that the utility function actually returned something valid
        html: str = fetch_character_html(character)
        assert "<html " in html, "fetch_character_html failed: No valid HTML returned"

        parsed: ParsedSections = parse_html(html)
        assert 'character_info' in parsed, f"Missing key character_info in {parsed}"
        assert 'definitions' in parsed, f"Missing key definitions in {parsed}"
        assert isinstance(parsed['character_info'], dict)
        assert isinstance(parsed['definitions'], dict)


    @pytest.mark.parametrize("character, expected_keys", fetch_character_info_section_data.items())
    def test_parse_character_info_section(self, character: str, expected_keys: dict[str, bool]):
        # Sanity check to just confirm that the utility function actually returned something valid
        html: str = fetch_character_html(character)
        assert "<html " in html, "fetch_character_html failed: No valid HTML returned"

        # If this ever fails, it most likely means zdic's structure changed
        section: bs4.element.Tag | None = fetch_character_info_section(html)
        assert section is not None, f"Zdic's structure must've changed if you see this"

        # Use for loop to confirm existence of key-value pairs
        parsed_data: CharacterInfo = parse_character_info_section(section)
        for key, value in expected_keys.items():
            assert (key in parsed_data) == value, f"Key '{key}' presence mismatch for character '{character}'"


    @pytest.mark.parametrize("character, expected_keys", fetch_definitions_section_data_1.items())
    def test_parse_definitions_section_1(self, character: str, expected_keys: dict[str, list[str]]):
        # Sanity check to just confirm that the utility function actually returned something valid
        html: str = fetch_character_html(character)
        assert "<html " in html, "fetch_character_html failed: No valid HTML returned"

        # If this ever fails, it most likely means zdic's structure changed
        section: bs4.element.Tag | None = fetch_definitions_section(html)
        assert section is not None, f"Zdic's structure must've changed if you see this"

        # Check that the simple_defs key exists
        parsed_data: Definitions = parse_definitions_section(section)
        assert "simple_defs" in parsed_data, f"The simple_defs key is not inside the dictionary"

        # Check all the definitions keys are the same
        parsed_simple_defs = parsed_data["simple_defs"]
        assert set(parsed_simple_defs.keys()) == set(expected_keys.keys()), f"The keys do not match"

        # Check all the items inside the simple_definitions
        for key, value in expected_keys.items():
            assert key in parsed_simple_defs, f"Missing key: {key}"
            assert set(parsed_simple_defs[key]) == set(value), f"The keys don't match"

    @pytest.mark.parametrize("character, expected_keys", fetch_definitions_section_data_2.items())
    def test_parse_definitions_section_2(self, character: str, expected_keys: dict[str, list[str]]):
        # Sanity check to just confirm that the utility function actually returned something valid
        html: str = fetch_character_html(character)
        assert "<html " in html, "fetch_character_html failed: No valid HTML returned"

        # If this ever fails, it most likely means zdic's structure changed
        section: bs4.element.Tag | None = fetch_definitions_section(html)
        assert section is not None, f"Zdic's structure must've changed if you see this"

        # Check that the simple_defs key exists
        parsed_data: Definitions = parse_definitions_section(section)
        assert "simple_defs" in parsed_data, f"The simple_defs key is not inside the dictionary"

        # Check the dictionary is empty
        parsed_simple_defs = parsed_data["simple_defs"]
        assert not parsed_simple_defs, f"The dictionary should be empty but wasn't"
