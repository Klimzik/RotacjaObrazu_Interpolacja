import math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def show_image(image1, image2):
    fig, axs = plt.subplots(1, 2)

    axs[0].imshow(image1.astype('uint8'))
    axs[1].imshow(image2.astype('uint8'))
    axs[0].title.set_text('Original')
    axs[1].title.set_text('Rotated')
    plt.show()


def interpolation(edit_img, edit_img_0_1):   # funkcja ktora zlicza na okolo punkty w sume i liczy srednią
    for l in range(3):
        for x in range(edit_img.shape[0]):
            for y in range(edit_img.shape[1]):
                values, counter = 0, 0
                if edit_img_0_1[x, y, l] == 0:
                    for a in range(x - 1, x + 2):
                        for b in range(y - 1, y + 2):
                            if a > edit_img.shape[0] - 1 or a < 0 or b > edit_img.shape[1] - 1 or b < 0:
                                continue
                            if edit_img_0_1[a, b, l] == 1:
                                values += edit_img[a, b, l]
                                counter += 1
                    if counter != 0:
                        edit_img[x, y, l] = values / counter


def rotation_matrix(x, y, angle):
    rotation_martix = np.array([[math.cos(math.radians(angle)), -math.sin(math.radians(angle))],
                                [math.sin(math.radians(angle)), math.cos(math.radians(angle))]])
    return round(x*rotation_martix[0, 0]+y*rotation_martix[1, 0]), round(x*rotation_martix[0, 1]+y*rotation_martix[1, 1])


def rotation(img_original, img_rotated, img_rotated_0_1, angle):
    x1, y1 = int(img_original.shape[0]/2), int(img_original.shape[1]/2)
    for x in range(img_original.shape[0]):
        for y in range(img_original.shape[1]):
            if y == y1:   # dla prawej strony zdj
                y1 = y1-1
            if y == 0:    # dla lewej strony zdj
                y1 = img_original.shape[1]/2
            if x == x1:   # dla dolnej czesci zdj
                x1 = x1-1
            a1 = rotation_matrix(x1-x, y-y1, angle)[0]
            b1 = rotation_matrix(x1-x, y-y1, angle)[1]
            if rotation_matrix(x1-x, y-y1, angle)[0] > 0:   # tutaj te ify by wrocic na stre wspolrzedne
                a = round(img_original.shape[0]/2)-a1
            else:
                a = round(img_original.shape[0]/2)-a1-1
            if rotation_matrix(x1-x, y-y1, angle)[1] > 0:
                b = round(b1-1-(img_original.shape[1]/2))
            else:
                b = round(b1-(img_original.shape[1]/2))
            if (a >= 0) and ((img_original.shape[0]-1) >= a) and (b <= 0) and (-(img_original.shape[1]-1) <= b):
                img_rotated[a, b] = img_original[x, y]
                img_rotated_0_1[a, b, :] = 1


image = cv.imread('blackbuck.bmp')
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

rotated_image = np.zeros(image.shape)
rotated_image_0_1 = np.zeros(image.shape)

rotation(image, rotated_image, rotated_image_0_1, 80)  # kat obrotu
interpolation(rotated_image, rotated_image_0_1)
show_image(image, rotated_image)
