from PIL import Image
import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter, interpolation
import matplotlib.pyplot as plt


def load_animals(path: str):
    img = Image.open(path)
    img.convert('HSV')
    pix = np.array(img)
    return pix / 255


def calc_gradient(block):
    voting_set = np.zeros(2)
    grad_y, grad_x = np.gradient(block)
    grad_x = grad_x.flatten()
    grad_y = grad_y.flatten()
    # grad_x /= grad_mag
    # grad_y /= grad_mag
    # grad_dir = np.arctan(grad_y , grad_x).flatten() / np.pi * 180
    # grad_mag = grad_mag.flatten()
    # for iD, i in enumerate(grad_dir):
    #     num = int(i // 15)
    #     voting_set[num] += grad_mag[iD]
    for y, x in zip(grad_x, grad_y):
        voting_set[0] += x
        voting_set[1] += y
    mag = np.linalg.norm(voting_set)
    # x = []
    # y = []
    # for i in range(8):
    #     for j in range(8):
    #         x.append(i)
    #         y.append(j)

    # x = np.array(x)
    # y = np.array(y)
    # print(x)
    # print(y)
    # plt.imshow(block, cmap='gray')
    # for xx, yy, dx, dy in zip(x, y, grad_x, grad_y):
    #     plt.arrow(xx, yy, dx, dy, color='red', width = 0.05)
    # plt.show()
    if np.abs(mag) > 1e-10: 
        return voting_set / mag
    else:
        return np.zeros(2)


# def gaussian_pyramide(mat):
#     down_sample = np.ones((2, 2)) / 4
#     results = [mat.copy()]
#     for sigma in range(3):
#         mat = gaussian_filter(mat, sigma=1, radius=4, mode='mirror')
#         mat = convolve2d(mat, down_sample, boundary='symm')
#         mat = interpolation.zoom(mat,.5) #decimate resolution
#         results.append(mat.copy())
#     return results


def gaussian_pyramide(mat):
    down_sample = np.ones((2, 2)) / 4
    results = []
    for i in range(3):
        hsv_seg = mat[:, :, i]
        results.append(hsv_seg.copy())
        for _ in range(3):
            hsv_seg = gaussian_filter(hsv_seg, sigma=1, radius=4, mode='mirror')
            hsv_seg = convolve2d(hsv_seg, down_sample, boundary='symm')
            hsv_seg = interpolation.zoom(hsv_seg,.5) #decimate resolution
            results.append(hsv_seg.copy())
    return results

def feature_extraction(img):
    blocks = None
    for image in img:
        width, _  = image.shape
        count = 0
        for i in range(0, width, 8):
            for j in range(0, width, 8):
                count += 1
                block = image[i: i + 8, j: j + 8]
                voting =calc_gradient(block)
                if blocks is None:
                    blocks = voting.copy()
                else:
                    blocks = np.hstack((blocks, voting))
                # show grid view of block voting results
                # plt.subplot(8, 8, count)
                # plt.imshow(block, cmap='gray')
    return blocks


def main():
    path = '/Users/lukasye/Projects/ImageArrow/LinnaeusDS/test/dog/2_64.jpg'
    img = load_animals(path=path)
    hiera = gaussian_pyramide(img) 
    # show pyramid
    # for num, im in enumerate(hiera):
    #     plt.subplot(2, 2, num + 1)
    #     plt.imshow(im, cmap='gray')
    # plt.show()

    blocks = feature_extraction(hiera)
    print(blocks)
    print(blocks.shape)



if __name__ == '__main__':
    main()
