import cv2
import numpy as np
import random
import os 
import json

output_directory = "synthetic_dataset"

ann_file = "annotations.json"

categories = [
    {
        "id": 1,
        "name": "object",
        "supercategory": "none"
    } ]

def rotate_image(img, angle):
    # Get image size
    height, width = img.shape[:2]

    # Calculate image center and rotation matrix
    center = (width / 2, height / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Perform rotation
    rotated_img = cv2.warpAffine(img, matrix, (width, height), flags=cv2.INTER_LINEAR)

    return rotated_img



def main():
    annotations = []
    for i in range(1000):
        bg = cv2.imread('background.png')
        obj = cv2.imread('object.png', cv2.IMREAD_UNCHANGED)
        # Get the dimensions of the object image
        rows, cols, channels = obj.shape
        instance = random.randint(1,4)
        for j in range(instance):
        # Define a region of interest on the background image
            bg_h, bg_w, _ = bg.shape
            x_offset = random.randint(0, bg_w-cols)
            y_offset = random.randint(0, bg_h-rows)
            roi = bg[y_offset:y_offset+rows, x_offset:x_offset+cols]
            
            # Rotate the object image to a random angle
            angle = random.randint(0, 360)
            obj_rotated = rotate_image(obj, angle)

            # Create a mask for the rotated object image
            mask = obj_rotated[:, :, 3]
            mask_inv = cv2.bitwise_not(mask)

            # Convert the rotated object image to RGB and get the color channels
            obj_rgb = cv2.cvtColor(obj_rotated, cv2.COLOR_BGRA2BGR)
            obj_b, obj_g, obj_r = cv2.split(obj_rgb)

            # Blending the object on the background image
            bg_b = cv2.bitwise_and(roi[:, :, 0], roi[:, :, 0], mask=mask_inv)
            bg_g = cv2.bitwise_and(roi[:, :, 1], roi[:, :, 1], mask=mask_inv)
            bg_r = cv2.bitwise_and(roi[:, :, 2], roi[:, :, 2], mask=mask_inv)
            obj_b = cv2.bitwise_and(obj_b, obj_b, mask=mask)
            obj_g = cv2.bitwise_and(obj_g, obj_g, mask=mask)
            obj_r = cv2.bitwise_and(obj_r, obj_r, mask=mask)
            blend_b = cv2.add(bg_b, obj_b)
            blend_g = cv2.add(bg_g, obj_g)
            blend_r = cv2.add(bg_r, obj_r)
            blend = cv2.merge((blend_b, blend_g, blend_r))
            bg[y_offset:y_offset+rows, x_offset:x_offset+cols] = blend

            # Add annotations to the list
            annotation = {}
            annotation["image_id"] = i
            annotation["category_id"] = 1 # Change this to the appropriate category ID
            annotation["bbox"] = [x_offset, y_offset, cols, rows]
            annotations.append(annotation)

        
        # save the blended image
        filename = "dataset_"+str(i)+".png"
        cv2.imwrite(os.path.join(output_directory, filename), bg)
    #add the catogories , annotaions in json
    data = {
    "categories": categories,
    "annotations": annotations
    }

    with open(ann_file, "w") as f:
        json.dump(data, f)

main()
    
