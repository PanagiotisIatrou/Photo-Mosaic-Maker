# Photo-Mosaic-Maker
A python command line tool for creating effortless photo mosaics

![](/Examples/out1.jpg)

## How to install
Clone the repository or just download the repository as a .zip

## How to use
Depending on the platform, you can run the program by:  
**Linux:** ```python3 mosaic.py```  
**Windows:** ```py mosaic.py```

The only needed argument is the ```--input filename.jpg``` which sets the image to create a mosaic out of.  
Put all the images that are going to be used as cells in the Images/ folder.

Also, see the examples below.

## List of configurations
* ```--output filename.jpg```  
Saves the output image as filename.jpg.  
* ```--input filename.jpg```  
Takes filename.jpg as the input image.
* ```--mode mode_selected```  
Sets the current mode to mode_selected. There are currently 2 modes available, **blend** and **original**. When ```--mode``` is not specified, **blend** mode is selected by default. **blend** mode uses a random image from the Images/ folder and applies a tint in each cell to match the input image color. **original** mode takes the average color for each image in the Images/ folder and tries to match the input image pixels as close as possible without tampering with the color.
* ```--blend_amount number```  
This argument is only valid when the ```--mode``` is set to blend. It defaults to 0.8 and specifies how much color tint is used in each cell of the mosaic. Smaller value leads to clearer cells but more crude output image, while bigger values lead to fainted cells but smoother output image.
* ```--resolution_scale number```  
This argument is only valid when neither ```--grid_x``` or ```--grid_y``` are specified (Also read ```--grid_x``` argument). It applies a factor to the total number of cells of the mosaic (which by default is 10000). For example, a value of 2 would set the total number of cells of the mosaic to 20000, while a value of 0.5 would set the total number of cells of the mosaic to 5000.
* ```--cell_x number```  
Sets the width of each cell. The program shrinks each image from the Images/ folder so that each cell of the output image is the same. By default, if not specified, ```--cell_x``` is set to 50.
* ```--cell_y number```  
Sets the width of each cell. By default, if not specified, ```--cell_y``` is set to 50.
* ```--grid_x number```  
Sets the width of the mosaic grid. By default, if neither ```--grid_x``` or ```--grid_y``` are specified, the program tries to match the input image aspect ratio such that the total number of cells in the mosaic does not exceed 10000.
* ```--grid_y number```  
Sets the height of the mosaic grid.

## Supported image formats
* .jpg
* .jpeg
* .png

## Examples
```python3 mosaic.py --input Examples/photo1.jpg --output out1.jpg```
This creates the image on the top.