import pytest

from test_data import (
    ZdicScraper_search_data,
    ZdicScraper_get_img_src_data,
    ZdicScraper_get_pinyin_data,
    ZdicScraper_get_zhuyin_data,
    ZdicScraper_get_radical_data,
    ZdicScraper_get_non_radical_stroke_count,
    ZdicScraper_get_total_stroke_count,
    ZdicScraper_get_simple_trad_data,
    ZdicScraper_variant_characters_data,
    ZdicScraper_get_unicode_data,
    ZdicScraper_get_character_structure_data,
    ZdicScraper_get_stroke_order_data,
    ZdicScraper_get_wubi_data,
    ZdicScraper_get_cangjie_data,
    ZdicScraper_get_zhengma_data,
    ZdicScraper_get_fcorners_data,
    ZdicScraper_get_simple_defs_data,
)
from zdic_parser.type_definitions.types import (
    CharacterInfo,
    Definitions,
    ParsedSections,
)
from zdic_parser.parser import (
    ZDicCharacterParser,
)

class TestZdicScraper:
    def test_init(self):
        """ Check if the scraper can be initialized correctly """
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        assert scraper.character_info == {}
        assert scraper.definitions == {}

    @pytest.mark.parametrize("letters", list("abcdefhijklmnopqruvwxyz"))
    def test_search_exception(self, letters: str):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        with pytest.raises(ValueError,
                           match="mode must be either 's' \(Simplified Chinese\) or 't' \(Traditional Chinese\)\."):
            scraper.search("你", mode=letters)

    @pytest.mark.parametrize("letters", list("sStT"))
    def test_search_no_exception(self, letters: str):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search("你", mode=letters)

    @pytest.mark.parametrize("character, expected_keys", ZdicScraper_search_data.items())
    def test_search_characters(self, character: str, expected_keys: dict[str, bool]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")
        print(scraper.character_info)

        for key, value in expected_keys.items():
            assert (key in scraper.character_info) == value, f"Key '{key}' presence mismatch for character '{character}'"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_img_src_data.items())
    def test_get_img_src(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        # Check the image sources are the same
        if scraper.get_img_src():
            assert set(expected) == set(scraper.get_img_src().split(", ")), "Image sources are different"
        else:
            assert expected == scraper.get_img_src(), "Image sources are different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_pinyin_data.items())
    def test_get_pinyin(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        # Check the pinyin are the same
        if scraper.get_pinyin():
            assert set(expected) == set(scraper.get_pinyin().split(", ")), "Pinyin are different"
        else:
            assert expected == scraper.get_pinyin(), "Pinyin are different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_zhuyin_data.items())
    def test_get_zhuyin(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_zhuyin():
            assert set(expected) == set(scraper.get_zhuyin().split(", ")), "Zhuyin data is different"
        else:
            assert expected == scraper.get_zhuyin(), "Zhuyin data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_radical_data.items())
    def test_get_radical(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_radical():
            assert set(expected) == set(scraper.get_radical().split(", ")), "Radical data is different"
        else:
            assert expected == scraper.get_radical(), "Radical data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_non_radical_stroke_count.items())
    def test_get_non_radical_stroke_count(self, character: str, expected: list[int]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_non_radical_stroke_count():
            assert set(expected) == {scraper.get_non_radical_stroke_count()}, "Non-radical stroke count is different"
        else:
            assert expected == scraper.get_non_radical_stroke_count(), "Non-radical stroke count is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_total_stroke_count.items())
    def test_get_total_stroke_count(self, character: str, expected: list[int]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_total_stroke_count():
            assert set(expected) == {scraper.get_total_stroke_count()}, "Total stroke count is different"
        else:
            assert expected == scraper.get_total_stroke_count(), "Total stroke count is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_simple_trad_data.items())
    def test_get_simple_trad(self, character: str, expected: list[str]):
        scraper = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_simple_trad():
            assert set(expected) == set(
                scraper.get_simple_trad().split(", ")), "Simplified-Traditional data is different"
        else:
            assert expected == scraper.get_simple_trad(), "Simplified-Traditional data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_variant_characters_data.items())
    def test_get_variant_characters(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_variant_characters():
            assert set(expected) == set(scraper.get_variant_characters().split(", ")), "Variants data is different"
        else:
            assert expected == scraper.get_variant_characters(), "Variants data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_unicode_data.items())
    def test_get_unicode(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_unicode():
            assert set(expected) == set(scraper.get_unicode().split(", ")), "Unicode data is different"
        else:
            assert expected == scraper.get_unicode(), "Unicode data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_character_structure_data.items())
    def test_get_character_structure(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_character_structure():
            assert set(expected) == set(scraper.get_character_structure().split(", ")), "Structure data is different"
        else:
            assert expected == scraper.get_character_structure(), "Structure data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_stroke_order_data.items())
    def test_get_stroke_order(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_stroke_order():
            assert set(expected) == {scraper.get_stroke_order()}, "Stroke order data is different"
        else:
            assert expected == scraper.get_stroke_order(), "Stroke order data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_wubi_data.items())
    def test_get_wubi(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_wubi():
            assert set(expected) == set(scraper.get_wubi().split(", ")), "Wubi data is different"
        else:
            assert expected == scraper.get_wubi(), "Wubi data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_cangjie_data.items())
    def test_get_cangjie(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_cangjie():
            assert set(expected) == set(scraper.get_cangjie().split(", ")), "Cangjie data is different"
        else:
            assert expected == scraper.get_cangjie(), "Cangjie data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_zhengma_data.items())
    def test_get_zhengma(self, character: str, expected: list[str]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_zhengma():
            assert set(expected) == set(scraper.get_zhengma().split(", ")), "Zhengma data is different"
        else:
            assert expected == scraper.get_zhengma(), "Zhengma data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_fcorners_data.items())
    def test_get_fcorners(self, character: str, expected: list[int]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        if scraper.get_fcorners():
            assert set(expected) == {scraper.get_fcorners()}, "Fcorners data is different"
        else:
            assert expected == scraper.get_fcorners(), "Fcorners data is different"

    @pytest.mark.parametrize("character, expected", ZdicScraper_get_simple_defs_data.items())
    def test_get_simple_defs(self, character: str, expected: dict[str, list[str]]):
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        scraper.search(character, mode="s")

        definitions = scraper.get_simple_defs()
        assert set(definitions.keys()) == set(expected.keys()), f"The keys do not match"

        # Check all the items inside the simple_definitions
        for key, value in expected.items():
            assert key in definitions, f"Missing key: {key}"
            assert set(definitions[key]) == set(value), f"The keys don't match"