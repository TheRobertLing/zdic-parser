from bs4 import BeautifulSoup
import httpx
import re
import pandas as pd

URL = "https://zh.wikisource.org/wiki/%E9%80%9A%E7%94%A8%E8%A7%84%E8%8C%83%E6%B1%89%E5%AD%97%E8%A1%A8"
stroke_dict = {
    "一画": 1, "二画": 2, "三画": 3, "四画": 4, "五画": 5, "六画": 6, "七画": 7, "八画": 8, "九画": 9, "十画": 10,
    "十一画": 11, "十二画": 12, "十三画": 13, "十四画": 14, "十五画": 15, "十六画": 16, "十七画": 17, "十八画": 18, "十九画": 19,
    "二十画": 20, "二十一画": 21, "二十二画": 22, "二十三画": 23, "二十四画": 24, "二十五画": 25, "二十六画": 26, "二十七画": 27,
    "二十八画": 28, "二十九画": 29, "三十画": 30, "三十一画": 31, "三十二画": 32, "三十三画": 33, "三十四画": 34, "三十五画": 35,
    "三十六画": 36
}

# Get page HTML
page = httpx.get(URL)
soup = BeautifulSoup(page.content, "lxml")

# Find where the tables for the top 8105 characters ends
char_tables_end = (soup
                   .find("h2", {"id": "附件1._规范字与繁体字、异体字对照表"})
                   .find_parent("div", {"class": "mw-heading mw-heading2"}))

char_tables = char_tables_end.find_all_previous("table", {"class": "multicol"})
char_tables.reverse()

# Extract the characters
characters = []
for table in char_tables:
    for dd in table.find_all("dd"):
        # Remove superscript
        superscript = dd.find("sup")
        if superscript:
            superscript.decompose()

        # Extract data
        characters_stroke_count = [item.strip() for item in dd.get_text(separator=" ", strip=True).split(" ")]
        characters.append((int(characters_stroke_count[0]), characters_stroke_count[1]))

# Find traditional/variant tables
combined_trs = []
traditional_variants_tds = soup.find_all("td", {"width": "50%"})
for td in traditional_variants_tds:
    trs = td.find_all("tr")[1:]  # Ignore table titles
    combined_trs.extend(trs)

# Extract the characters
trad_variants_characters = []
row_span_count = 0
row_span_data = {}
for tr in combined_trs:
    # Remove superscript
    superscript = tr.find_all("sup")
    for sup in superscript:
        sup.decompose()

    tds = tr.find_all("td")
    if not row_span_count:  # If the row_span_count is 0, it means a new entry has been reached
        if row_span_data:
            trad_variants_characters.append((
                row_span_data["position"],
                row_span_data["simplified"],
                row_span_data["traditional"],
                row_span_data["variants"],
            ))
        row_span_data = {}

        # Get the rowcount if it exists
        row_span_count = int(tds[0].get("rowspan")) if tds[0].get("rowspan") is not None else 1

        # Case 1: start of a new rowspan and Case 2: start of a new one-liner
        position_str = tds[0].get_text(strip=True).strip()

        # Edge case: 1455 is split across 2 tables
        if position_str:
            position = int(position_str)
        else:
            # simply add to the last item in the list
            traditional = re.sub(r"^[()\s～]+", "", tds[2].get_text(strip=True)).strip()
            variant = re.sub(r"^[\[\]\s]+", "", tds[3].get_text(strip=True)).strip()

            if trad_variants_characters:
                last_entry = list(trad_variants_characters[-1])
                last_entry[2].extend(list(traditional))
                last_entry[3].extend(list(variant))
                trad_variants_characters[-1] = tuple(last_entry)

            row_span_count -= 1
            continue

        simplified = tds[1].get_text(strip=True).strip()
        traditional = tds[2].get_text(strip=True).strip("()～ ")
        variant = tds[3].get_text(strip=True).strip("[] ")

        row_span_data["position"] = position
        row_span_data["simplified"] = simplified
        row_span_data["traditional"] = list(traditional) if traditional else []
        row_span_data["variants"] = list(variant) if variant else []
    else:
        # Case 3: still in the middle of a rowspan

        # Check if the row_span spans across 2 tables in which case 4 tds are present, otherwise only 2 tds
        if len(tds) == 2:
            traditional = tds[0].get_text(strip=True).strip("()～ ")
            variant = tds[1].get_text(strip=True).strip("[] ")
        else:  # length should be 2
            traditional = tds[2].get_text(strip=True).strip("()～ ")
            variant = tds[3].get_text(strip=True).strip("[] ")

        # Separate characters into a list
        traditional_list = list(traditional) if traditional else []
        variants_list = list(variant) if variant else []

        # Extend the list inside row_span_data
        row_span_data["traditional"].extend(traditional_list)
        row_span_data["variants"].extend(variants_list)

    # Subtract the row_span_count at the end of iteration
    row_span_count -= 1

# Add final value as well
trad_variants_characters.append((
    row_span_data["position"],
    row_span_data["simplified"],
    row_span_data["traditional"],
    row_span_data["variants"],
))

# Find the stroke count tables
stroke_count_tables_start = (soup
                             .find("h2", {"id": "附件2._《通用规范汉字表》笔画检字表"})
                             .find_parent("div", {"class": "mw-heading mw-heading2"}))
stroke_count_tds = stroke_count_tables_start.find_all_next("td")
stroke_count = 0
characters_stroke_count = []
for td in stroke_count_tds:
    for tag in td.find_all(["p", "dl"], recursive=False):
        if tag.name == "p":
            # Get the stroke count
            if tag.find('b'):
                stroke_count = stroke_dict[tag.text.strip()]

        elif tag.name == "dl":
            # Get a list of all dds
            for dd in tag.find_all('dd'):
                # Add the character and stroke count
                characters_stroke_count.append((dd.get_text(strip=True).strip()[-1], stroke_count))

# characters
# trad_variants_characters
# characters_stroke_count

# Create pandas dataframe
df = pd.DataFrame(characters, columns =["Position", "Simplified"])
df2 = pd.DataFrame(trad_variants_characters, columns=["Position", "Simplified", "Traditional", "Variants"])
df3 = pd.DataFrame(characters_stroke_count, columns = ["Simplified", "Stroke Count"])

df_merged = (df.merge(df3[["Simplified", "Stroke Count"]], on=["Simplified"], how="left")
             .merge(df2[["Position", "Simplified", "Traditional", "Variants"]],
                    on=["Position", "Simplified"],
                    how="left"))
df_merged["Traditional"] = df_merged["Traditional"].fillna("[]")
df_merged["Variants"] = df_merged["Variants"].fillna("[]")

# Save to Excel file
df_merged.to_excel("Top8105CharactersData.xlsx", index=False)