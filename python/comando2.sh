#! /bin/bash
cd /home/repos/VisionArtificialCadem2.0/yolov5
source activate env
python /home/repos/VisionArtificialCadem2.0/yolov5/detect.py /home/admin/SUB_IMAGENES/$1  
