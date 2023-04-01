# -*- coding: utf-8 -*-
import cv2
import os
import dlib
import datetime
import uuid
import face_recognition
from PIL import Image, ImageDraw
import numpy as np


# 人脸识别程序
class Face:
    # 定义一个构造方法
    def __init__(self, directory_path, picture_name, save_path):
        # 把外部参数赋值
        self.dir_path = directory_path  # 图片目录
        self.pic_name = picture_name  # 图片名称
        self.save_path = save_path  # 保存路径

    # 使用face_recognition对图片初始化
    @property
    def rec_image_init(self):
        # 加载图片，对图片进行初始化
        # 就把图片转化为像素矩阵
        image = face_recognition.load_image_file(
            os.path.join(
                self.dir_path,
                self.pic_name
            )
        )
        return image

    # 通过openCV读取图片
    @property
    def cv2_image_init(self):
        image = cv2.imread(
            os.path.join(
                self.dir_path,
                self.pic_name
            )
        )
        return image

    # 时间
    @property
    def dt(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # 保存名称定义
    @property
    def image_name(self):
        # 名称构成：时间+唯一字符串
        prefix1 = self.dt
        prefix2 = uuid.uuid4().hex
        return prefix1 + prefix2

    # 保存OpenCV识别结果方法
    def save_cv2_face(self, cv2_image):
        # 如果保存目录不存在，则创建
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # 定义图片完整名称
        filename = "{}.png".format(
            self.image_name
        )
        # 将numpy数组转化为图片
        cv2.imwrite(os.path.join(self.save_path, filename), cv2_image)
        return filename

    # 保存pillow识别结果
    def save_pil_face(self, pil_image):
        # 如果保存目录不存在，则创建
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # 定义图片完整名称
        filename = "{}.png".format(
            self.image_name
        )
        # 保存图片至指定的位置
        pil_image.save(os.path.join(self.save_path, filename), 'png')
        return filename

    # 获取图像中人脸位置
    def get_face_locaions(self):
        image = self.cv2_image_init
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 创建haar级联器对象
        face_cascade = cv2.CascadeClassifier(os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            'static/haarcascades/haarcascade_frontalface_default.xml'
        ))
        faces = face_cascade.detectMultiScale(image, 1.2, 5)
        return image, faces

    # 获取图像中人脸特征
    def get_face_landmarks(self):
        # 初始化
        image = self.rec_image_init
        # 通过特征算法获取所有的特征点
        face_landmarks_list = face_recognition.face_landmarks(image)
        return image, face_landmarks_list

    # 框选人脸
    def face_box(self):
        cv2_image, face_locations = self.get_face_locaions()
        for x, y, w, h in face_locations:
            cv2.rectangle(
                cv2_image,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )
        # 保存图像
        filename = self.save_cv2_face(cv2_image)
        return [filename]

    # 人脸勾勒
    def face_sense(self):
        # 获取图像和人脸特征
        image, face_landmarks_list = self.get_face_landmarks()
        # 定义获取脸部特征的列表，键
        facial_features = [
            'chin',
            'left_eyebrow',
            'right_eyebrow',
            'nose_bridge',
            'nose_tip',
            'left_eye',
            'right_eye',
            'top_lip',
            'bottom_lip'
        ]
        # 将图像转化为图像数组
        pil_image = Image.fromarray(image)
        # 将图像数组转化为可绘制的对象
        draw = ImageDraw.Draw(pil_image)
        # 遍历所有特征点
        for face_landmark in face_landmarks_list:
            # 遍历特征列表
            for facial_feature in facial_features:
                # 绘制描线
                draw.line(face_landmark[facial_feature], width=5, fill=(255, 255, 255))
        # # 显示图像
        # pil_image.show()
        # 保存图像
        filename = self.save_pil_face(pil_image)
        return [filename]

    # 人脸截取
    def face_find(self):
        result = []
        # 获取人脸位置
        image, face_locations = self.get_face_locaions()
        for x, y, w, h in face_locations:
            face_image = image[y:y + h, x:x + w]
            filename = self.save_cv2_face(face_image)
            result.append(
                filename
            )

        return result

    # 获取眼鼻口
    def eye_nose_mouth(self):
        image = self.cv2_image_init
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 创建眼鼻口haar级联器
        eye = cv2.CascadeClassifier(os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            'static/haarcascades/haarcascade_eye.xml'
        ))
        nose = cv2.CascadeClassifier(os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            'static/haarcascades/haarcascade_mcs_nose.xml'
        ))
        mouth = cv2.CascadeClassifier(os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            'static/haarcascades/haarcascade_mcs_mouth.xml'
        ))

        face_eye = eye.detectMultiScale(image, 1.2, 5)
        face_nose = nose.detectMultiScale(image, 1.2, 5)
        face_mouth = mouth.detectMultiScale(image, 1.2, 5)
        return face_eye, face_nose, face_mouth

    # 框选眼鼻口
    def eye_nose_mouth_box(self):
        eye, nose, mouth = self.eye_nose_mouth()
        image, face = self.get_face_locaions()
        for x, y, w, h in face:
            for x, y, w, h in eye:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # for x,y,w,h in nose:
            #     cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            for x, y, w, h in mouth:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        filename = self.save_cv2_face(image)
        return [filename]

    # 人脸68检测点
    def face_68_landmarks(self):
        image = self.cv2_image_init
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 使用dlib自带的frontal_face_detector人脸检测器
        detector = dlib.get_frontal_face_detector()
        # 使用官方模型构建特征提取器
        predictor = dlib.shape_predictor(os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            'static/shape_predictor/shape_predictor_68_face_landmarks.dat'
        ))
        dets = detector(gray, 1)
        for face in dets:
            shape = predictor(image, face)

            # 绘制特征点
            for index, pt in enumerate(shape.parts()):
                pt_pos = (pt.x, pt.y)
                cv2.circle(image, pt_pos, 1, (255, 0, 0), -1)
                # 利用cv2.putText输出1-68
                cv2.putText(image, str(index + 1), pt_pos, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.3, (0, 255, 0), 1,
                            cv2.LINE_AA)

        filename = self.save_cv2_face(image)
        return [filename]

# if __name__ == "__main__":
#     root_path = os.path.dirname(
#         os.path.dirname(__file__)
#     )
#     face = Face(
#         directory_path=os.path.join(root_path,'static/images/exp'),
#         picture_name='g.png',
#         save_path=os.path.join(root_path, 'static/uploads')
#     )
#     face.eye_nose_mouth_box()
# print(face.face_68_landmarks())
#     # image = face.image_init
#     # image,shape = face.get_face_landmarks()
#     # for pt in shape.parts():
#     #     #获取横坐标
#     #     pt_position = (pt.x,pt.y)
#     #     #绘制关键点
#     #     cv2.circle(image,pt_position,1,(0,0,255),-1)
#     # cv2.imshow('image_face_68',image)
#
# faces,image = face.get_face_locaions()
# for (x,y,w,h) in faces:
#     cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
#     cv2.imshow('face_box',face.face_box())
#
