import face_recognition
import os
import errno
import sys
import csv
import datetime
import cv2
from PIL import Image

if len(sys.argv) < 2:
    print("Please pass folder argument")
    sys.exit()

if len(sys.argv) > 2 and sys.argv[2] == 'debug':
    debug = True
else:
    debug = False


report_header = ['Ficheiro', 'Resolucao_Original', 'Resolucao_Calculada', 'Aspect_Ratio_Calculado', 'Erro_Calculo']
report_lines = []

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

                min_top = max(top - face_height*0.6, 0)
                max_bottom = min(bottom + face_height*0.6, original_pil_img.height)

                min_left = max(left - face_width*0.5, 0)
                max_right = min(right + face_width*0.5, original_pil_img.width)

                if max_right-abs(min_left) > original_pil_img.width:
                    final_width = original_pil_img.width
                else:
                    final_width = max_right-abs(min_left)

                if max_bottom-abs(min_top) > original_pil_img.height:
                    final_height = original_pil_img.height
                else:
                    final_height = max_bottom-abs(min_top)

                if debug:
                    originalImage = cv2.imread(file_name)
                    # Draw a box around the face
                    cv2.rectangle(originalImage, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 5)
                    cv2.rectangle(originalImage, (int(min_left), int(min_top)), (int(max_right), int(max_bottom)), (0, 0, 255), 4)
                    cv2.imwrite(results_dir+"/"+os.path.splitext(os.path.basename(file_name))[0]+"_debug"+
                    os.path.splitext(os.path.basename(file_name))[1],originalImage)

                if original_pil_img.width >= original_pil_img.height:
                    # caso a foto esteja em landscape
                    # fixa a largura
                    # calcula a altura
                    final_height = max_bottom - min_top
                    final_width = final_height * 115/150
                    
                else:
                    # caso a foto esteja em portrait
                    # fixa a altura
                    # calcula a largura consoante o ASPECT RATIO
                    final_width = max_right - min_left
                    final_height = final_width * 150/115
                    
                # crop imagem no formato correto
                # centro da cara esta em ((right-left)/2, (bottom-top)/2)
                center_y = min_top + (bottom-min_top)/2
                y_min = int(center_y - final_height/2)
                y_max = int(center_y + final_height/2)

                if y_min < 0:
                    aux_y = y_min
                    y_min = 0
                    y_max = y_max - aux_y
                if y_max > original_pil_img.height:
                    y_max = original_pil_img.height
                    final_width = (y_max-y_min) * 115/150
                    
                center_x = min_left + (max_right-min_left)/2
                x_min = int(center_x - final_width/2)
                x_max = int(center_x + final_width/2)

                face_image = image[y_min:y_max, x_min:x_max]
                pil_image = Image.fromarray(face_image)
                
                nome_ficheiro = ""
                if( n > 0):
                    nome_ficheiro = "{}/{}_{}{}".format(results_dir, os.path.splitext(os.path.basename(file_name))[0], 
                    n, os.path.splitext(os.path.basename(file_name))[1])
                    print("{}/{}_{}{}".format(results_dir, os.path.splitext(os.path.basename(file_name))[0], 
                    n, os.path.splitext(os.path.basename(file_name))[1]))
                else:
                    nome_ficheiro = "{}/{}".format(results_dir, os.path.basename(file_name))
                    print("{}/{}".format(results_dir, os.path.basename(file_name)))
                n = n + 1

                final_size = int(x_max-x_min), int(y_max-y_min)
                
                res_original = "{}x{}".format(original_pil_img.width, original_pil_img.height)
                print(res_original)
                res_calculada = "{}x{}".format(x_max-x_min, y_max-y_min)
                print(res_calculada)
                aspect_ratio = (x_max-x_min)/(y_max-y_min)
                print(aspect_ratio)
                erro_calculado = abs(aspect_ratio - (115/150))
                pil_image.thumbnail(final_size)
                pil_image.save(results_dir+"/"+os.path.basename(file_name))

                report_lines.append([nome_ficheiro, res_original, res_calculada, aspect_ratio, erro_calculado])
                
# traverse root directory, and list directories as dirs and files as files
for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    print(dirpath)
    print("Sub-diretorias: {}".format(len(dirnames)))
    print("Ficheiros: {}".format(len(filenames))) 
    for filename in filenames:
        treat_image(os.path.join(dirpath, filename), dirpath)
    print("Proxima diretoria.\n")

if not debug:
    with open('report-{}.csv'.format(datetime.datetime.now()), 'w', newline='') as csvfile:
        report_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        report_writer.writerow(report_header)
        for line in report_lines:
            report_writer.writerow(line)
