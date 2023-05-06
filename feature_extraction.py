from PIL import Image
import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter, interpolation
import matplotlib.pyplot as plt


def load_animals(path: str):
    img = Image.open(path)
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
    if np.abs(mag) > 1e-10: 
        return voting_set / mag
    else:
        return np.zeros(2)


def gaussian_pyramide(mat):
    down_sample = np.ones((2, 2)) / 4
    results = [mat.copy()]
    for sigma in range(3):
        mat = gaussian_filter(mat, sigma=1, radius=4, mode='mirror')
        mat = convolve2d(mat, down_sample, boundary='symm')
        mat = interpolation.zoom(mat,.5) #decimate resolution
        results.append(mat.copy())
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
    path = './database/dog/1.jpg'
    img = load_animals(path=path)
    
    # show pyramid
    # for num, im in enumerate(hiera):
    #     plt.subplot(2, 2, num + 1)
    #     plt.imshow(im, cmap='gray')
    # plt.show()

    feature_extraction(hiera)



if __name__ == '__main__':
    main()
