# Synthetic Dataset Generator
This is a Python script that generates a synthetic dataset of images with randomly placed and rotated objects on a background image. The generated dataset can be used for training and testing computer vision models.

Requirements
To run this script, you need the following packages installed:

- OpenCV (cv2)
- NumPy
- Random
- OS
- JSON

### How to Use
Put the background image (background.png) and object image (object.png) in the same directory as the script.
Specify the output directory and annotation file name in the script.
Define the categories for the objects in the script.
### Run the script.
The script generates 1000 images by default. You can change the number of images by modifying the loop range in the main() function.

The generated images will be saved in the specified output directory, and the annotations will be saved in a JSON file with the specified file name.

### How it Works
The script randomly selects a region of interest on the background image and rotates the object image to a random angle. It then blends the rotated object image onto the background image at the selected region of interest using bitwise operations. Finally, it saves the blended image and adds the annotations to the list of annotations.

The annotations include the image ID, category ID, and bounding box coordinates of the object on the image. The category ID is set to 1 by default, but you can change it to the appropriate category ID for your use case.
