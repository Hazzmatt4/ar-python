import time
import os
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

i = 48973

print("\033[1;31;40m--- Item with grade ripper looping script ---\033[0m")

while True:
    num = str(i).zfill(4)
    new_url = 'https://archeagecodex.com/us/item/' + num + '/'

    print("Next Url: \033[34m" + new_url + " \033[0m")

    ###
    # Code from the 'Archeage Item Icon Ripper.py'
    item_url = new_url

    print("\033[1;31;40m--- Searching for item image, and name ---\033[0m")

    # extracting the image from the copied link  # URL
    response = requests.get(item_url)

    soup = BeautifulSoup(response.text, "html.parser")  # URL

    img_elements = soup.find_all("img", {"alt": "icon"}) # looking for an img element with the alt attribute that equals icon
    for img_element in img_elements:
        if "icon_item_" in img_element.get("src", ""): # checking if the found element has icon_item_ as part of the src
            url_item = img_element["src"]
            print("\033[30mFound item image at \033[1;36mhttps:" + url_item + "\033[0m")
            break
    else:
        print("\033[2;35mNo usable item image was found at this at \033[1;36m" + new_url + "\033[0m") # No img element with alt='icon' and src containing 'icon_item_' found.
        i += 1
        time.sleep(.5)
        continue

    # Find item name from item_url
    span_element = soup.find('span', {'id': 'item_name'})  # URL

    item_name = span_element.text.strip()

    print("\033[30mItem name found! - \033[2;32;40m" + item_name + "\033[30m -")

    def replace_chars(text):
        return text.replace(':', '').replace(';', '').replace('+', 'plus').replace('/', '').replace('<', '').replace('>', '').replace('*', '').replace('\"', '').replace('?', 'question mark').replace('\\', '')

    print("\033[1;31;40m--- Searching for item grade ---\033[0m")

    img_elements2 = soup.find_all("img", {"alt": "icon"}) # looking for an img element with the alt attribute that equals icon   # URL
    for img_element2 in img_elements2:
        if "icon_grade" in img_element2.get("src", ""): # checking if the found element has icon_grade as part of the src
            url_grade = img_element2["src"]
            print("\033[30mFound grade image at \033[1;36mhttps:" + url_grade + "\033[0m")
            break
    else:
        print("\033[2;35mNo usable grade image was found at this \033[1;36m" + new_url + "\033[0m") # No img element with alt='icon' and src containing 'icon_item_' found.
        i += 1
        time.sleep(0)
        continue

    # Download the first image
    response1 = requests.get('https:' + url_item)  # URL
    img1 = Image.open(BytesIO(response1.content))

    # Download the second image
    response2 = requests.get('https:' + url_grade)  # URL
    img2 = Image.open(BytesIO(response2.content))

    print("\033[1;31;40m--- Downloading item and grade and creating new image. ---\033[0m")

    # Resize the second image to cover the same area as the first image
    img2 = img2.resize(img1.size)

    # Combine the images by pasting img2 onto img1
    img1.paste(img2, (0, 0), img2)

    # Create a new folder for the output file
    output_folder = os.path.join(os.getcwd(), 'Ripper_Loop_Output')
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # Construct the output filename based on the input filenames
    output_filename = str(num + "_" + replace_chars(item_name) + ".png")

    # Save the combined image in the output folder
    output_path = os.path.join(output_folder, output_filename)
    img1.save(output_path)

    # Print output image name
    print("\033[30mImage saved as: \033[1;32;40m" + output_filename + "\033[30m in \033[1;33;40m" + output_folder)
    print("\033[1;31;40m--- Completed! ---\033[0m")

    ###

    i += 1
    time.sleep(.5)
