import face_recognition
import os
import errno
from PIL import Image

def treat_image(file_name, file_dir, n):
    
        #print(file_name)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            
            #Cria diretorias para guardar os resultados se não existem
            results_dir = os.path.dirname(file_name)+"_resultados"
            if(not os.path.isdir(results_dir)):
                try:
                    os.makedirs(results_dir)
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
                
            image = face_recognition.load_image_file(file_name)
            face_locations = face_recognition.face_locations(image)

            
            offsetx = 40
            offsety = 40
            for face_location in face_locations:
                top, right, bottom, left = face_location
                print("top: {}, left: {}, bottom: {}, right: {}".format(top,left, bottom, right))
                face_image = image[top-offsety:bottom+offsety, left-offsetx:right+offsetx]
                pil_image = Image.fromarray(face_image)
                pil_image.save("{}-{}.jpg".format(os.path.splitext(os.path.basename(file_name))[0], n))
                

i = 0
# traverse root directory, and list directories as dirs and files as files
for dirpath, dirnames, filenames in os.walk("./fotos"):
    print(dirpath)
    print("Sub-diretorias: {}".format(len(dirnames)))
    print("Ficheiros: {}".format(len(filenames))) 
    for filename in filenames:
        treat_image(os.path.join(dirpath, filename), dirpath, i)
        i = i+1
    print("Próxima diretoria.\n")
