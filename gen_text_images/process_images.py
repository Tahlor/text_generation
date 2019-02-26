import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# crop too long images for now? can edit bounding boxes to get GT
    # you don't need GT, you need to have a language model etc. anyway?
    # somehow you need to go from some encoding to actual words

def resize_image(image, target_ratio=1.0, tolerance=.2, output_short_dimension=64, pad_color=(255,255,255)):
    """
    Args:
        image (array-like): numpy array of image
        target_ratio: between 0,1, ratio of short:long side
        tolerance (float): Value between 0,1; how close the ratio should be after cropping
                           1 is 0 tolerance, 0 is infinite tolerance
        output_short_dimension (int): output of short dimension
        pad_color (3-tuple): 3-tuple for 3-D images

    Returns:
        array-like: numpy array of resized image
    """
    short_axis = np.argmin(image.shape[:2])
    long_axis = not short_axis
    _3d = len(image.shape)==3
    ratio = image.shape[short_axis] / image.shape[long_axis]

    too_short_axis = short_axis if ratio < target_ratio else long_axis

    ## Fill short axis with white space
    if too_short_axis == 1: # don't add white space on Y-axis
        if ratio >= target_ratio * 1/tolerance or ratio <= target_ratio*tolerance:
            diff = int(abs(image.shape[0] - image.shape[1])* target_ratio * tolerance / 2) # go to tolerance by default
            npad = [(0, 0), (0, 0)] if not _3d else [(0, 0), (0, 0), (0, 0)]
            npad[too_short_axis] = (diff, diff)
            image = np.pad(image, pad_width=npad, mode='constant', constant_values=0)

            if too_short_axis == 0:
                image[0:diff] = pad_color
                image[-diff:None] = pad_color
            else:
                image[:, 0:diff] = pad_color
                image[:, -diff:None] = pad_color

    # resize to do the rest
    old_x = image.shape[0]
    old_y = image.shape[1]

    if old_x < old_y:
        x_size = output_short_dimension
        y_size = int(output_short_dimension * 1/target_ratio)
    else:
        y_size = output_short_dimension
        x_size = int(output_short_dimension * 1/target_ratio)

    image = cv2.resize(image, dsize=(y_size, x_size))[:,:]
    return image

def recrop_image(image, color_threshold=180, x_padding=20, y_padding=2):
    """ Crop image from path to content (e.g. darkest pixels, alpha channel)

    Args:
        image_path (array-like): Numpy array of image
        color_threshold: pixels darker than this will be considered border
        x_padding: padding to add after choosing crop

    Returns:
        np-array: A BGR numpy picture representation
    """

    ## Define crop max
    if len(image.shape)==3:
        average_color = np.mean(image, axis=2)
        mask_coords = np.where(average_color < color_threshold)
    else:
        mask_coords = np.where(image < color_threshold)

    # crop to picture
    x_min = np.min(mask_coords[0])
    x_max = np.max(mask_coords[0])
    y_min = np.min(mask_coords[1])
    y_max = np.max(mask_coords[1])

    x_min = max(0, x_min - x_padding)
    x_max = min(image.shape[0], x_max + x_padding)
    y_min = max(0, y_min - y_padding)
    y_max = min(image.shape[1], y_max + y_padding)

    # crop to image
    image = image[x_min:x_max, y_min:y_max]

    return image

def make_3d(image):
    """ Make a 1 color image 3

    Args:
        image:

    Returns:

    """
    return np.tile(image[:,:, None],[1,1,3])

def end_to_end(image_path):
    _3d = False
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED) # in BGR
    if _3d:
        image = make_3d(image)
        color = (255,255,255)
    else:
        color = 255
    #image = image[:,:,::-1] # reverse colors
    cropped_image = recrop_image(image)
    image = resize_image(cropped_image, tolerance=1, pad_color=color, target_ratio=1/20.)
    #cv2.imwrite(output_path, image)
    # print(image.shape)
    # plt.imshow(image,cmap='gray')
    # plt.show()
    return image

def show_image(image):
    plt.imshow(image,cmap='gray')
    plt.show()

def save_image(path, image):
    #print(path)
    cv2.imwrite(path, image)

def loop(input="./datasets/handwriting/testA", output=None):
    if output is None:
        output=input
    for ds, ss, fs in os.walk(input):
        for i, f in enumerate(fs):
            if i % 1000 ==0:
                print("Step: {}".format(i))
            image_path = os.path.join(input, f)
            output_path = os.path.join(output, f)
            image = end_to_end(image_path)
            cv2.imwrite(output_path, image)

if __name__=='__main__':
    #loop("./datasets/handwriting/testA")
    loop("./datasets/handwriting/trainA")
    loop("./datasets/handwriting/val")

    #end_to_end("/media/taylor/eef4fe97-0587-4acb-b65d-f0ad5ed8d623/taylor/GitHub/MUNIT/datasets/handwriting/testA/a05-058-06.png")