# try:
#     if definitions_card is None:
#         raise ElementIsMissingException()
#
#     # Get simple definitions
#     parsed_info["simple_defs"] = {}
#     simple_defs: bs4.element.Tag | None = definitions_card.select_one("div.content.definitions.jnr")
#     if simple_defs is not None:
#         # Get all chinese definitions
#         dicpy_list = simple_defs.select("p > span.dicpy")
#         if dicpy_list:
#             # Necessary filter for certain edge cases
#             filtered_dicpy: list[bs4.element.Tag] = [span for span in dicpy_list if
#                                                      span.find("span", {"class": "ptr"})]
#
#             for dicpy in filtered_dicpy:
#                 # Get pinyin/zhuyin for definition entry
#                 key: str = dicpy.get_text(separator=", ", strip=True)
#
#                 # Get corresponding definitions
#                 key_parent: bs4.element.Tag | None = dicpy.find_parent("p")
#                 if key_parent:
#                     def_list = key_parent.find_next_sibling("ol")
#                     if def_list:
#                         # Case 1: Definitions use <ol> with <li> e.g. most properly formatted pages
#                         parsed_info["simple_defs"][key] = [li.text.strip() for li in def_list.find_all('li')]
#
#                         # Case 2: Definitions use <ol> with <p> e.g. the entry for 佚
#                         p_tag = def_list.find("p")
#                         if p_tag:
#                             parsed_info["simple_defs"][key] = [p_tag.text.strip("◎ \u3000")]
#                     else:
#                         # Case 3: Definitions use <p> instead of <ol> e.g. the entry for 杉
#                         p_tag = key_parent.find_next_sibling("p")
#
#                         # Ensure the title is not accidentally fetched
#                         if p_tag and not (p_tag.find("strong") and "其它字义" in p_tag.find("strong").text):
#                             parsed_info["simple_defs"][key] = [p_tag.text.strip("◎ \u3000")]
#
#         # Get non chinese definitions if there are any
#         other_defs = simple_defs.find("div", {"class": "enbox"})
#         if other_defs:
#             for p in other_defs.find_all("p", recursive=False):
#                 span: bs4.element.Tag | None = p.find("span")
#                 span_title: str
#                 if span:
#                     span_title = span.get_text(strip=True)
#                     span.extract()
#                 else:
#                     span_title = ""
#
#                 parsed_info["simple_defs"][span_title] = [p.get_text(separator=", ", strip=True)]
#
#     # Get other definitions potentially in future
#
#     return parsed_info
# except ElementIsMissingException as e:
#     logging.error(e)
#     return {}