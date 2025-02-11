import httpx

from bs4 import BeautifulSoup

from .parser import parse_html
from .types import CharacterInfo, Definitions, ParsedSections


class ZDicCharacterParser:
    """
    ZDic Chinese Character Data Parser

    Fields:
    - character_info = {
        img_src: str | None,
        pinyin: str | None, e.g. "he4, he3"
        zhuyin: list[str],
        radical: str | None,
        non_radical_stroke_count: int | None,
        total_stroke_count: int | None,
        simple_trad: str,
        variant_characters: list[str],
        unicode: str | None,
        character_structure: str | None,
        stroke_order: str | None,
        wubi: str | None,
        cangjie: str | None,
        zhengma: str | None,
        sijiao: str | None,
    }
    - definitions = {
        simple_def = list[dict[str, list[str]]],
    }

    Methods:
        'get_' + dictionary key
        e.g. get_pinyin, get_homophones, get_simple_def

    """
    BASE_URL = "https://www.zdic.net/han{mode}/{character}"

    def __init__(self):
        self.character_info: CharacterInfo = {}
        self.definitions: Definitions = {}

    def search(self, character: str, mode: str = "s", timeout: int = 5) -> None:
        if mode not in ("s", "t"):
            raise ValueError("mode must be either 's' (Simplified Chinese) or 't' (Traditional Chinese).")

        full_url = self.BASE_URL.format(mode=mode, character=character)

        response = httpx.get(full_url, timeout=timeout)
        response.raise_for_status()

        parsed: ParsedSections = parse_html(response.text)
        self.character_info = parsed.get("character_info", {})
        self.definitions = parsed.get("definitions", {})

    """ 
    Actions:
    """

    def get_img_src(self) -> str | None:
        pass

    def get_pinyin(self) -> list[str] | None:
        pass

    def get_zhuyin(self) -> list[str] | None:
        pass

    def get_radical(self):
        pass

    def get_stroke_info(self):
        pass

    def get_variants(self):
        pass

    def get_unicode(self):
        pass

    def get_structure(self):
        pass

    def get_stroke_order(self):
        """ Returns a string of numbers that represents the strokes, compared to simply the count """
        pass

    def get_wubi(self):
        pass

    def get_cangjie(self):
        pass

    def get_zhengma(self):
        pass

    def get_fcorners(self):
        pass

    """ Work on these ones later """

    def get_definition_simple(self):
        pass

    def get_definition_detailed(self):
        pass
