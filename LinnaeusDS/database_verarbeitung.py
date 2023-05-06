from PIL import Image
import os

basewidth = 64
new_height = 64
new_width = 64

def main(train_path):
    train_set = os.listdir(train_path)
    for ele in train_set:
        tmp_path = os.path.join(train_path, ele)
        images = os.listdir(tmp_path)
        for image in images:
            path = os.path.join(tmp_path, image)
            img = Image.open(path)
            img = img.convert("L")
            img.save(path)
    print('Complete!')


def shrink_db(train_path, num = 600):
    train_set = os.listdir(train_path)
    for ele in train_set:
        tmp_path = os.path.join(train_path, ele)
        images = os.listdir(tmp_path)
        for id, image in enumerate(images):
            path = os.path.join(tmp_path, image)
            os.remove(path)
            if id == num - 1:
                break
    print('Complete!')


if __name__ == '__main__':
    main(train_path='./train/')
    main(train_path='./test/')
    shrink_db(train_path='./train/')
    shrink_db(train_path='./test/', num=200)