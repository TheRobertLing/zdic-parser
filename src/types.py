type CharacterInfo = dict[str, int | str | list[str] | None]
type Definitions = dict[str, dict[str, list[str]]]
type ParsedSections = dict[str, CharacterInfo | Definitions]