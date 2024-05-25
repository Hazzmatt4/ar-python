import time
import os
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

# Max number of icon_item_5492
i = 0

print("\033[1;31;40m--- Item with grade ripper looping script ---\033[0m")

while True:
    num = str(i).zfill(1)
    #Skills illusion, fight, adamant, will, death, wild, magic, vocation, romance, love, hatred, assassin, madness, pleasure, buff
    skill_class = ''
    icon_img_url = 'https://archeagecodex.com/images/icon_quest_cat' + skill_class + num + '.png'

    print("Next Url: \033[34m" + icon_img_url + " \033[0m")
    time.sleep(.5)
    print("\033[1;31;40m--- Downloading item icon ---\033[0m")

    # --- Download the first image ---
    response1 = requests.get(icon_img_url)  # URL
    icon_img = Image.open(BytesIO(response1.content))

    # --- Create a new folder for the output file ---
    output_folder = os.path.join(os.getcwd(), 'Ripper_Loop_Output-icons') # /// OUTPUT FOLDER
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # --- Construct the output filename based on the input filenames ---
    output_filename = str("icon_quest_cat"+ skill_class + num + ".png") # /// FILE NAME

    # --- Save the combined image in the output folder ---
    output_path = os.path.join(output_folder, output_filename)
    icon_img.save(output_path)

    # --- Print output image name ---
    print("\033[30mImage saved as: \033[1;32;40m" + output_filename + "\033[30m in \033[1;33;40m" + output_folder)
    print("\033[1;31;40m--- Completed! ---\033[0m")

    ###

    i += 1
    time.sleep(.5)
