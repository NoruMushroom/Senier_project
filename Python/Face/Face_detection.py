from retinaface import RetinaFace
from retinaface.commons import postprocess
from deepface.commons import functions
import os
import pickle
import cv2
import numpy as np
from keras_preprocessing import image
import pandas as pd
from deepface.commons import distance
import Option
from datetime import datetime
import sys


def face_box(img_path):
    print(sys._getframe().f_code.co_name , str(datetime.now()))
    
    read_img = cv2.imread(img_path) if type(img_path)!=np.ndarray else img_path
    img = cv2.cvtColor(read_img, cv2.COLOR_BGR2RGB)
    faces = RetinaFace.detect_faces(img)
    if type(faces) == dict:
        box, landmarks, score = (faces['face_1']['facial_area'],
                                faces['face_1']['landmarks'],
                                faces['face_1']['score'])
        img = postprocess.alignment_procedure(img, 
                                              landmarks['right_eye'], 
                                              landmarks['left_eye'],
                                              landmarks['nose'])
        img= img[box[1]: box[3], box[0]:box[2]].copy() 
    return img

def ArcFace(img_path, face = False):
    '''
    This function represents facial images as vectors.
    img_path : img_path or image
    face : Face detection
    '''
    print(sys._getframe().f_code.co_name , str(datetime.now()))
    
    from deepface.basemodels import ArcFace
    model = ArcFace.loadModel()
    read_img = cv2.imread(img_path) if type(img_path)!=np.ndarray else img_path
    img = cv2.cvtColor(read_img, cv2.COLOR_BGR2RGB)
    if face:
        faces = RetinaFace.detect_faces(img)
        if type(faces) == dict:
            box, landmarks, score = (faces['face_1']['facial_area'],
                                    faces['face_1']['landmarks'],
                                    faces['face_1']['score'])
            img = postprocess.alignment_procedure(img, landmarks['right_eye'],
                                                  landmarks['left_eye'],
                                                  landmarks['nose'])
            img= img[box[1]: box[3], box[0]:box[2]].copy()

    if img.shape[0] > 0 and img.shape[1] > 0:
        factor_0 = 112 / img.shape[0]
        factor_1 = 112 / img.shape[1]
        factor = min(factor_0, factor_1)

        dsize = (int(img.shape[1] * factor), int(img.shape[0] * factor))
        img = cv2.resize(img, dsize)
        diff_0 = 112 - img.shape[0]
        diff_1 = 112 - img.shape[1]
        img = np.pad(img, ((diff_0 // 2, diff_0 - diff_0 // 2),
                           (diff_1 // 2, diff_1 - diff_1 // 2), (0, 0)), 'constant')

    if img.shape[0:2] != 112:
        img = cv2.resize(img, (112,112))

    img_pixels = image.img_to_array(img)
    img_pixels = np.expand_dims(img_pixels, axis = 0)
    img_pixels /= 255
    img = functions.normalize_input(img = img_pixels,
                                    normalization = "ArcFace")
    embedding = model.predict(img)[0].tolist()
    return embedding
           
def save_pickle():
    
    '''Add the latest face image'''
    print(sys._getframe().f_code.co_name , str(datetime.now()))
    
    with open(r"Python\user_img\NoMask.txt","r") as f:
        lines = f.readlines()
    with open(Option.NOMASK_PKL,"ab") as train:
        lines = [line.rstrip('\n') for line in lines]
        if lines != []:
            for i in lines:
                embedding = ArcFace(i)
                pickle.dump([i, embedding], train)
                
    with open(r"Python\user_img\Mask.txt","r") as f:
        lines = f.readlines()
    with open(Option.MASK_PKL,"ab") as train:
        lines = [line.rstrip('\n') for line in lines]
        if lines != []:
            for i in lines:
                embedding = ArcFace(i)
                pickle.dump([i, embedding], train)  
                  
    with open(r"Python\user_img\NoMask.txt",'w',encoding='UTF-8') as f:
            pass
    with open(r"Python\user_img\Mask.txt",'w',encoding='UTF-8') as f:
            pass
        
        
def save_image(id, img, img_db):

    print(sys._getframe().f_code.co_name , str(datetime.now()))
    
    path = os.path.join(img_db,id)
    save_path = ""
    for (root, directories, files) in os.walk(path):
        for file in files:
            if '.jpg' in file:
                save_path = os.path.join(root, file)
    if save_path == "":
        save_path =  os.path.join(f"{path}/", str(id) + "_001.jpg" )
        

    number = os.path.basename(save_path)
    number = int(number[-7:-4]) + 1
    number = format(number, '03')
    # dir , studentID + _ + number + extension
    save_path = os.path.join(os.path.dirname(save_path),
                            os.path.basename(save_path)[0:8] + "_" + number + os.path.splitext(save_path)[1])
    save_path = save_path.replace("\\", "/")
    cv2.imwrite(save_path, img)                
    save_list(save_path)
    
    
        
def save_list(path:str):
    ''' Insert attendance completed face image '''
    
    print(sys._getframe().f_code.co_name , str(datetime.now()))
    
    if "NoMask" in path:
        with open(r"Python\user_img\NoMask.txt",'a',encoding='UTF-8') as f:
                f.write(path +'\n')
    else: 
        with open(r"Python\user_img\Mask.txt",'a',encoding='UTF-8') as ff:
                ff.write(path +'\n') 
             
def exists_Pickle(): 
    ''' Create a pickle file if it does not exist '''
    
    print(sys._getframe().f_code.co_name , str(datetime.now()))
    
    if not os.path.exists(Option.MASK_PKL):
        with open(Option.MASK_PKL,"wb") as a:
            pass
    if not os.path.exists(Option.NOMASK_PKL):
        with open(Option.NOMASK_PKL,"wb") as b:
            pass
            
def save_masked_image(path_list:list,face = False):
    '''
    Cover the underside of the nose from the face bounding box using a white box
    
    list = ```image path(Just the face)```
    '''
    print(sys._getframe().f_code.co_name , str(datetime.now()))
    
    for path in path_list:    
        maskedImagePath = ""
        studentID = os.path.basename(path)[0:8]
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if face:
            faces = RetinaFace.detect_faces(img)
            if type(faces) == dict:
                box, landmarks, score = (faces['face_1']['facial_area'],
                                        faces['face_1']['landmarks'],
                                        faces['face_1']['score'])
                
                img = postprocess.alignment_procedure(img, landmarks['right_eye'],
                                                    landmarks['left_eye'],
                                                    landmarks['nose'])
                img= img[box[1]: box[3], box[0]:box[2]].copy()
            
        cv2.rectangle(img, (0, img.shape[0]//2), (img.shape[1],img.shape[0]), color=(255, 255, 255), thickness=-1)
        for (root, directories, files) in os.walk(f"{Option.MASK_PATH}/{studentID}"):
            for file in files:
                if '.jpg' in file:
                    maskedImagePath = os.path.join(root, file)
                    
        if maskedImagePath == "":
            maskedImagePath =  os.path.join(f"{Option.MASK_PATH}/{studentID}",
                                            str(studentID) + "_001.jpg" )
        

        number = os.path.basename(maskedImagePath)
        number = int(number[-7:-4]) + 1
        number = format(number, '03')
        # dir , studentID + _ + number + extension
        savePath = os.path.join(os.path.dirname(maskedImagePath),
                                os.path.basename(maskedImagePath)[0:8] + "_" + 
                                number + os.path.splitext(maskedImagePath)[1])
        savePath = savePath.replace("\\", "/")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(savePath, img)
        
        embedding = ArcFace(img)
        with open(Option.MASK_PKL ,"ab") as f:
            pickle.dump( [savePath, embedding], f)   
        
        
        
def recognition(img_path: str, pkl_file:str, reference_value: float):
    
    print(sys._getframe().f_code.co_name , str(datetime.now()))
    
    read_img = cv2.imread(img_path) if type(img_path)!=np.ndarray else img_path
    img = cv2.cvtColor(read_img, cv2.COLOR_BGR2RGB)
    target_embedding = ArcFace(img)
    pkl_data = list()

    with open(pkl_file,'rb') as f:
        while True:
            try: pkl_data.append(pickle.load(f))
            except:
                f.close()
                break
            
    if pkl_data == []:
        return None
        
    df = pd.DataFrame(columns=['StudentID', 'distance'])
    test = []
    for i in pkl_data:
        if i == []: continue
        if len(df) > 9:
            break
        dis = distance.findCosineDistance(target_embedding,i[1])
        if dis < reference_value and test.count(os.path.basename(i[0])[:8]) < 3:
            df.loc[len(df)+1] = [os.path.basename(i[0])[:12],dis]
            test.append(os.path.basename(i[0])[:8])
    
    if len(df) == 0:
        return None
        
    df = df.sort_values(by = 'distance',ignore_index=True)

    test_dict = dict()
    for id in set(test):
        r =df[df['StudentID'].str.contains(id)]
        test_dict[id] = sum(r.index)+1

    top = [k for k, v in test_dict.items() if v == min(test_dict.values())]

    if len(top) > 1:
        rating = df[df['StudentID'].str.contains(top.pop())].iloc[0]
        for c in top:
            if rating[1] > df[df['StudentID'].str.contains(c)].iloc[0][1]:
                rating =  df[df['StudentID'].str.contains(c)].iloc[0]
    else:
        rating = df[df['StudentID'].str.contains(top.pop())].iloc[0]
    
    return rating[0][:8]


