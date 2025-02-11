type CharacterInfo = dict[str, int | str | list[str] | None]
type Definitions = dict[str, list[dict[str, list[str]]]]
type RelatedCharacters = dict[str, list[str]]
type ParsedSections = dict[str, CharacterInfo | Definitions | RelatedCharacters]