import time
import os
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
import re

i = 3409

print("\033[1;31;40m--- ArcheRage Item Information Collection Loop ---\033[0m")

while True:

    num = str(i).zfill(4) # num for column E (5) ----------
    next_url = 'https://wiki.archerage.to/na-en/db/items/' + num + '/'

    print("Next Url: \033[34m" + next_url + " \033[0m")
    time.sleep(.5)

    # ===== Modified Code from the 'AAIconRipper-Loop.py' =====
    item_url = next_url # item_url for column F (6) ----------

    print("\033[1;31;40m--- Searching for item image, and name ---\033[0m")

    # extracting the image from the copied link  # URL
    response = requests.get(item_url)

    soup = BeautifulSoup(response.text, "html.parser")  # URL

    img_elements = soup.find_all("img", {"alt": "icon"}) # looking for an img element with the alt attribute that equals icon
    for img_element in img_elements:
        if "icon_item_" in img_element.get("src", ""): # checking if the found element has icon_item_ as part of the src
            url_icon = img_element["src"] # url_icon for column G (7) ----------
            print("\033[30mFound item image at \033[1;36mhttps:" + url_icon + "\033[0m")
            break
    else:
        print("\033[2;35mNo usable item image was found at this at \033[1;36m" + next_url + "\033[0m") # No img element with alt='icon' and src containing 'icon_item_' found.
        i += 1
        time.sleep(.5)
        continue

    # Find item name from item_url
    span_element = soup.find('span', {'id': 'item_name'})  # URL
    item_name = span_element.text.strip() # item_name for column A (1) ----------
    print("\033[30mItem name found! - \033[2;32;40m" + item_name + "\033[30m -")

    def replace_chars(text):
        return text.replace(':', '').replace(';', '').replace('+', 'plus').replace('/', '').replace('<', '').replace('>', '').replace('*', '').replace('\"', '').replace('?', 'question mark').replace('\\', '')

    print("\033[1;31;40m--- Searching for item grade ---\033[0m")

    img_elements2 = soup.find_all("img", {"alt": "icon"}) # looking for an img element with the alt attribute that equals icon   # URL
    for img_element2 in img_elements2:
        if "icon_grade" in img_element2.get("src", ""): # checking if the found element has icon_grade as part of the src
            url_grade = img_element2["src"] # url_grade for column I (9) ----------
            print("\033[30mFound grade image at \033[1;36mhttps:" + url_grade + "\033[0m")
            break
    else:
        print("\033[2;35mNo usable grade image was found at this \033[1;36m" + next_url + "\033[0m") # No img element with alt='icon' and src containing 'icon_item_' found.
        i += 1
        time.sleep(.5)
        continue

    # Creating numerical and text representations of the grades from url_grade
    grades = {"Crude": 0, "Basic": 1, 'Grand': 2, 'Rare': 3, 'Arcane': 4, 'Heroic': 5, 'Unique': 6, 'Celestial': 7, 'Divine': 8, 'Epic': 9, 'Legendary': 10, 'Mythic': 11, 'Eternal': 12}
    rev_grades = {0: "Crude", 1: "Basic", 2: 'Grand', 3: 'Rare', 4: 'Arcane', 5: "Heroic", 6: "Unique", 7: 'Celestial', 8: 'Divine', 9: 'Epic', 10: 'Legendary', 11: 'Mythic', 12: 'Eternal'} 

    grade_number = re.findall(r'\d+', url_grade) # grade_number for column I (12) ----------
    grade_name = rev_grades[float(grade_number[0])] # grade_name[0] for column K (11) -----------
    print("\033[30mGrade name found! - \033[2;32;40m" + grade_name + "\033[30m -")

    # Download the first image
    response1 = requests.get('https:' + url_icon)  # URL
    img1 = Image.open(BytesIO(response1.content))

    # Download the second image
    response2 = requests.get('https:' + url_grade)  # URL
    img2 = Image.open(BytesIO(response2.content))
    print("\033[1;31;40m--- Downloading item and grade and creating new image ---\033[0m")

    # Resize the second image to cover the same area as the first image
    img2 = img2.resize(img1.size)

    #
    # Combine the images by pasting img2 onto img1
    img1.paste(img2, (0, 0), img2) 
    # img1 is the full icon but im not sure how to pass this from python to the spreadsheet
    #

    # Construct the output filename based on the input filenames
    file_name = str(num + "_" + replace_chars(item_name) + ".png") # file_name for column C (3)
    print("\033[30mFile Name: \033[34m" + file_name + "\033[0m")

    # funtion to extract text from all <td> from the webpage, the second <td> always contains the GroupGradeName of the item
    def extract_td_text(item_url):
        # Send a GET request to the webpage
        response = requests.get(item_url)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <td> elements on the page
        td_elements = soup.find_all('td')

        # Extract the text from each <td> element
        td_text = [td.get_text(strip=True) for td in td_elements]

        return td_text
    
    # finding item_group by splitting apart the second <td> text extract
    print("\033[1;31;40m--- Extracting item group from text on page ---\033[0m")
    td_text = extract_td_text(item_url)

    item_group = td_text[1].split(grade_name)[0]

    print("\033[30mItem Group found! - \033[2;32;40m" + item_group + "\033[30m -")
    
    # Print complete set of created values
    print("\033[1;31;40m--- Completed! ---\033[0m")
    time.sleep(.5)
    print("\033[30mIn Game Name: \033[34m" + item_name + "\033[0m")
    print("\033[30mItem Group: \033[34m" + item_group + "\033[0m")
    print("\033[30mFile Name: \033[34m" + file_name + "\033[0m")
    print("\033[30mFull Icon: \033[1;31;40m"+ "Curently held in img1" + "\033[0m") #how do i get the spreadsheet to add this? currently held in img1
    print("\033[30mItem ID: \033[34m" + num + "\033[0m")
    print("\033[30mCodex URL: \033[34m" + item_url + "\033[0m")
    print("\033[30mCodex Icon URL: \033[34mhttps:" + url_icon + "\033[0m")
    print("\033[30mIcon IMG: \033[33m Spreadsheet Formula\033[0m")
    print("\033[30mCodex Grade URL: \033[34mhttps:" + url_grade + "\033[0m")
    print("\033[30mGrade Overlay IMG: \033[33m Spreadsheet Formula\033[0m")
    print("\033[30mGrade Name: \033[34m" + grade_name + "\033[0m")
    print("\033[30mGrade Number: \033[34m" + str(grade_number[0]) + "\033[0m")

    i += 1
    time.sleep(10)

