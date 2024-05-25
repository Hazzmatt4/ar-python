import requests
import re
from bs4 import BeautifulSoup

url = 'https://wiki.archerage.to/na-en/db/items/31403'

# url = input("\033[2mCopy and paste the link of the item from ArcheRage Wiki:\033[34m ")

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print("\033[30mExtracting text...\033[0m")

# Item ID
span_item_id = soup.find('div', {'class': 'd-inline-block cl-grey'})
item_id = re.sub(r'\D', '', span_item_id.text.strip())
print("\033[30mItem ID found! - \033[2;32;40m" + item_id + "\033[30m -")

# Item Name
span_item_name = soup.find('div', {'class': 'col font-size-lg'})
item_name = span_item_name.text.strip()
print("\033[30mItem name found! - \033[2;32;40m" + item_name + "\033[30m -")

# Items Grade Number
span_item_grade = soup.find_all('img', class_='w40 grade-icon')
grade_search = [img['src'] for img in span_item_grade]
# print(grade_search)
grade_file = grade_search[0].replace("/static/images/icons/item_grade_", "")
# print(grade_file)
ar_grade = grade_file[:-8]
# print(ar_grade)
grade_num = re.sub("[^0-9]", "", ar_grade)
print("\033[30mGrade number found! - \033[2;32;40m" + str(grade_num) + "\033[30m -")

# Item Grade Name
conv_grades = {
    0: "Crude", 
    1: "Basic", 
    2: 'Grand', 
    3: 'Rare', 
    4: 'Arcane', 
    5: "Heroic", 
    6: "Unique", 
    7: 'Celestial', 
    8: 'Divine', 
    9: 'Epic', 
    10: 'Legendary', 
    11: 'Mythic', 
    12: 'Eternal'
    } 
grade_int = int(grade_num)
grade_name = conv_grades.get(grade_int,grade_num)
print("\033[30mGrade Name found! - \033[2;32;40m" + str(grade_name) + "\033[30m -")

# Item Groups and Sub-Groups
span_item_groups = soup.find('div', {'class': 'col font-size-md cl-l-orange'})
item_full_group = span_item_groups.text.strip()
item_group, item_subgroup = item_full_group.split(" > ")
print("\033[30mItem Group found! - \033[2;32;40m" + item_group + "\033[30m -")
print("\033[30mItem Sub-Group found! - \033[2;32;40m" + item_subgroup + "\033[30m -")