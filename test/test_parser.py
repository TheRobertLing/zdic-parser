import pytest
from src.scraper import ZDicParser
import bs4
from collections import Counter

test_characters = "蔡徐坤鸡你太美𫮃𬺓𬙋耰𩾌𬙊𬶋𬶍𬭚𬭛陎𫵷鱲䲘鱣纕鸊鸏乾幹個豐餜餛闍淼溼擣𢷬蹵躕樐㯭艣艪"
test_pinyin = [
    ("篮", ["lán"]),
    ("籃", ["lán"]),
    ("球", ["qiú"]),
    ("鸡", ["jī"]),
    ("鷄", ["jī"]),
    ("鄀", ["ruò"]),
    ("眍", ["kōu"]),
    ("瞘", ["kōu"]),
    ("毗", ["pí"]),
    ("彳", ["chì"]),
    ("癿", ["qié"]),
]
test_pinyin_dyz = [
    ("种", ["zhǒng", "zhòng", "chóng"]),
    # ("種", ["zhǒng", "zhòng", "chóng"]), zdic error probably
    ("叕", ["zhuì", "zhuó", "yǐ", "jué"]),
    ("华", ["huá", "huà", "huā"]),
    ("亹", ["wěi", "mén"]),
    ("柁", ["tuó", "duò"]),
    ("戧", ["qiāng", "qiàng"]),
    ("僥", ["jiǎo", "yáo"]),
    ("攢", ["zǎn", "cuán"]),
    ("㥮", ["zhòu", "chăo"]),
    ("㤘", ["zhòu", "chăo"]),
    ("和", ["hé", "hè", "huó", "huò", "hú"]),
]
test_pinyin_invalid = "𬣙𪨰𫭢𫘪𣗋𬙂䎖"




@pytest.mark.parametrize("character", list(test_characters))
def test_character_sections(character):
    """ Test if each character successfully returns a valid section """
    parser: ZDicParser | None = ZDicParser.search(character)
    assert parser is not None, f"Failed to fetch data for character {character}"
    assert parser.sections is not None, f"Sections doesn't even exist"

    info_card: bs4.element.Tag | None = parser.sections['info_card']
    assert info_card is not None, f"info_card is None for {character}"

    definitions_card: bs4.element.Tag | None = parser.sections['definitions_card']
    assert definitions_card is not None, f"definitions_card is None for {character}"

    side_card: bs4.element.Tag | None = parser.sections['side_card']
    assert side_card is not None, f"side_card is None for {character}"


@pytest.mark.parametrize("character", list(test_characters))
def test_get_img_src(character):
    """ Test if an image is successfully returned for each character """
    parser: ZDicParser = ZDicParser.search(character)

    img_src: str | None = parser.get_img_src()
    assert img_src is not None, f"Could not find the svg for {character}"


@pytest.mark.parametrize("character, expected", test_pinyin)
def test_get_pinyin(character, expected):
    parser: ZDicParser = ZDicParser.search(character)

    pinyin_list: list[str] | None = parser.get_pinyin()
    assert pinyin_list is not None, f"There was no pinyin found for {character}"
    assert Counter(pinyin_list) == Counter(expected), f"{character} should only have one pronunciation"


@pytest.mark.parametrize("character, expected", test_pinyin_dyz)
def test_get_pinyin_dyz(character, expected):
    parser: ZDicParser = ZDicParser.search(character)

    pinyin_list: list[str] | None = parser.get_pinyin()
    assert pinyin_list is not None, f"There was no pinyin found for {character}"
    assert Counter(pinyin_list) == Counter(expected), (f"{character} should have more than one pronunciation, but only "
                                                       f"got {pinyin_list}")


@pytest.mark.parametrize("character", test_pinyin_invalid)
def test_get_pinyin_invalid(character):
    parser: ZDicParser = ZDicParser.search(character)

    pinyin_list: list[str] | None = parser.get_pinyin()
    assert pinyin_list is None, f"There was no pinyin found for {character}"

