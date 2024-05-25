import time
import os
import requests
import re
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

print("\033[1;30;40m-< >- ArcheRage Full Item Ripper -< >-\033[0m")


while True:
    print("\033[1;31;40m--- Requesting item icon ---\033[0m")

    # Request the items url from archeage codex
    item_url = input("\033[2mCopy and paste the link of the item from ArcheRage wiki:\033[34m ")

    print("\033[1;31;40m--- Searching for item image, and name ---\033[0m")

    # extracting the image from the copied link
    response = requests.get(item_url)

    soup = BeautifulSoup(response.text, "html.parser")

    img_elements = soup.find_all("img", {"class": "w40"}) # looking for an img element with the alt attribute that equals icon
    for img_element in img_elements:
        if "icon_item_" in img_element.get("src", ""): # checking if the found element has icon_item_ as part of the src
            img_src = img_element["src"]
            print("\033[30mFound item image at \033[1;36mhttps://wiki.archerage.to" + img_src + "\033[0m")
            break
    else:
        print("\033[2;35mNo usable item image was found at this link\033[0m") # No img element with alt='icon' and src containing 'icon_item_' found.
        continue

    # Item Name
    span_element = soup.find('div', {'class': 'col font-size-lg'})
    item_name = span_element.text.strip()
    print("\033[30mItem name found! - \033[2;32;40m" + item_name + "\033[30m -")

    # Finding Item Grade from web URL
    print("\033[1;31;40m--- Locating item grade ---\033[0m")

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
    # print("\033[30mGrade Name found! - \033[2;32;40m" + str(grade_name) + "\033[30m -")
        

    # creating the archeage codex url for the grade of the item
    grades = {"Crude": "0poor", "Basic": "1common", 'Grand': "2uncommmon", 'Rare': "3rare", 'Arcane': "4ancient", 'Heroic': "5heroic", 'Unique': "6unique", 'Celestial': "7artifact", 'Divine': "8wonder", 'Epic': 9, 'Legendary': "10legendary", 'Mythic': "11mythic", 'Eternal': "12arche"}
    
    Grade = grade_name.capitalize()
    if Grade in grades:
        grade_overlay = grades[Grade]
        url_grade = 'https://wiki.archerage.to/static/images/icons/item_grade_' + str(grade_overlay) + '.dds.png'
        print("\033[30mThe items grade is \033[32m" + Grade + "\033[30m!\033[0m")
    else:
        print("\033[2;35mProblem Matching Grade.\033[0m")
        continue

    print("\033[1;31;40m--- Downloading item and grade and creating new image. ---\033[0m")

    # Download the first image
    response1 = requests.get('https://wiki.archerage.to' + img_src)
    img1 = Image.open(BytesIO(response1.content))

    # Download the second image
    response2 = requests.get(url_grade)
    img2 = Image.open(BytesIO(response2.content))

    # Resize the second image to cover the same area as the first image
    img2 = img2.resize(img1.size)

    # Combine the images by pasting img2 onto img1
    img1.paste(img2, (0, 0), img2)

    # Create a new folder for the output file
    output_folder = os.path.join(os.getcwd(), 'ItemCreatorOutput')
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    print("\033[1;31;40m--- Creating unique file name and saving image to folder. ---\033[0m")

    # Construct the output filename based on the input filenames
    span_element = soup.find('div', {'class': 'd-inline-block cl-grey'})
    item_id = re.sub(r'\D', '', span_element.text.strip())

    output_filename = item_id + "-" + Grade + "_" + item_name + ".png"

    # Save the combined image in the output folder
    output_path = os.path.join(output_folder, output_filename)
    img1.save(output_path)

    # Print output image name
    print("\033[30mImage saved as: \033[1;32;40m" + output_filename + "\033[30m in \033[1;33;40m" + output_folder)
    print("\033[1;31;40m--- Completed! ---\033[0m")

    time.sleep(.5)

    print("\033[30mRestarting script...\033[0m")
    continue