import cv2
import os

def getFilePathList(path, filetype):
    pathList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(filetype):
                pathList.append(os.path.join(root, file))
    return pathList

path = getFilePathList('/home/lss/Desktop/cky/PRNet/TestImages/results','mat')
for mat in path:
    start = mat.find('img') + 4
    end = mat.find('mash') - 1
    obj = mat[start:end]
    dir1 = '/home/lss/Desktop/cky/NAN-test/FDDB/'+obj
    imglist = getFilePathList(dir1 + "/l2r",'jpg')
    for image in imglist:
        img=cv2.imread(image)
        imgrot = cv2.flip(img, 0)
        cv2.imwrite(image,imgrot)
    imglist = getFilePathList(dir1 + "/u2d",'jpg')
    for image in imglist:
        img=cv2.imread(image)
        imgrot = cv2.flip(img, 0)
        cv2.imwrite(image,imgrot)
    imglist = getFilePathList(dir1 + "/r_1",'jpg')
    for image in imglist:
        img=cv2.imread(image)
        imgrot = cv2.flip(img, 0)
        cv2.imwrite(image,imgrot)
    imglist = getFilePathList(dir1 + "/r_2",'jpg')
    for image in imglist:
        img=cv2.imread(image)
        imgrot = cv2.flip(img, 0)
        cv2.imwrite(image,imgrot)
    imglist = getFilePathList(dir1 + "r_3",'jpg')
    for image in imglist:
        img=cv2.imread(image)
        imgrot = cv2.flip(img, 0)
        cv2.imwrite(image,imgrot)