from keras.utils import load_img, img_to_array
import os
import matplotlib.pyplot as plt

def load_images_from_path(path, label, treshold):
    count = 0
    images, labels = [], []
    
    for file in os.listdir(path):
        if (count > treshold):
            break
        images.append(img_to_array(load_img(os.path.join(path, file), 
                                            target_size=(224, 224), 
                                            color_mode='rgb')))
        labels.append((label))
        count += 1

    return images, labels

def show_images(images):
    num_images = min(len(images), 8)
    _, axes = plt.subplots(1, num_images, figsize=(20, 20), 
                           subplot_kw={'xticks': [], 'yticks': []})

    for i, ax in enumerate(axes.flat):
        if i < len(images):
            ax.imshow(images[i] / 255.0)
