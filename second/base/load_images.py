from keras.preprocessing import image
import os
import matplotlib.pyplot as plt

def load_images_from_path(path, label, treshold):
    count = 0
    images, labels = [], []
    
    for file in os.listdir(path):
        if (count > treshold):
            break
        images.append(image.img_to_array(image.load_img(os.path.join(path, file), 
                                                        target_size=(224, 224, 'rgb'))))
        labels.append((label))
        count += 1

    return images, labels

def show_images(images):
    _, axes = plt.subplots(1, 8, figsize=(20, 20), subplot_kw={'xticks': [], 'yticks': []})

    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i] / 255)
    
x, y = [], []

images, labels = load_images_from_path('/home/admin/graduate-work/data/spectrograms/voice-data-minist/0/', 0, 100)
show_images(images)

x += images
y += labels

print(len(x), len(y))
