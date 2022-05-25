from math import sqrt
from random import randint
from PIL import Image, ImageEnhance, ImageOps, ImageChops
from os import listdir
import os
import operator
from os.path import isfile, join
import sys

if __name__ == "__main__":
    edited_path = "temp"
    original_path = None
    allowed_extensions = [".png", ".jpg", ".jpeg"]
    available_modes = ["blend", "original"]
    input_file = None
    output_file = "out.jpg"
    mode = "blend"
    cell_x = None
    cell_y = None
    grid_x = None
    grid_y = None
    blend_amount = 0.8
    resolution_scale = None

    arg_num = len(sys.argv)
    for i in range(1, arg_num, 2):
        if (i == arg_num - 1):
            print(f"Wrong {sys.argv[i]} argument input")
            exit(1)

        if (sys.argv[i] == "--output"):
            output_file = sys.argv[i + 1]
        elif (sys.argv[i] == "--input"):
            input_file = sys.argv[i + 1]
        elif (sys.argv[i] == "--cell_x"):
            cell_x = int(sys.argv[i + 1])
        elif (sys.argv[i] == "--cell_y"):
            cell_y = int(sys.argv[i + 1])
        elif (sys.argv[i] == "--grid_x"):
            grid_x = int(sys.argv[i + 1])
        elif (sys.argv[i] == "--grid_y"):
            grid_y = int(sys.argv[i + 1])
        elif (sys.argv[i] == "--blend_amount"):
            blend_amount = float(sys.argv[i + 1])
        elif (sys.argv[i] == "--resolution_scale"):
            resolution_scale = float(sys.argv[i + 1])
        elif (sys.argv[i] == "--mode"):
            mode = sys.argv[i + 1]
        elif (sys.argv[i] == "--input_cells_path"):
            original_path = sys.argv[i + 1]
        else:
            print(f"Unknown argument {sys.argv[i]}")
            exit(1)

    if (input_file == None):
        print("Argument --input not specified")
        exit(1)

    if (cell_x == None and cell_y != None):
        print("Argument --cell_x not specified but --cell_y is specified. Please specify --cell_x or remove --cell_y")
        exit(1)

    if (cell_y == None and cell_x != None):
        print("Argument --cell_y not specified but --cell_x is specified. Please specify --cell_y or remove --cell_x")
        exit(1)

    if (grid_x == None and grid_y != None):
        print("Argument --grid_x not specified but --grid_y is specified. Please specify --grid_x or remove --grid_y")
        exit(1)

    if (grid_y == None and grid_x != None):
        print("Argument --grid_y not specified but --grid_x is specified. Please specify --grid_y or remove --grid_x")
        exit(1)

    if (mode not in available_modes):
        print("The --mode is not a valid mode")
        exit(1)

    if (blend_amount < 0 or blend_amount > 1):
        print("Argument --blend_amount must be between 0 and 1")
        exit(1)

    if (resolution_scale != None and (grid_x != None or grid_y != None)):
        print("Argument --resolution_scale is only valid when neither --grid_x or --grid_y are specified")
        exit(1)
    if (resolution_scale == None):
        resolution_scale = 1.0
    if (resolution_scale < 0):
        print("Argument --resolution_scale must be bigger than 0")
        exit(1)
    
    if (original_path == None):
        print("Argument --input_cells_path must be specified")
        exit(1)

    if (os.path.splitext(output_file)[1] not in allowed_extensions):
        print("The only image formats supported are " + ", ".join(allowed_extensions))
        exit(1)
    if (os.path.splitext(input_file)[1] not in allowed_extensions):
        print("The only image formats supported are " + ", ".join(allowed_extensions))
        exit(1)
    
    if (cell_x == None):
        cell_x = 50
    if (cell_y == None):
        cell_y = 50

    # Create directories
    if not os.path.exists(original_path):
        os.mkdir(original_path) 
    if not os.path.exists(edited_path):
        os.mkdir(edited_path) 

    # Empty temp folder
    for f in os.listdir(edited_path):
        os.remove(os.path.join(edited_path, f))

    # Resize input images
    file_names = [f for f in listdir(original_path) if isfile(join(original_path, f))]
    file_names = [f for f in file_names if os.path.splitext(f)[1] in allowed_extensions]
    if (len(file_names) == 0):
        print(f"There are no valid image files at {original_path}")
        exit(1)
    for file_name in file_names:
        image = Image.open(original_path + "/" + file_name)
        image = image.resize((cell_x, cell_y))
        image.save(edited_path + "/" + file_name)

    # Get all the images in the path (only allow specific extensions)
    file_names = [f for f in listdir(edited_path) if isfile(join(edited_path, f))]
    file_names = [f for f in file_names if os.path.splitext(f)[1] in allowed_extensions]

    # Open the images
    images = {}
    for image_name in file_names:
        img = Image.open(edited_path + "/" + image_name)
        images[image_name] = img
    
    # Open the input image
    input_image = Image.open(input_file)

    # Calculate the grid size if grid sizes are not set
    if (grid_x == None or grid_y == None):
        sz_x = float(input_image.size[0])
        sz_y = float(input_image.size[1])
        ratio = sz_x / sz_y
        prod = 10000 * resolution_scale
        grid_y = int(sqrt(prod / ratio))
        grid_x = int(ratio * grid_y)

    # Resize input image
    input_image = input_image.resize((grid_x, grid_y))
    new_image = Image.new(mode="RGB", size=(cell_x * grid_x, cell_y * grid_y))

    # Edit the image according to --mode
    if (mode == "original"):
        # Get average color of each image
        average_colors = {}
        for image_name in file_names:
            image = images[image_name]
            img_size = image.size
            for i in range(img_size[0]):
                for j in range(img_size[1]):
                    col = image.getpixel((i, j))
                    if not image_name in average_colors.keys():
                        average_colors[image_name] = (0, 0, 0)
                    else:
                        average_colors[image_name] = tuple(map(operator.add, average_colors[image_name], col))
            sum = average_colors[image_name]
            total_pixels = img_size[0] * img_size[1]
            average_colors[image_name] = (int(sum[0] / total_pixels), int(sum[1] / total_pixels), int(sum[2] / total_pixels))

        # Create the new image
        enhancer = ImageEnhance.Contrast(input_image)
        input_image = enhancer.enhance(1.25)
        for i in range(grid_x):
            for j in range(grid_y):
                r, g, b = input_image.getpixel((i, j))
                min_loss = 1000 # Can never be more than 1000 (max 255 * 3)
                image_chosen = None
                for image_name, col in average_colors.items():
                    loss = abs(col[0] - r) + abs(col[1] - g) + abs(col[2] - b)
                    if (loss < min_loss):
                        min_loss = loss
                        image_chosen = image_name
                new_image.paste(images[image_chosen], (i * cell_x, j * cell_y))
        new_image.save(output_file)
    elif (mode == "blend"):
        for i in range(grid_x):
            for j in range(grid_y):
                r, g, b = input_image.getpixel((i, j))
                image_chosen = images[file_names[randint(0, len(file_names) - 1)]]
                # Tint image
                tint = Image.new("RGB", (image_chosen.size), color=(r, g, b))
                img = Image.blend(image_chosen, tint, blend_amount)
                new_image.paste(img, (i * cell_x, j * cell_y))
        new_image.save(output_file)
    else:
        print("Unknown mode")
        exit(1)
