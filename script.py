import face_recognition
import os
import errno
from PIL import Image

def treat_image(file_name, file_dir):
    
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
            original_pil_img = Image.fromarray(image)

            n = 0
            #ar = 23/30
            size = 500, 652
            for face_location in face_locations:
                top, right, bottom, left = face_location
                
                min_top = 0
                max_bottom = original_pil_img.height
                min_left = left*0.4
                max_right = right*1.4

                final_width = min(original_pil_img.width, max_right) - max(0, min_left)
                final_height = final_width * 652/500

                delta_height = final_height - (min(original_pil_img.height, max_bottom) - max(0, min_top))
                #print(final_width)
                #print(final_height)
                #print(delta_height)

                face_image = image[int(max(0, min_top+(delta_height/2))):int(min(original_pil_img.height, max_bottom+(delta_height/2))), int(max(0, min_left)):int(min(original_pil_img.width, max_right))]
                pil_image = Image.fromarray(face_image)
                if( n > 0):
                    print("{}/{}_{}{}".format(results_dir, os.path.splitext(os.path.basename(file_name))[0], n, os.path.splitext(os.path.basename(file_name))[1]))
                else:
                    print("{}/{}".format(results_dir, os.path.basename(file_name)))
                n = n + 1
                final_size = final_width, final_height
                pil_image.thumbnail(final_size)
                pil_image.save(results_dir+"/"+os.path.basename(file_name))
                
# traverse root directory, and list directories as dirs and files as files
for dirpath, dirnames, filenames in os.walk("./fotos"):
    print(dirpath)
    print("Sub-diretorias: {}".format(len(dirnames)))
    print("Ficheiros: {}".format(len(filenames))) 
    for filename in filenames:
        treat_image(os.path.join(dirpath, filename), dirpath)
    print("Próxima diretoria.\n")
