import os
from PIL import Image
import random
from pydub import AudioSegment
import os
script_dir = os.path.dirname(__file__)

def slice(path, start, end):
    sound = AudioSegment.from_mp3(path)
    extract = sound[start:end]
    extract.export('/.', format='mp3')


def cropper(width, length, x,y):
    names = os.listdir()
    for el in names:
        if el.split('.')[1] in ('jpg', 'jpeg', 'png'):
            image = Image.open(el)
            image_cropped = image.crop((x,y,x + width, y + length))
            image_cropped.save('cropped_'+ el)
    return image_cropped


def cropper_weighted(percent, x,y):
    names = os.listdir()
    for el in names:
        if el.split('.')[1] in ('jpg', 'jpeg', 'png'):
            image = Image.open(el)
            width = percent*image.size[0]
            length = percent*image.size[1]
            print(width, length)
            image_cropped = image.crop((x,y,x + width, y + length))
            image_cropped.save(str(percent) + '_cropped_'+ el)
    return image_cropped


def cropper_weighted_random(percent, string):
    output_list = []
    names = os.listdir(script_dir + '/static/Artworks Database/Artpieces/')
    print("I AM LOOKINF FOR YOU PART 2") 
    print(names)
    for el in names:
        if el.split('.')[1] in ('jpg', 'jpeg', 'png'):
            print("Im looking at this file rh " + el)
            image = Image.open(script_dir + '/static/Artworks Database/Artpieces/' + el)
            width = percent*image.size[0]
            x = random.randrange(image.size[0])
            length = percent*image.size[1]
            y = random.randrange(image.size[1])
            print(x,y)
            print(width, length)
            image_cropped = image.crop((x,y,x + width, y + length))
            path = script_dir + '/static/CroppedImages/'
            image_cropped.save(path + string)
            output_list.append(path + string)
    return output_list


def cropper_weighted(percent):
    output_list = []
    names = os.listdir()
    for el in names:
        if el.split('.')[1] in ('jpg', 'jpeg', 'png'):
            image = Image.open(el)
            width = percent*image.size[0]
            x = random.randrange(image.size[0])
            length = percent*image.size[1]
            y = random.randrange(image.size[1])
            print(x,y)
            print(width, length)
            image_cropped = image.crop((x,y,x + width, y + length))
            name = str(percent) + '_cropped_'+ el
            image_cropped.save(name)
            output_list.append(name)
    return output_list

def grab_with_threshold(image):
    x = 0
    y = 0
    step = 900
    while x + step < image.size[0]:
        while y + step < image.size[1]:
            croppy = image.crop((x,y,x+step, y+step))
            data = croppy.getdata()
            print("---------")
            for el in data:
                print(el)
            print("---------")
            croppy.show()
            y = y + step
        x = x + step
