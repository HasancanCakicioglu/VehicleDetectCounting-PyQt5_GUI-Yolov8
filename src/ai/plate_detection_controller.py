import os
from time import sleep

import tensorflow as tf
import numpy as np
import cv2
from easyocr import easyocr


class plateDetectionController:
    model = None
    reader = None

    @classmethod
    def initialize(cls):
        plateDetectionController.reader = easyocr.Reader(['en'])

    @classmethod
    def getInstance(cls, model_path):
        """Singleton örneğini döndürür"""
        if cls.model is None:
            cls(model_path)
        return cls.model

    def __init__(self, model_path):
        """Örnek oluşturma yöntemi"""
        if plateDetectionController.model is not None:
            raise Exception("Bu sınıf Singleton tasarım deseniyle oluşturulmuştur!")
        else:
            plateDetectionController.model = self

        if not os.path.exists(model_path):
            raise ValueError(f"Model path '{model_path}' not found")
        self.__class__.model = tf.saved_model.load(model_path)

    @classmethod
    def predict(cls, image_np,id):

        if 0 in image_np.shape:
            return False, 0, 0, 0, 0, None
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]

        # Modeli kullanarak tahminleri yapın
        output_dict = cls.model(input_tensor)


        # Tahminleri alın
        boxes = output_dict['detection_boxes'][0].numpy()
        classes = output_dict['detection_classes'][0].numpy().astype(np.int32)
        scores = output_dict['detection_scores'][0].numpy()



        # İstenen sınırlar aralığında olan kutuları seçin
        min_score_thresh = 0.70
        selected_indices = np.where(scores > min_score_thresh)
        selected_boxes = boxes[selected_indices]
        selected_classes = classes[selected_indices]

        #print("scores = "+str(scores))
        #print("slected boxes = "+str(selected_boxes))
        #print("slected classes = " + str(selected_classes))
        #print("slected indices = " + str(selected_indices))
        #print("slected indices1 = " + str(selected_indices[0]))
        #if scores[selected_indices[0][0]] is not None:
        #    print("indices2 = " + str(scores[selected_indices[0][0]]))
        there_is = False
        # Seçilen kutuları çizin
        for box, clss ,indi in zip(selected_boxes, selected_classes,selected_indices):
            there_is = True
            ymin, xmin, ymax, xmax = box
            xmin = int(xmin * image_np.shape[1])
            xmax = int(xmax * image_np.shape[1])
            ymin = int(ymin * image_np.shape[0])
            ymax = int(ymax * image_np.shape[0])

            cv2.rectangle(image_np, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)
            ocr_result = plateDetectionController.plate_reader(image_np[ymin:ymax, xmin:xmax])
            print("cls = "+str(clss))
            print("indi = "+str(indi))

            break
        print("scores outside =" + str(selected_indices))
        if there_is and (ocr_result is not None) and (ocr_result!=[]) and (len(ocr_result[0])>1):
            return there_is,xmin, ymin,xmax, ymax,ocr_result
        else:
            there_is = False
        return there_is,0,0,0,0,None

    @classmethod
    def plate_reader(cls, plate):

        ocr_result = plateDetectionController.reader.readtext(plate)
        return ocr_result
