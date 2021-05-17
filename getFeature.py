from facenet_pytorch import MTCNN, InceptionResnetV1

from PIL import Image
import numpy as np
import os

dataset_path = '/home/lss/Desktop/cky/NAN-test/FDDB'

persons = os.listdir(dataset_path)
for person in persons:
    person_path = os.path.join(dataset_path,person)
    
    #actions = os.listdir(person_path)
    #for action in actions:
    action = "r_3"
    action_path = os.path.join(person_path,action)
    print(action_path)
    indexs = os.listdir(action_path)
    for index in indexs:
        img_path = os.path.join(action_path,index)
        save_path = img_path+'.txt'
            
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


