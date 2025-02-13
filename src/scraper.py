import httpx

from .parser import parse_html
from src.types.types import CharacterInfo, Definitions, ParsedSections


class ZDicCharacterParser:
    """
    A utility class for storing and retrieving data scraped from ZDic.

    Attributes:
        character_info (dict): A dictionary containing various details about a Chinese character.
            Note: Not all keys may be present in every entry.

            Possible keys:
            - img_src (str, optional): URL of the character's image.
            - pinyin (str, optional): Pinyin representation.
            - zhuyin (str, optional): Zhuyin (Bopomofo) notation.
            - radical (str, optional): Radical component.
            - non_radical_stroke_count (int, optional): Stroke count excluding the radical.
            - total_stroke_count (int, optional): Total stroke count.
            - simple_trad (str, optional): Simplified and traditional forms.
            - variant_characters (list, optional): Alternative character forms.
            - unicode (str, optional): Unicode representation.
            - character_structure (str, optional): Structural composition.
            - stroke_order (str, optional): Stroke order diagram or data.
            - wubi (str, optional): Wubi input method code.
            - cangjie (str, optional): Cangjie input method code.
            - zhengma (str, optional): Zhengma input method code.
            - fcorners (int, optional): Four-corner input method code.

        definitions (dict): A dictionary containing character definitions.
            - simple_defs (dict): Basic definitions of the character.

    Methods:
        Various getter methods for retrieving specific data fields, following the naming pattern:
            - get_<field_name>(), e.g., get_pinyin(), get_homophones(), get_simple_defs().
    """
    BASE_URL = "https://www.zdic.net/han{mode}/{character}"

    def __init__(self):
        self.character_info: CharacterInfo = {}
        self.definitions: Definitions = {}

    def search(self, character: str, mode: str = "s", timeout: int = 5) -> None:
        if mode.lower() not in ("s", "t"):
            raise ValueError("mode must be either 's' (Simplified Chinese) or 't' (Traditional Chinese).")

        full_url = self.BASE_URL.format(mode=mode.lower(), character=character)

        response = httpx.get(full_url, timeout=timeout)
        response.raise_for_status()

        parsed: ParsedSections = parse_html(response.text)
        self.character_info = parsed.get("character_info", {})
        self.definitions = parsed.get("definitions", {})

    async def search_async(self, character: str, mode: str = "s", timeout: int = 5) -> None:
        if mode not in ("s", "t"):
            raise ValueError("mode must be either 's' (Simplified Chinese) or 't' (Traditional Chinese).")

        full_url = self.BASE_URL.format(mode=mode, character=character)

        async with httpx.AsyncClient() as client:
            response = await client.get(full_url, timeout=timeout)
            response.raise_for_status()

        parsed: ParsedSections = parse_html(response.text)
        self.character_info = parsed.get("character_info", {})
        self.definitions = parsed.get("definitions", {})

    # STATIC METHODS
    @staticmethod
    async def fetch_img_src(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_img_src()

    @staticmethod
    async def fetch_pinyin(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_pinyin()

    @staticmethod
    async def fetch_zhuyin(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_zhuyin()

    @staticmethod
    async def fetch_radical(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_radical()

    @staticmethod
    async def fetch_non_radical_stroke_count(character: str, mode: str = "s", timeout: int = 5) -> int | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_non_radical_stroke_count()

    @staticmethod
    async def fetch_total_stroke_count(character: str, mode: str = "s", timeout: int = 5) -> int | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_total_stroke_count()

    @staticmethod
    async def fetch_simple_trad(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_simple_trad()

    @staticmethod
    async def fetch_variant_characters(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_variant_characters()

    @staticmethod
    async def fetch_unicode(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_unicode()

    @staticmethod
    async def fetch_character_structure(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_character_structure()

    @staticmethod
    async def fetch_stroke_order(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_stroke_order()

    @staticmethod
    async def fetch_wubi(character: str, mode: str = "s", timeout: int = 5) -> int | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_wubi()

    @staticmethod
    async def fetch_cangjie(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_cangjie()

    @staticmethod
    async def fetch_zhengma(character: str, mode: str = "s", timeout: int = 5) -> str | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_zhengma()

    @staticmethod
    async def fetch_fcorners(character: str, mode: str = "s", timeout: int = 5) -> int | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_fcorners()

    @staticmethod
    async def fetch_simple_defs(character: str, mode: str = "s", timeout: int = 5) -> dict[str, list[str]] | None:
        parser = ZDicCharacterParser()
        await parser.search_async(character, mode, timeout)
        return parser.get_simple_defs()

    # GETTERS
    def get_img_src(self) -> str | None:
        return self.character_info.get("img_src")

    def get_pinyin(self) -> str | None:
        return self.character_info.get("pinyin")

    def get_zhuyin(self) -> str | None:
        return self.character_info.get("zhuyin")

    def get_radical(self) -> str | None:
        return self.character_info.get("radical")

    def get_non_radical_stroke_count(self) -> int | None:
        non_radical_stroke_count = self.character_info.get("non_radical_stroke_count")
        return int(non_radical_stroke_count) if non_radical_stroke_count is not None else None

    def get_total_stroke_count(self) -> int | None:
        total_stroke_count = self.character_info.get("total_stroke_count")
        return int(total_stroke_count) if total_stroke_count is not None else None

    def get_simple_trad(self) -> str | None:
        return self.character_info.get("simple_trad")

    def get_variant_characters(self) -> str | None:
        return self.character_info.get("variant_characters")

    def get_unicode(self) -> str | None:
        return self.character_info.get("unicode")

    def get_character_structure(self) -> str | None:
        return self.character_info.get("character_structure")

    def get_stroke_order(self) -> int | None:
        stroke_order = self.character_info.get("stroke_order")
        return int(stroke_order) if stroke_order is not None else None

    def get_wubi(self) -> str | None:
        return self.character_info.get("wubi")

    def get_cangjie(self) -> str | None:
        return self.character_info.get("cangjie")

    def get_zhengma(self) -> str | None:
        return self.character_info.get("zhengma")

    def get_fcorners(self) -> int | None:
        fcorners = self.character_info.get("fcorners")
        return int(fcorners) if fcorners is not None else None

    def get_simple_defs(self) -> dict[str, list[str]]:
        return self.definitions.get("simple_defs")
