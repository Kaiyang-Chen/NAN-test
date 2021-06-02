import os, sys
import cv2
import glob
import numpy as np
import math
import scipy.io as sio
from skimage import io
from time import time
import subprocess
from PIL import Image
sys.path.append('..')
import face3d
from face3d import mesh
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image



def getFilePathList(path, filetype):
    pathList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(filetype):
                pathList.append(os.path.join(root, file))
    return pathList


def transform_test(vertices, obj, camera, h = 256, w = 256):
	'''
	Args:
		obj: dict contains obj transform paras
		camera: dict contains camera paras
	'''
	R = mesh.transform.angle2matrix(obj['angles'])
	transformed_vertices = mesh.transform.similarity_transform(vertices, obj['s'], R, obj['t'])
	
	if camera['proj_type'] == 'orthographic':
		projected_vertices = transformed_vertices
		image_vertices = mesh.transform.to_image(projected_vertices, h, w)
	else:

		## world space to camera space. (Look at camera.) 
		camera_vertices = mesh.transform.lookat_camera(transformed_vertices, camera['eye'], camera['at'], camera['up'])
		## camera space to image space. (Projection) if orth project, omit
		projected_vertices = mesh.transform.perspective_project(camera_vertices, camera['fovy'], near = camera['near'], far = camera['far'])
		## to image coords(position in image)
		image_vertices = mesh.transform.to_image(projected_vertices, h, w, True)

	rendering = mesh.render.render_colors(image_vertices, triangles, colors, h, w)
	rendering = np.minimum((np.maximum(rendering, 0)), 1)
	return rendering


def get_pic(mat_path, save_path):
    # --------- load mesh data
    path = getFilePathList(mat_path,'mat')
    for mat in path:
        C = sio.loadmat(mat)
        start = mat.find('img') + 4
        end = mat.find('mash') - 1
        object = mat[start:end]
        vertices = C['vertices']
        colors = C['colors']
        triangles = C['triangles']
        colors = colors/np.max(colors)
        # move center to [0,0,0]
        vertices = vertices - np.mean(vertices, 0)[np.newaxis, :]

        # save folder
        save_folder = os.path.join(save_path, object)
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        options = '-delay 10 -loop 0 -layers optimize' # gif options. need ImageMagick installed.

        # ---- start
        obj = {}
        camera = {}
        ### face in reality: ~18cm height/width. set 180 = 18cm. image size: 256 x 256
        scale_init = 180/(np.max(vertices[:,1]) - np.min(vertices[:,1])) # scale face model to real size

        ## 1. fix camera model(stadard camera& orth proj). change obj position.
        camera['proj_type'] = 'orthographic'

        # angles
        i = 1
        angles = [-30,30]
        for angle in angles:
            obj['s'] = scale_init*i
            obj['angles'] = [0, 0, 0]
            obj['angles'][0] = angle
            obj['angles'][1] = 0
            obj['t'] = [0, 0, 0]
            image = transform_test(vertices, obj, camera) 
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            image_name = '{}/{}.jpg'.format(save_folder, angle)
            io.imsave(image_name, image)

def get_feature(dataset_path):
    persons = os.listdir(dataset_path)
    for person in persons:
        person_path = os.path.join(dataset_path,person)
        
        indexs = os.listdir(person)
        for index in indexs:
            img_path = os.path.join(person,index)
            save_path = img_path[:-4]+'.txt'
                
            # If required, create a face detection pipeline using MTCNN:
            mtcnn = MTCNN(image_size=240)

            # Create an inception resnet (in eval mode):
            resnet = InceptionResnetV1(pretrained='vggface2').eval()

            img = Image.open(img_path)

            # Get cropped and prewhitened image tensor
            img_cropped = mtcnn(img)
            if img_cropped is None:
                os.remove(img_path)
            else:
            # Calculate embedding (unsqueeze to add batch dimension)
                img_embedding = resnet(img_cropped.unsqueeze(0))
                features = img_embedding.detach().numpy()
                np.savetxt(save_path,features)


if __name__ == '__main__':
    get_pic('/home/lss/Desktop/cky/PRNet/TestImages/results','/home/lss/Desktop/cky/NAN-test/correlation')
    get_feature('/home/lss/Desktop/cky/NAN-test/correlation')