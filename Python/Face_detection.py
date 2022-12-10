from retinaface import RetinaFace
from retinaface.commons import postprocess
from deepface import DeepFace
from deepface.commons import functions
import os
import pickle
import __default__ as default
import cv2
import numpy as np
from keras_preprocessing import image
#------------------------

mask_file_patha = ""
embedding_list_No = []
file_list = []
count = 0
embedding_list = []
#------------------------
down = 0.35
up = 0.05
embedding_list_Ma = []
fail_count = 0                           

def face_box(img_path):
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
    print("파일 추가중입니다.")
    with open(default.PKL_NoMask_Path,"wb") as m:
        pkl_m= pickle.load(m)
    with open(default.PKL_NoMask_Path,"wb") as n:
        pkl_n= pickle.load(n)
    with open("NoMask.txt") as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    for i in lines:
        embedding = ArcFace(i)
        pkl_n.append([i, embedding])
    with open(default.PKL_NoMask_Path,"ab") as train:
        pickle.dump(pkl_n, train)
    
    with open("Mask.txt") as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    for i in lines:
        embedding = ArcFace(i)
        pkl_m.append([i, embedding])
    with open(default.PKL_Mask_Path,"ab") as train:
        pickle.dump(pkl_m, train)    
            
    print("파일 추가 완료")
    with open('NoMask.txt','w',encoding='UTF-8') as f:
            pass
    with open('Mask.txt','w',encoding='UTF-8') as f:
            pass
        
def save_image(id, img, img_db):
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
    if "NoMask" in path:
        with open('NoMask.txt','a',encoding='UTF-8') as f:
                f.write(path +'\n')
    else: 
        with open('Mask.txt','a',encoding='UTF-8') as ff:
                ff.write(path +'\n') 
             
def exists_Pickle(): 
    ''' Create a pickle file if it does not exist '''
    if not os.path.exists(default.PKL_Mask_Path):
        with open(default.PKL_Mask_Path,"wb") as a:
            pickle.dump([], a)
    if not os.path.exists(default.PKL_NoMask_Path):
        with open(default.PKL_NoMask_Path,"wb") as b:
            pickle.dump([], b)

            
def save_masked_image(path_list:list):
    '''
    Cover the underside of the nose from the face bounding box using a white box
    
    list = ```image path(Just the face)```
    '''
    with open(default.PKL_Mask_Path ,"rb") as r:
        pkl = pickle.load(r)
    
    for path in path_list:    
        maskedImagePath = ""
        studentID = os.path.basename(path)[0:8]
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        '''
        faces = RetinaFace.detect_faces(img) 
        if type(faces) == dict:
                box, landmarks, score = (faces['face_1']['facial_area'],
                                        faces['face_1']['landmarks'],
                                        faces['face_1']['score'])
        else:
            box, landmarks, score = [], [], 0        
            print("face not found")
            return
            
            
        img = postprocess.alignment_procedure(img, landmarks['right_eye'], landmarks['left_eye'],landmarks['nose'])
        img= img[box[1]: box[3], box[0]:box[2]].copy()
        '''
        
        cv2.rectangle(img, (0, img.shape[0]//2), (img.shape[1],img.shape[0]), color=(255, 255, 255), thickness=-1)
        for (root, directories, files) in os.walk(f"{default.Mask_DB_Path}/{studentID}"):
            for file in files:
                if '.jpg' in file:
                    maskedImagePath = os.path.join(root, file)
                    
        if maskedImagePath == "":
            maskedImagePath =  os.path.join(f"{default.Mask_DB_Path}/{studentID}",
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
        user_list = [savePath,embedding]
        pkl.append(user_list)
    with open(default.PKL_Mask_Path ,"wb") as w:
        pickle.dump(pkl, w)   
        
        
        
def recognition(img, box, img_db):
    Rdict = DeepFace.find(img_path=img, 
                          db_path=img_db,
                          enforce_detection=False,
                          model_name ='ArcFace',
                          detector_backend='retinaface')
    if len(Rdict) != 0:
        studentID = os.path.basename(Rdict.iloc[0]['identity'])
        studentID = studentID[0:8]
        return studentID
    else:
        return None        
        
exists_Pickle()
