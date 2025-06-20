from django.http import HttpResponse
from django.shortcuts import render, redirect
from ImageStorage.models import ImageFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from tensorflow.keras.utils import load_img
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array

def home(request):
    if request.method == "POST":
        image=request.FILES.get('imagedata')
        if image:
            s = ImageFile(img=image)
            s.save()
            return render(request, 'welcome.html',{})
    return render(request, 'Home.html')


def GenerateSingleImage(request):
    if request.method == 'POST':
        img_obj = ImageFile.objects.last()
        num=request.POST.get('number')
        n = int(num)
        print(type(n))
        img_path = os.path.join(settings.MEDIA_ROOT, str(img_obj.img))

        # ✅ Load the image with target size directly
        img = load_img(img_path, target_size=(1000, 1000))

        # ✅ Apply augmentation
        datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )

        # ✅ Convert image to array
        img_array = img_to_array(img)
        input_batch = img_array.reshape((1, 1000, 1000, 3))
        print(input_batch)
        i=0
        save_path = os.path.join(settings.BASE_DIR,  'Imagefolder')
        for output in datagen.flow(input_batch,batch_size=1, save_to_dir=save_path, save_format='jpeg'):
         i=i+1
         if i==n:
          break
        # ✅ You can apply datagen if needed like:
        # aug_iter = datagen.flow(input_batch)
        # aug_img = next(aug_iter)[0]  # first augmented image

        return HttpResponse("Image uploaded and processed successfully.")

    return HttpResponse("Only POST method allowed", status=405)
