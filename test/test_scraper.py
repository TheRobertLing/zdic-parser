from src.scraper import ZDicCharacterParser


class TestZdicScraper:
    def test_init(self):
        """ Check if the scraper can be initialized correctly """
        scraper: ZDicCharacterParser = ZDicCharacterParser()
        assert scraper.character_info == {}
        assert scraper.definitions == {}
        assert scraper.related_character == {}

    def test_search(self):
        """ Integration test for searching and parsing HTML """