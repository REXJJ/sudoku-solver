import cv2
import numpy as np
import time
import digitidentifier


def processImage(image):
    model=digitidentifier.train()    
    img = cv2.imread(image)
    back=img
    img = cv2.GaussianBlur(img,(5,5),0)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    mask = np.zeros((gray.shape),np.uint8)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))
    close = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel1)
    div = np.float32(gray)/(close)
    res = np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX))
    res2 = cv2.cvtColor(res,cv2.COLOR_GRAY2BGR)
    thresh = cv2.adaptiveThreshold(res,255,0,1,19,2)
    image, contour, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    best_cnt = None
    for cnt in contour:
      area = cv2.contourArea(cnt)
      if area > 1000:
        if area > max_area:
            max_area = area
            best_cnt = cnt
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)
    res = cv2.bitwise_and(res,mask)
    mask = res > 0
    # Coordinates of non-black pixels.
    coords = np.argwhere(mask)
    # Bounding box of non-black pixels.
    x0, y0 = coords.min(axis=0)
    x1, y1 = coords.max(axis=0) + 1   # slices are exclusive at the top
    # Get the contents of the bounding box.
    cropped = res[x0:x1, y0:y1]
    img=cropped
    img2 = img
    height, width = img.shape
    CROP_W_SIZE  = 9 
    CROP_H_SIZE = 9
    sudoku=[];
    count=0
    z=[]
    for ih in range(CROP_W_SIZE):
      for iw in range(CROP_H_SIZE):
        x = int(width/CROP_W_SIZE * iw) 
        y = int(height/CROP_H_SIZE * ih)
        h = int(height / CROP_H_SIZE)
        w = int(width / CROP_W_SIZE )
        #print(x,y,h,w)
        img = img[y+int(h/10):y+int(h)-int(h/10), x+int(w/10):x+int(w)-int(w/10)]
        NAME = "square"+str(ih)+str(iw)
        cv2.imwrite("./CROP/" + NAME +  ".png",img)
        imag=cv2.imread("./CROP/" + NAME +  ".png")
        t=digitidentifier.predictor(imag,model)
        count=count+1;
        z.append(t);
        if count%9==0:
            sudoku.append(z)
            z=[]
        #NAME = str(time.time()) 
        #cv2.imwrite("./CROP/" + str(time.time()) +  ".png",img)
        img = img2
    return sudoku
