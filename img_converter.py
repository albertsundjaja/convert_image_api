import cv2

def convert_image(image_name):
    """
    Convert the image into grayscale using cv2 library, it will replace the original file

    :param image_name: the image name to be converted e.g. image.png
    """
    image = cv2.imread('temp/' + image_name)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cv2.imwrite('temp/' + image_name)