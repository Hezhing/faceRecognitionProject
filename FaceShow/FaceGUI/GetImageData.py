import os
import re
import cv2
import time
import numpy as np
from PIL import Image
import face_recognition


# 获取KnownFace目录下的所有文件名
def GetImage():
    names = []
    file_dir = "KnownFace"
    for root, dirs, files in os.walk(file_dir):
        names = files
    return names

# 获取KnownFace目录下的所有图片
def GetKnownImageLocations(names):
    print('获取所有已知人脸数据...')
    images = []
    for i in range(len(names)):
        name = names[i]
        filename = 'KnownFace/' + name
        image = cv2.imread(filename)
        face_locations = face_recognition.face_locations(image)
        # print(face_locations)
        images.append(image)
    return images

# 获取UnknownFace目录下的所有图片和图片名称
def GetUnknownImageLocations():
    print('获取所有未知的人脸数据...')
    unknown_images = []
    unknown_image_filenames = []

    for root, dirs, files in os.walk('UnknownFace'):
        unknown_image_filenames = files

    for unname in range(len(unknown_image_filenames)):

        filename = 'UnknownFace/' + unknown_image_filenames[unname]
        unknown_image = face_recognition.load_image_file(filename)
        img_resized1 = cv2.resize(unknown_image, None, fx=1.5, fy=2, interpolation=cv2.INTER_AREA)
        img_resized = cv2.resize(img_resized1, None, fx=2, fy=1.5, interpolation=cv2.INTER_AREA)
        face_locations = face_recognition.face_locations(img_resized)
        if len(face_locations) == 0:
            img_resized = cv2.resize(img_resized1, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
        face_locations = face_recognition.face_locations(img_resized)
        unknown_images.append(img_resized)
    return unknown_images ,unknown_image_filenames

# 获取人脸数据，数据类型为矩阵
def GetFaceEncodings(images ,unknown_images):
    print('将图片转化为矩阵数据中...')
    face_encodings = []
    for image in images:
        encoding = face_recognition.face_encodings(image)[0]
        face_encodings.append(encoding)

    unknown_face_encodings = []
    for unknown_image in unknown_images:
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        unknown_face_encodings.append(unknown_face_encoding)

    return face_encodings ,unknown_face_encodings

# 保存人脸数据
def SaveFaceData(face_encodings ,unknown_face_encodings):
    print('保存人脸数据中...')
    for i in range(len(face_encodings)):
        face_encoding = face_encodings[i]
        Face_csv_flieName = 'KnownFaceData' + '/' + 'Knownface' + str(i) + '.csv'
        np.savetxt(Face_csv_flieName ,face_encoding ,delimiter=',')

    for i in range(len(unknown_face_encodings)):
        unknown_face_encoding = unknown_face_encodings[i]
        UnknownFace_csv_fileName = 'UnknownFaceData' + '/' + 'UnknownFace' + str(i) + '.csv'
        np.savetxt(UnknownFace_csv_fileName ,unknown_face_encoding ,delimiter=',')

# 加载人脸数据
def LoadFaceData(csv_flieName):
    face_encoding = np.loadtxt(open(csv_flieName ,'rb') ,delimiter=',' ,skiprows=0)
    return face_encoding

# 比较人脸相似度
def CompareFace(face_encodings,names,unknown_face_encodings):
    print('载入人脸数据中...')
    print('人脸识别中...')
    OutImageName = {}

    for i in range(len(face_encodings)):
        Face_csv_flieName = 'KnownFaceData' + '/' + 'Knownface' + str(i) + '.csv'
        face_encoding = LoadFaceData(Face_csv_flieName)
        for j in range(len(unknown_face_encodings)):
            UnknownFace_csv_fileName = 'UnknownFaceData' + '/' + 'UnknownFace' + str(j) + '.csv'
            unknown_face_encoding = LoadFaceData(UnknownFace_csv_fileName)

            results = face_recognition.compare_faces([face_encoding], unknown_face_encoding ,tolerance=0.45)
            for k in results:
                if k == True:
                    OutImageName[j] = names[i]
    return OutImageName

# 输出比较结果
def PrintResult(OutImageName ,unknown_image_filenames):
    for i in OutImageName:
        OutImageName[i] = re.sub(r'.jpg|.png' ,"" ,OutImageName[i])
        print("The name of the {} is:{}".format(unknown_image_filenames[i] ,OutImageName[i]))

# 保存未知图片（已切割）
def saveUnknownFace(img_path):
    print('保存已切割的未知图片...')
    image_dir = img_path
    img = face_recognition.load_image_file(image_dir)
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_AREA)
    resized = img
    Unknown_images = []

    face_locations = face_recognition.face_locations(img)
    faceNum = len(face_locations)
    for i in range(faceNum):
        top = face_locations[i][0]
        right = face_locations[i][1]
        bottom = face_locations[i][2]
        left = face_locations[i][3]

        face_image = resized[top - 10:bottom + 10, left - 10:right + 10]
        Unknown_images.append(face_image)
        pil_image = Image.fromarray(face_image)
        image_dir = os.path.split(image_dir)[1]
        save_names = re.sub(r'.jpg|.png', "", image_dir)
        save_name = re.sub(r'UnknownImage/', "", save_names)
        pil_image.save("UnknownFace/" + save_name + '_' + str(i) + ".jpg", quality=100)

# 保存结果图片
def showFaceRead(img_path):
    timeStart = time.clock()
    names = GetImage()
    images = GetKnownImageLocations(names)

    known_face_encodings = []
    for image in images:
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)

    image_dir = img_path
    print("文件路径:{}".format(image_dir))

    # 读取图片并定位
    img = face_recognition.load_image_file(image_dir)
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_AREA)

    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img,face_locations)

    time_1 = time.clock()
    timeRec = time_1 - timeStart
    print("识别时间：", timeRec)

    # 调用opencv显示人脸
    image = cv2.imread(image_dir)

    print("I found {} face(s) in this photograph.".format(len(face_locations)))

    for (top,right,bottom,left),face_encoding in zip(face_locations,face_encodings):

        matches = face_recognition.compare_faces(known_face_encodings,face_encoding,tolerance=0.445)
        name = 'Unknown'

        for index, value in enumerate(matches):
            if value == True:
                match_index = index
                name = names[match_index]


        print(
            "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                  right))

        start = (int(left / 1.5), int(top / 1.5))
        end = (int(right / 1.5), int(bottom / 1.5))

        color = (55, 255, 155)
        thickness = 2
        cv2.rectangle(image, start, end, color, thickness)


        name = re.sub(r'.jpg|.png', "", name)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (int(left / 1.5), int(bottom / 1.5)), font, 0.5, (255, 0, 0), 1)

    cv2.imwrite("KnownImage/" + "KnownImage.jpg", image)
    time_2 = time.clock()
    timeDraw = time_2 - time_1
    print("画出位置时间：", timeDraw)

# 主函数
def Main(img_path):
    names = []
    dirs = ['UnknownFace','UnknownFaceData','KnownFaceData','KnownImage']
    for i in dirs:
        if not os.path.exists(i):
            os.makedirs(i)
    for i,num in enumerate(os.listdir('UnknownFace')):
        reMatch = '_' + str(i) + '.jpg' + '|_' + str(i) + '.png'
        names.append(re.sub(reMatch, "", num))
    fileName = re.sub(r'.jpg|.png',"",os.path.split(img_path)[1])

    if os.listdir('UnknownFaceData') and os.listdir('KnownFaceData') and fileName in names:
        showFaceRead(img_path)
    else:
        names = GetImage()
        images = GetKnownImageLocations(names)
        saveUnknownFace(img_path)
        unknown_images, unknown_image_filenames = GetUnknownImageLocations()
        face_encodings, unknown_face_encodings = GetFaceEncodings(images, unknown_images)
        SaveFaceData(face_encodings, unknown_face_encodings)
        OutImageName = CompareFace(face_encodings, names, unknown_face_encodings)
        showFaceRead(img_path)
        PrintResult(OutImageName, unknown_image_filenames)
