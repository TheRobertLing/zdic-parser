from bs4 import BeautifulSoup

html = '''<td class="z_bs2 z_ytz2">
            <a href="/hans/為" target="_blank">為</a>
            <a href="/hans/𦥮" target="_blank"><span class="ytz_txt">𦥮</span></a>
          </td>'''

soup = BeautifulSoup(html, 'html.parser')
value_td = soup.find("td")  # Find the <td> element

# Check if class "z_ytz2" exists
if "z_ytz2" in value_td.get("class", []):
    print("Class 'z_ytz2' exists in this <td>!")

# Alternative way
if value_td.has_attr("class") and "z_ytz2" in value_td["class"]:
    print("Confirmed: 'z_ytz2' is present!")
