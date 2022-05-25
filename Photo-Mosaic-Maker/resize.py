from PIL import Image
from os import listdir
import os
from os.path import isfile, join

original_path = "Images"
edited_path = "temp"

def create_folders():
    if not os.path.exists(original_path):
        os.mkdir(original_path) 
    if not os.path.exists(edited_path):
        os.mkdir(edited_path) 

def empty_edited_folder():
    for f in os.listdir(edited_path):
        os.remove(os.path.join(edited_path, f))

# Get all the images in the path (only allow specific extensions)
# and shrink them
def resize_photos(size, allowed_extensions):
    file_names = [f for f in listdir(original_path) if isfile(join(original_path, f))]
    file_names = [f for f in file_names if os.path.splitext(f)[1] in allowed_extensions]
    for file_name in file_names:
        image = Image.open(original_path + "/" + file_name)
        image = image.resize(size)
        image.save(edited_path + "/" + file_name)
