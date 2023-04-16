import cv2
import numpy as np
from PIL import Image


def nd_img_rgb_to_bgr(nd_img):
    return cv2.cvtColor(np.array(nd_img), cv2.COLOR_RGB2BGR)


def check_image_is_valid(imgBGR24, threshold, orientation='Vertical'):
    gray_img = convert_nd_img_to_gray(imgBGR24)

    _, img_bw = binary_image_apply_threshold(gray_img, threshold)

    binary_img = Image.fromarray(img_bw)

    first_wp = None
    second_wp = None
    if (orientation == 'Vertical'):
        first_wp = image_white_percentage(
            crop_img_section_y(binary_img, 0.25, 'top'))

        second_wp = image_white_percentage(
            crop_img_section_y(binary_img, 0.25, 'bottom'))
    else:
        first_wp = image_white_percentage(
            crop_img_section_x(binary_img, 0.25, 'left'))

        second_wp = image_white_percentage(
            crop_img_section_x(binary_img, 0.25, 'right'))

    return first_wp, second_wp


def convert_frame_to_gray(img_nd_array_bgr24):
    return convert_nd_img_to_gray(img_nd_array_bgr24)


def convert_nd_img_to_gray(img):
    return cv2.cvtColor(
        img, cv2.COLOR_BGR2GRAY
    )


def binary_image_apply_threshold(gray_img, threshold):
    return cv2.threshold(
        gray_img, threshold, 255, cv2.THRESH_BINARY)


def image_white_percentage(img: Image.Image):
    total_pixels = np.prod(img.size)
    nd_img = np.array(img)
    num_white_pixels = np.count_nonzero(nd_img)
    if (num_white_pixels == 0):
        return 0
    percent_white = (num_white_pixels / (total_pixels)) * 100
    return percent_white


def crop_img_section_y(img: Image.Image, percentage, part='top'):
    height = img.size[1]

    # Define the top section of the image
    height_percent = int(percentage * height)

    # Define the bottom section of the image
    bottom_height = int(percentage * height)
    bottom_start = height - bottom_height

    img_section = img.crop((0, 0, img.size[0], height_percent))

    if (part == 'bottom'):
        img_section = img.crop((0, bottom_start, img.size[0], height))

    return img_section


def crop_img_section_x(img: Image.Image, percentage, part='left'):
    width = img.size[0]

    # Define the left section of the image
    width_percent = int(percentage * width)

    # Define the right section of the image
    right_width = int(percentage * width)
    right_start = width - right_width

    img_section = img.crop((0, 0, width_percent, img.size[1]))

    if (part == 'right'):
        img_section = img.crop((right_start, 0, width, img.size[1]))

    return img_section


def check_top_green_percentage(img, section='top'):
    height = img.size[1]

    # Define the top section of the image
    height_percent = int(0.25 * height)

    # Define the bottom section of the image
    bottom_height = int(0.25 * height)
    bottom_start = height - bottom_height

    img_section = img.crop((0, 0, img.size[0], height_percent))

    if (section == 'bottom'):
        img_section = img.crop((0, bottom_start, img.size[0], height_percent))

    # Convert the cropped image to the HSV color space
    hsv_img = img_section.convert('HSV')

    # Define a lower and upper green color range in HSV values
    lower_green = np.array([50, 93, 81])  # dark green
    upper_green = np.array([145, 181, 139])  # light green

    # Threshold the image using the green color range to create a binary mask of green pixels
    green_mask = cv2.inRange(np.array(hsv_img), lower_green, upper_green)

    # Calculate the percentage of green pixels in the mask
    green_percentage = np.sum(green_mask == 255) / \
        (img_section.size[0] * img_section.size[1])
    return green_percentage


def check_image_section_is_not_black(img, section='top'):
    height = img.size[1]

    # Define the top section of the image
    height_percent = int(0.25 * height)

    # Define the bottom section of the image
    bottom_height = int(0.25 * height)
    bottom_start = height - bottom_height

    img_section = img.crop((0, 0, img.size[0], height_percent))

    if (section == 'bottom'):
        img_section = img.crop((0, bottom_start, img.size[0], height_percent))

    # Convert the cropped image to the HSV color space
    hsv_img = img_section.convert('HSV')

    # Define a lower and upper black color range in HSV values
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])

    # Threshold the image using the black color range to create a binary mask of black pixels
    black_mask = cv2.inRange(np.array(hsv_img), lower_black, upper_black)

    # Calculate the percentage of black pixels in the mask
    black_percentage = np.sum(black_mask == 255) / \
        (img_section.size[0] * img_section.size[1])
    return black_percentage


def crop_only_contact_sections(binary_tresh_img, crop_percent=0.1, orientation='Vertical'):
    if (orientation == 'Vertical'):
        height, width = binary_tresh_img.shape[:2]
        roi_top = int(crop_percent * height)
        roi_bottom = int(1 - crop_percent * height)
        mask = np.zeros((height, width), dtype=np.uint8)
        mask[:roi_top, :] = 255
        mask[roi_bottom:, :] = 255
        return cv2.bitwise_and(binary_tresh_img, binary_tresh_img, mask=mask)
    else:
        height, width = binary_tresh_img.shape[:2]
        roi_left = int(crop_percent * width)
        roi_right = int(1 - crop_percent * width)
        mask = np.zeros((height, width), dtype=np.uint8)
        mask[:, :roi_left] = 255
        mask[:, roi_right:] = 255
        return cv2.bitwise_and(binary_tresh_img, binary_tresh_img, mask=mask)
