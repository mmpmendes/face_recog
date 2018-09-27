import face_recognition
import os
import errno
from PIL import Image

def treat_image(file_name, file_dir):
    
        #print(file_name)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            
            #Cria diretorias para guardar os resultados se nao existem
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
            for face_location in face_locations:
                top, right, bottom, left = face_location
                # quadrado da cara
                
                # buffer para a cara
                # incluir cabelo, pescoco etc

                face_width = right-left
                face_height = bottom-top

                min_top = top - face_height*0.2
                max_bottom = bottom + face_height*0.8

                min_left = left - face_width*1.05
                max_right = right + face_width

                final_width = original_pil_img.width
                final_height = original_pil_img.height

                if original_pil_img.width > original_pil_img.height:
                    # caso a foto esteja em portrait
                    # fixa a largura
                    # calcula a altura
                    final_width = max_right - min_left
                    final_height = final_width * 150/115
                    if final_height > original_pil_img.height:
                        final_height = original_pil_img.height
                        final_width = final_height * 115/150
                    
                else:
                    # caso a foto esteja em landscape
                    # fixa a altura
                    # calcula a largura consoante o ASPECT RATIO
                    final_height = max_bottom - min_top
                    final_width = final_height * 115/150
                    
                # crop imagem no formato correto
                # centro da cara esta em ((right-left)/2, (bottom-top)/2)
                center_x = min_left + (max_right-min_left)/2
                x_min = int(max(center_x - final_width/2, 0))
                x_max = int(min(center_x + final_width/2, original_pil_img.width))

                center_y = min_top + (bottom-min_top)/2
                y_min = int(max(center_y - final_height/2, 0))
                y_max = int(min(center_y + final_height/2, original_pil_img.height))

                face_image = image[y_min:y_max, x_min:x_max]
                pil_image = Image.fromarray(face_image)
                if( n > 0):
                    print("{}/{}_{}{}".format(results_dir, os.path.splitext(os.path.basename(file_name))[0], n, os.path.splitext(os.path.basename(file_name))[1]))
                else:
                    print("{}/{}".format(results_dir, os.path.basename(file_name)))
                n = n + 1

                final_size = int(final_width), int(final_height)
                print(final_size)
                pil_image.resize(final_size)
                pil_image.thumbnail(final_size)
                pil_image.save(results_dir+"/"+os.path.basename(file_name))
                
# traverse root directory, and list directories as dirs and files as files
for dirpath, dirnames, filenames in os.walk("./f2"):
    print(dirpath)
    print("Sub-diretorias: {}".format(len(dirnames)))
    print("Ficheiros: {}".format(len(filenames))) 
    for filename in filenames:
        treat_image(os.path.join(dirpath, filename), dirpath)
    print("Proxima diretoria.\n")
