import pytest
from src.scraper import ZDicParser

test_characters = "蔡徐坤鸡你太美𫮃𬺓𬙋耰𩾌𬙊𬶋𬶍𬭚𬭛陎𫵷鱲䲘鱣纕鸊鸏乾幹個豐餜餛闍淼溼擣𢷬蹵躕樐㯭艣艪"


@pytest.mark.parametrize("character", list(test_characters))
def test_character_sections(character):
    """ Test if each character successfully returns a valid section """
    parser = ZDicParser.search(character)

    assert parser is not None, f"Failed to fetch data for character {character}"
    assert parser.sections is not None, f"Sections doesn't even exist"

    info_card = parser.sections['info_card']
    definitions_card = parser.sections['definitions_card']
    side_card = parser.sections['side_card']

    assert info_card is not None, f"info_card is None for {character}"
    assert definitions_card is not None, f"definitions_card is None for {character}"
    assert side_card is not None, f"side_card is None for {character}"
