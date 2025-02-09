import bs4
import httpx
from .utils import get_sections
from bs4 import BeautifulSoup


class ZDicParser:
    """
    ZDic Chinese Character Data Parser
    """
    BASE_URL = "https://www.zdic.net/han{mode}/{character}"

    def __init__(self, html: str):
        self.sections: dict[str, bs4.element.Tag | None] = get_sections(BeautifulSoup(html, "lxml"))

    @classmethod
    def search(cls, character: str, mode: str = "s", timeout: int = 5):
        """ Static constructor for synchronous requests """
        if mode not in ("s", "t"):
            raise ValueError("mode must be either 's' (Simplified Chinese) or 't' (Traditional Chinese).")

        full_url = cls.BASE_URL.format(mode=mode, character=character)

        try:
            response = httpx.get(full_url, timeout=timeout)
            response.raise_for_status()
            return cls(response.text)
        except httpx.TimeoutException:
            print("HTTP request timed out.")
        except httpx.ConnectError:
            print("Connection error. Please check your internet connection.")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"An error occurred while making the request: {str(e)}")

        return None

    """ 
    Actions:
    """

    def get_img_src(self) -> str | None:
        # Check if the section for the image exists
        if not self.sections['info_card']:
            return None

        td: bs4.element.Tag | None = self.sections['info_card'].find("td", {"class": "ziif_d_l"})
        if not td:
            return None

        # Check if the image exists
        img: bs4.element.Tag | None = td.find('img')
        if not img or not img.has_attr("src"):
            return None

        return img["src"]

    def get_pinyin(self) -> list[str] | None:
        # Check if the section for pinyin exists
        if not self.sections['info_card']:
            return None

        table: bs4.element.Tag | None = self.sections['info_card'].find("table", {"border": "0"})
        if not table:
            return None

        # Check if the pinyin exists
        tds: list[bs4.element.Tag] = table.find_all("td", {"class": "z_py"})
        if len(tds) == 2:
            td = tds[1]
        else:
            return None

        # Get all pinyin paragraphs
        ps: list[bs4.element.Tag] = td.find_all('p')
        if not ps:
            return None

        return [p.text.strip() for p in ps]

    def get_zhuyin(self) -> list[str] | None:
        # Check if the section for zhuyin exists
        if not self.sections['info_card']:
            return None

        table: bs4.element.Tag | None = self.sections['info_card'].find("table", {"border": "0"})
        if not table:
            return None

        # Check if the pinyin exists
        tds: list[bs4.element.Tag] = table.find_all("td", {"class": "z_py"})
        if len(tds) == 2:
            td = tds[1]
        else:
            return None

        # Get all pinyin paragraphs
        ps: list[bs4.element.Tag] = td.find_all('p')
        if not ps:
            return None

        return [p.text.strip() for p in ps]

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

    def get_homophones(self):
        pass

    def get_same_radicals(self):
        pass

    def get_same_stroke_count(self):
        pass

    """ Work on these ones later """

    def get_definition_simple(self):
        pass

    def get_definition_detailed(self):
        pass
