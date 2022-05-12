# quiero librerias infinitas amigo
# https://stackoverflow.com/questions/54632009/how-to-increase-the-maximum-size-of-the-aws-lambda-deployment-package-requesten
# https://thinkinfi.com/yolo-object-detection-using-python-opencv/
# https://pjreddie.com/darknet/yolo/
# https://pjreddie.com/darknet/install/
# <a href="https://thinkinfi.com/basic-python-opencv-tutorial-function/" data-internallinksmanager029f6b8e52c="14" title="OpenCV" target="_blank" rel="noopener">opencv</a> object tracking
# object detection and tracking <a href="https://thinkinfi.com/basic-python-opencv-tutorial-function/" data-internallinksmanager029f6b8e52c="14" title="OpenCV" target="_blank" rel="noopener">opencv</a>
# https://docs.opencv.org/3.4/db/d30/classcv_1_1dnn_1_1Net.html

from sklearn.cluster import KMeans
import sys
import cv2
import numpy as np
import json
import boto3
import os

def testYolo(src_, types_):
    # Loading image


    img = None

    #img_ORIGINAL = None

    if os.name != 'nt':
        session = boto3.Session(profile_name='default')
        dev_client = session.client('s3')
        dev_resource = boto3.resource('s3')
        bucket_name = "cadem-vision-artificial-photos"

        print(f"vamos a abrir: vision_artificial/{src_}, en el bucket:{bucket_name}")
        file_obj = dev_client.get_object(
            Bucket=bucket_name, Key=f'vision_artificial/{src_}')
        # reading the file content in bytes
        file_content = file_obj["Body"].read()

        # creating 1D array from bytes data range between[0,255]
        np_array = np.frombuffer(file_content, np.uint8)

        # decoding array
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        img_ORIGINAL = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    else:
        path_ = "C:/RSILVA_REPOS/TEST_CLASIFICATOR/python/"
        img = None
        img = cv2.imread(f'{path_}{src_}')
        #print(f"tamos en windors compare:{src_}")

    salida = {}

    #img = cv2.imread(f'{path_}{src_}')

    # Load Yolo
    yolo_weight = "C:/RSILVA_REPOS/yolov3.weights"
    yolo_config = "yolov3.cfg"
    coco_labels = "coco.names"
    net = cv2.dnn.readNet(yolo_weight, yolo_config)

    classes = []
    with open(coco_labels, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # print(classes)

    # # Defining desired shape
    fWidth = 1024
    fHeight = 1024
    #fWidth = 2048
    #fHeight = 2048
    #fWidth = 4096
    #fHeight = 4096
    out_flag = f"{fWidth}{fHeight}"

    # Resize image in opencv
    img = cv2.resize(img, (fWidth, fHeight))

    img_ORIGINAL_TO_1024 = cv2.resize(img, (fWidth, fHeight))
    # SOLO EN DEV
    # cv2.imwrite(f'{path_}_ORIG_BANDEJERO_1024_{src_}',img)

    height, width, channels = img.shape

    # Convert image to Blob
    blob = cv2.dnn.blobFromImage(
        img, 1/255, (fWidth, fHeight), (0, 0, 0), True, crop=False)
    # Set input for YOLO object detection
    net.setInput(blob)

    # Find names of all layers
    layer_names = net.getLayerNames()
    #print(layer_names)
    # Find names of three output layers
    # ORIGINAL_ERROR _     output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    colors_TYPE = np.random.uniform(0, 255, size=(50, 3))

    pos_ = 0
    for i in net.getUnconnectedOutLayers():
        #print(f"pos:{pos_}:getUnconnectedOutLayers:{i}")
        pos_ = pos_+1
    pos_ = 0
    for i in net.getLayerNames():
        #print(f"pos:{pos_}:getLayerNames:{i}")
        pos_ = pos_+1
    output_layers = []

    if os.name != 'nt':
        print("tamos en linus compare")
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    else:
        print("tamos en windors compare")
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()] 


    #print(output_layers)
      # FALLA EN WINDOWS
    # 
    #print(output_layers)

    # Send blob data to forward pass
    outs = net.forward(output_layers)
    #print(outs[0].shape)
    #print(outs[1].shape)
    #print(outs[2].shape)

    # Generating random color for all 80 classes
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Extract information on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            # Extract score value
            scores = detection[5:]
            # Object id
            class_id = np.argmax(scores)
            # Confidence score for each object ID
            confidence = scores[class_id]
            # if confidence > 0.5 and class_id == 0:
            if confidence > 0.5:
                # Extract values to draw bounding box
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # fixed by renest
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))  # fixed

    lista = []

    listaAlturasMedias = {}

    # Draw bounding box with text for each object
    font = cv2.FONT_HERSHEY_DUPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]


            #si tiene una guatones muy grande
            if w>100:
                continue

            label = str(classes[class_ids[i]])
            confidence_label = int(confidences[i] * 100)
            #color = colors[i]
            color_ = colors[i]
            #print("color_caja:" + str(color_))
            elemento = {}
            elemento["tipo"] = label

            if not label in types_:
                continue

            elemento["id_interno"] = str(i)
            elemento["x1"] = x
            elemento["x2"] = x + w
            elemento["y1"] = y
            elemento["y2"] = y + h
            elemento["w"] = w
            elemento["h"] = h
            elemento["marca"] = "EN_DESARROLLO"

            #altura_mitad = int(h/2)
            half_altura = int(h/20)

            clase_H = "H"+str(half_altura)
            elemento["clase_H"] = clase_H

            #elemento["clase_CURVA"] = "CV_1_CV1" #detector de tapas
            elemento["clase_GRUPO_PALETA_2"] = "P_000000" + "invoquepaleta" #2
            elemento["clase_GRUPO_PALETA_3"] = "P_000000" + "invoquepaleta"#3
            elemento["clase_GRUPO_PALETA_4"] = "P_000000" + "invoquepaleta" #4
            elemento["clase_VOLUMEN"] = "V_" + str( (h*w)/20 )
            elemento["altura_media"] = half_altura
            elemento["EAN"] = "NULL"

            #lista["elemento_"+ str(i)] = elemento
            lista.append(elemento)

            colors_TYPE_ = colors_TYPE[half_altura]

            cv2.rectangle(img, (x, y), (x + w, y + h), colors_TYPE_, 2)
#            cv2.putText(img, f'{ "H"+str(half_altura)}',(x-25, y + 75), font, 0.5, colors_TYPE_, 2)
            cv2.putText(img, str(i) ,(x-25, y + 75), font, 0.5, colors_TYPE_, 2)

            # C:\RSILVA_BOT_BASICS\ETL_CADEM\VISION_ARTIFICIAL\DEMO_OBJETOS\PALETA_FILES_5_CLUSTER
            img_sub = img_ORIGINAL_TO_1024[y:y+h, x:x+w]

            img_sub_path = "C:/RSILVA_BOT_BASICS/ETL_CADEM/VISION_ARTIFICIAL/DEMO_OBJETOS/SUB_IMAGENES"
            img_sub_path_paleta = "C:/RSILVA_BOT_BASICS/ETL_CADEM/VISION_ARTIFICIAL/DEMO_OBJETOS/CLUSTERIZAR_PALETA"

            if os.name != 'nt':
                print("tamos en linus compare")
                img_sub_path = "/home/admin/SUB_IMAGENES"

            out_folder_ = src_.replace('.jpg','')           #img_sub_path = "/home/repos/SUB_IMAGENES/"
            img_sub_path = img_sub_path + "/" +     out_folder_ + "/"        #img_sub_path = "/home/repos/SUB_IMAGENES/"

            try:
                os.makedirs( img_sub_path)
            except Exception as ex:
                #print(f"folder ya existe:{img_sub_path}")
                a=0



            img_sub_name = src_ + "_" + elemento["id_interno"] + "_.jpg"


            img_sub_name = str(i) + ".jpg"


            try:
                #print(f"ABORTADO:SUB-IMAGEN:  cv2.imwrite")
                cv2.imwrite(img_sub_path + img_sub_name, img_sub)
                salida_PALETA = __paleta__(img_sub_path, img_sub_name)
                print(f"esta es la salida de Paleta:{salida_PALETA['OUT']}")
                print(f"esta es la salida de COLORES:{salida_PALETA['OUT']}")
                print(f"esta es la salida de COLORES:{salida_PALETA['OUT']}")
                lista["palquelee"] = "palquelee"

                lista["COLOR1"] = "COLOR1"
                lista["COLOR2"] = "COLOR2"
                lista["COLOR3"] = "COLOR3"




            except Exception as ex:
                print(f"Exception in imwrite -  : {ex}")



    if os.name != 'nt':
        print("tamos en linus compare")
        # ESCRIBE LA SALIDA JPG EN EL BUCKET
        image_string = cv2.imencode('.jpg', img)[1].tostring()
        dev_client.put_object(
            Bucket=bucket_name, Key=f"vision_artificial/OUT_{src_}", Body=image_string)

        # ESCRIBE LA SALIDA JSON EN EL BUCKET
        bucket_name = "cadem-vision-artificial-photos"
        nameFile = "entrada.jpg"
        nameJsonFile = "OUT_" + src_ + ".json"
        s3object = dev_resource.Object(
            bucket_name, f"vision_artificial/{nameJsonFile}")

        salida = s3object.put(
            Body=(bytes(json.dumps(lista).encode('UTF-8')))
        )
        print("vamos a escribir un JSON en S3")
        print(f"salida:{salida}")
        print("TERMINO SH")

    else:

        print("VAMOS A ESCRIBIR EL JSON EL LOCAL")

        ruta_OUT = f'{path_}_OUT_BANDEJERO_1024_{src_}'
        print("ruta_OUT:{ruta_OUT}")
        cv2.imwrite(ruta_OUT,img)

        #print(lista)
        print(lista)
        with open("OUT_" + src_ + ".json", "w") as outfile:
            json.dump(lista, outfile, indent = 4)

    salida["lista"] = lista
    return salida

def _RSILVA_20220330_visualize_Dominant_colors__(path_,file_,cluster, C_centroids):
    print(f"_RSILVA_20220330_visualize_Dominant_colors__:path_:{path_}:file_{file_}:cluster:{cluster}")
    salida = {}

    C_labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (C_hist, _) = np.histogram(cluster.labels_, bins=C_labels)
    C_hist = C_hist.astype("float")
    C_hist /= C_hist.sum()

    rect_color = np.zeros((50, 300, 3), dtype=np.uint8)
    img_colors = sorted([(percent, color)
                        for (percent, color) in zip(C_hist, C_centroids)])
    start = 0

    string_COLOR = ""
    string_COLOR_PCT = ""
    pos = 0
    for (percent, color) in img_colors:
        color[0] = int(color[0])
        color[1] = int(color[1])
        color[2] = int(color[2])

        string_COLOR_tmp = str(int(color[0])) + "_" + str(int(color[1])) + "_" + str(int(color[2]))
        string_COLOR = string_COLOR + "_" + string_COLOR_tmp

        string_COLOR_PCT_tmp = str( int(percent*100) ) + "_" + string_COLOR_tmp
        string_COLOR_PCT = string_COLOR_PCT + "_pct_" + string_COLOR_PCT_tmp

        salida["C" + str(pos) + "R"] = color[0]
        salida["C" + str(pos) + "G"] = color[1]
        salida["C" + str(pos) + "B"] = color[2]

        if(pos==3):
            print(f"pos:{pos}, ya compa saulcito:" +string_COLOR_PCT )

        #print(color, "{:0f}%".format(percent * 100))
        #print(color, "{:0f}%".format(percent * 100))

        end = start + (percent * 300)
        cv2.rectangle(rect_color, (int(start), 0), (int(end), 50),
                      color.astype("uint8").tolist(), -1)
        start = end
        pos = pos + 1

    salida["rect_color"] = rect_color
    salida["string_COLOR"] = string_COLOR
    salida["string_COLOR_PCT"] = string_COLOR_PCT

    return salida

def __paleta__(path_, file_):
    print(f"__paleta__:{file_}")
    __clusters__ = 3
    out = {}
    # Load image
    path_file_ = f"{path_}{file_}"
    src_image = cv2.imread(path_file_)

    src_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
    reshape_img = src_image.reshape(
        (src_image.shape[0] * src_image.shape[1], 3))

    # Display dominant colors Present in the image
    KM_cluster = KMeans(n_clusters=__clusters__).fit(reshape_img)
    visualize_color_salida = _RSILVA_20220330_visualize_Dominant_colors__(path_,file_,KM_cluster, KM_cluster.cluster_centers_)

    visualize_color_img = visualize_color_salida["rect_color"]
    visualize_color_img = cv2.cvtColor(visualize_color_img, cv2.COLOR_RGB2BGR)
    string_COLOR = visualize_color_salida["string_COLOR"]

    string_COLOR_PCT = visualize_color_salida["string_COLOR_PCT"]


    out["COLOR1"] = "palquelee"
    out["COLOR2"] = "palquelee"
    out["COLOR3"] = "palquelee"

    #print(f"string_COLOR_PCT:{string_COLOR_PCT}")
    ruta_OUT = f'{path_}{file_}_PALETA_.jpg'
    print(f"ABORTADO:imwrite:visualize_color_img:ruta:{ruta_OUT}:string_COLOR{string_COLOR}")
    cv2.imwrite(ruta_OUT, visualize_color_img)
    out["OUT"] = "test" 
    return out

#testYolo("22032022115408_FOTO_SALA_BUENA.jpg", types_=['bottle'])  #sprite
testYolo("_ELEGIDA_27012022165311_FOTO_SALA_BUENA.jpg", types_=['bottle']) # coca cola


"""

    if os.name != 'nt':
        print("tamos en linus compare")
    else:
        print("tamos en windors compare")
"""