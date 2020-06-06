#for crawler
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import requests
import shutil
import os
import validators
from selenium import webdriver
#for yolo 
from PIL import Image
from ctypes import *
import math
import random
import os
import cv2
import glob
from shutil import copyfile, copy
from en_bayes import *
#for popup window
import tkinter as tk
from tkinter import messagebox

######################################################################################################
#bayes_vn def
# -*- coding: utf-8 -*-
import os
import codecs
import numpy as np

def word(str):
    a=0
    if type(str)!=type(u""):
        try:
            str=unicode(str,"utf-8")
        except:
            return ""        
    str=str.strip()
    str=str.lower()
    S='~`@#%^&*()/,<>?.0123456789!:;-" '
    for c in S:
        if c=="_":
            a+=1
        str=str.replace(c,'')
    str=str.strip()
    if len(str)<2:
        return ""
    if a>1:
        str="" # khong xet nhung cum tu nhieu hon 2 tu
    if str[0]=="_":
        str=str[1:]
    if str[len(str)-1]=="_":
        str=str[:len(str)-1]  
   
    return str


lines=codecs.open("TextsProcess/vn.NaiveBayes/stopword.txt","r","utf-8").readlines()
stopword=[]
for line in lines:
    w=word(line)
    stopword.append(w)


class vn_Bayes:
    def __init__(self):        
        self.negwords=0
        self.poswords=0
        self.negDict=dict()
        self.posDict=dict()
        self.totalV=0
        self.negfiles=0
        self.posfiles=0
        self.negProb=0.
        self.posProb=0.
        self.negProbDict=dict()
        self.posProbDict=dict()  
        self.posP=0.
        self.negP=0.
        self.wd=dict()
        self.listWords=[]
        
    def train_model(self,TrainFile,negPath,posPath,Threshold):
        #tot========================================================
        files=os.listdir(negPath)        
        for file in files:
            fi=os.path.join(negPath,file)
            try:
                f=codecs.open(fi,"r","utf-8")
            except:
                continue
            self.negfiles+=1
            lines=f.readlines()            
            for line in lines:
                listword=line.split(" ")
                for w in listword:
                    w=word(w)
                    if len(w)<2:
                        continue
                    if w in stopword:
                        continue
                    
                    self.wd[w]=1
                    if w not in self.posDict:
                        self.posDict[w]=0
                        
                    if w not in self.negDict:
                        self.negDict[w]=1
                    else:
                        self.negDict[w]+=1
                    
        #Xau========================================================
        files=os.listdir(posPath)        
        for file in files:
            fi=os.path.join(posPath,file)
            try:
                f=codecs.open(fi,"r","utf-8")
            except:
                continue
            self.posfiles+=1
            lines=f.readlines()            
            for line in lines:
                listword=line.split(" ")
                for w in listword:
                    w=word(w)
                    if len(w)<2:
                        continue
                    if w in stopword:
                        continue
                    
                    self.wd[w]=1
                    if w not in self.negDict:
                        self.negDict[w]=0
                       
                    if w not in self.posDict:
                        self.posDict[w]=1
                    else:
                        self.posDict[w]+=1
        
        out=open(TrainFile,'w')
        # out.write(codecs.BOM_UTF8)
        out.write("files" + "," + str(self.negfiles) + "," + str(self.posfiles) + "\n" )
        for w in self.wd:
            if self.negDict[w]+self.posDict[w]>=Threshold:
                out.write(w+","+str(self.negDict[w])+","+str(self.posDict[w])+"\n")
        out.close()
    
        
    def load_model(self, trainmodelfile):
        self.vocabulary=[]
        self.trainmodelfile=trainmodelfile
        lines=open( self.trainmodelfile).readlines()
        i=0        
        for line in lines:
            i+=1
            if i==1:
                x=line.split(",")
                self.negfiles=int(x[1])
                self.posfiles=int(x[2])
                continue
            
            x=line.split(",")
            w=str(x[0])         
            self.vocabulary.append(w)
            self.negProbDict[w]=float(x[1])
            self.posProbDict[w]=float(x[2])
            self.negwords+=self.negProbDict[w]
            self.poswords+=self.posProbDict[w]
            
        
                          
    def classifier(self, TextFile):        
        lines=codecs.open(TextFile,"rb","utf-8").readlines()
        self.listWords=[]
        bfw=""
        for line in lines:
            nwords=line.split(" ")                             
            for i in range(len(nwords)-1):
                if 0<len(nwords)<2:                    
                    w=word(nwords[0])                
                    if len(w)>1 and (w in self.vocabulary):
                        
                        if w not in self.listWords:
                            self.listWords.append(w)
                else:
                    w1=word(nwords[i])
                    w2=word(nwords[i+1])
                    w=w1+"_"+w2                    
                    if len(w1)>1 and (w1 in self.vocabulary):
                        if w1 not in self.listWords:
                            self.listWords.append(w1)
                    if len(w)>1 and (w in self.vocabulary):                        
                        if w not in self.listWords:
                            self.listWords.append(w)

        p0=0.
        p1=0.       
        for w in self.listWords:
            p0+=np.log((self.negProbDict[w]+1.)/(self.negwords+len(self.vocabulary)))
            p1+=np.log((self.posProbDict[w]+1.)/(self.poswords+len(self.vocabulary)))

        p0+=np.log(self.negfiles*1./(self.negfiles+self.posfiles))
        p1+=np.log(self.posfiles*1./(self.negfiles+self.posfiles))
        if len(self.listWords)==0:
            return 0
        if p1>p0:
            return 1
        return 0
    
    def online_classifier(self, PlainText):
        
        self.listWords=[]
        bfw=u"00"
        for x in PlainText.split(" "):
            w=word(x)
            if len(w)<2:
                continue
           
            if (w in self.vocabulary):     
                if w not in self.listWords:
                    self.listWords.append(w)
            
            bfw=w
            w=bfw+"_"+w
            if (w in self.vocabulary):
                if w not in self.listWords:
                    self.listWords.append(w)
            
                    
        p0=0.
        p1=0. 
        
        for w in self.listWords:
            
            p0+=np.log((self.negProbDict[w]+1.)/(self.negwords+len(self.vocabulary)))
            p1+=np.log((self.posProbDict[w]+1.)/(self.poswords+len(self.vocabulary)))
            print(w,self.negProbDict[w],self.posProbDict[w])
        p0+=np.log(self.negfiles*1./(self.negfiles+self.posfiles))
        p1+=np.log(self.posfiles*1./(self.negfiles+self.posfiles))
        
        if len(self.listWords)==0:
            return 0
        if p1>p0:
            return 1
        return 0

#yolo def
def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int),
                ("uc", POINTER(c_float)),
                ("points", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]



#lib = CDLL("/home/pjreddie/documents/darknet/libdarknet.so", RTLD_GLOBAL)
# lib = CDLL("libdarknet.so", RTLD_GLOBAL)
hasGPU = True
if os.name == "nt":
    cwd = os.path.dirname(__file__)
    os.environ['PATH'] = cwd + ';' + os.environ['PATH']
    winGPUdll = os.path.join(cwd, "yolo_cpp_dll.dll")
    winNoGPUdll = os.path.join(cwd, "yolo_cpp_dll_nogpu.dll")
    envKeys = list()
    for k, v in os.environ.items():
        envKeys.append(k)
    try:
        try:
            tmp = os.environ["FORCE_CPU"].lower()
            if tmp in ["1", "true", "yes", "on"]:
                raise ValueError("ForceCPU")
            else:
                print("Flag value '"+tmp+"' not forcing CPU mode")
        except KeyError:
            # We never set the flag
            if 'CUDA_VISIBLE_DEVICES' in envKeys:
                if int(os.environ['CUDA_VISIBLE_DEVICES']) < 0:
                    raise ValueError("ForceCPU")
            try:
                global DARKNET_FORCE_CPU
                if DARKNET_FORCE_CPU:
                    raise ValueError("ForceCPU")
            except NameError:
                pass
            # print(os.environ.keys())
            # print("FORCE_CPU flag undefined, proceeding with GPU")
        if not os.path.exists(winGPUdll):
            raise ValueError("NoDLL")
        lib = CDLL(winGPUdll, RTLD_GLOBAL)
    except (KeyError, ValueError):
        hasGPU = False
        if os.path.exists(winNoGPUdll):
            lib = CDLL(winNoGPUdll, RTLD_GLOBAL)
            print("Notice: CPU-only mode")
        else:
            # Try the other way, in case no_gpu was
            # compile but not renamed
            lib = CDLL(winGPUdll, RTLD_GLOBAL)
            print("Environment variables indicated a CPU run, but we didn't find `"+winNoGPUdll+"`. Trying a GPU run anyway.")
else:
    lib = CDLL("./libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

copy_image_from_bytes = lib.copy_image_from_bytes
copy_image_from_bytes.argtypes = [IMAGE,c_char_p]

def network_width(net):
    return lib.network_width(net)

def network_height(net):
    return lib.network_height(net)

predict = lib.network_predict_ptr
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

if hasGPU:
    set_gpu = lib.cuda_set_device
    set_gpu.argtypes = [c_int]

init_cpu = lib.init_cpu

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int), c_int]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict_ptr
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

load_net_custom = lib.load_network_custom
load_net_custom.argtypes = [c_char_p, c_char_p, c_int, c_int]
load_net_custom.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

predict_image_letterbox = lib.network_predict_image_letterbox
predict_image_letterbox.argtypes = [c_void_p, IMAGE]
predict_image_letterbox.restype = POINTER(c_float)

def array_to_image(arr):
    import numpy as np
    # need to return old values to avoid python freeing memory
    arr = arr.transpose(2,0,1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
    data = arr.ctypes.data_as(POINTER(c_float))
    im = IMAGE(w,h,c,data)
    return im, arr

def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        if altNames is None:
            nameTag = meta.names[i]
        else:
            nameTag = altNames[i]
        res.append((nameTag, out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res

def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45, debug= False):
    """
    Performs the meat of the detection
    """
    #pylint: disable= C0321
    im = load_image(image, 0, 0)
    if debug: print("Loaded image")
    ret = detect_image(net, meta, im, thresh, hier_thresh, nms, debug)
    free_image(im)
    if debug: print("freed image")
    return ret

def detect_image(net, meta, im, thresh=.5, hier_thresh=.5, nms=.45, debug= False):
    #import cv2
    #custom_image_bgr = cv2.imread(image) # use: detect(,,imagePath,)
    #custom_image = cv2.cvtColor(custom_image_bgr, cv2.COLOR_BGR2RGB)
    #custom_image = cv2.resize(custom_image,(lib.network_width(net), lib.network_height(net)), interpolation = cv2.INTER_LINEAR)
    #import scipy.misc
    #custom_image = scipy.misc.imread(image)
    #im, arr = array_to_image(custom_image)		# you should comment line below: free_image(im)
    num = c_int(0)
    if debug: print("Assigned num")
    pnum = pointer(num)
    if debug: print("Assigned pnum")
    predict_image(net, im)
    letter_box = 0
    #predict_image_letterbox(net, im)
    #letter_box = 1
    if debug: print("did prediction")
    #dets = get_network_boxes(net, custom_image_bgr.shape[1], custom_image_bgr.shape[0], thresh, hier_thresh, None, 0, pnum, letter_box) # OpenCV
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum, letter_box)
    if debug: print("Got dets")
    num = pnum[0]
    if debug: print("got zeroth index of pnum")
    if nms:
        do_nms_sort(dets, num, meta.classes, nms)
    if debug: print("did sort")
    res = []
    if debug: print("about to range")
    for j in range(num):
        if debug: print("Ranging on "+str(j)+" of "+str(num))
        if debug: print("Classes: "+str(meta), meta.classes, meta.names)
        for i in range(meta.classes):
            if debug: print("Class-ranging on "+str(i)+" of "+str(meta.classes)+"= "+str(dets[j].prob[i]))
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                if altNames is None:
                    nameTag = meta.names[i]
                else:
                    nameTag = altNames[i]
                if debug:
                    print("Got bbox", b)
                    print(nameTag)
                    print(dets[j].prob[i])
                    print((b.x, b.y, b.w, b.h))
                res.append((nameTag, dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    if debug: print("did range")
    res = sorted(res, key=lambda x: -x[1])
    if debug: print("did sort")
    free_detections(dets, num)
    if debug: print("freed detections")
    return res


netMain = None
metaMain = None
altNames = None

def performDetect(imagePath, thresh= 0.5, configPath = "v3medium/backup/yolov3-spp-optimal-mosaic-adver-512-rd.cfg", weightPath = "v3medium/backup/yolov3-spp-optimal-mosaic-adver-512-rd_8526.weights", metaPath= "v3medium/obj.data", showImage= True, makeImageOnly = False, initOnly= False):
    """
    Convenience function to handle the detection and returns of objects.

    Displaying bounding boxes requires libraries scikit-image and numpy

    Parameters
    ----------------
    imagePath: str
        Path to the image to evaluate. Raises ValueError if not found

    thresh: float (default= 0.25)
        The detection threshold

    configPath: str
        Path to the configuration file. Raises ValueError if not found

    weightPath: str
        Path to the weights file. Raises ValueError if not found

    metaPath: str
        Path to the data file. Raises ValueError if not found

    showImage: bool (default= True)
        Compute (and show) bounding boxes. Changes return.

    makeImageOnly: bool (default= False)
        If showImage is True, this won't actually *show* the image, but will create the array and return it.

    initOnly: bool (default= False)
        Only initialize globals. Don't actually run a prediction.

    Returns
    ----------------------


    When showImage is False, list of tuples like
        ('obj_label', confidence, (bounding_box_x_px, bounding_box_y_px, bounding_box_width_px, bounding_box_height_px))
        The X and Y coordinates are from the center of the bounding box. Subtract half the width or height to get the lower corner.

    Otherwise, a dict with
        {
            "detections": as above
            "image": a numpy array representing an image, compatible with scikit-image
            "caption": an image caption
        }
    """
    # Import the global variables. This lets us instance Darknet once, then just call performDetect() again without instancing again
    global metaMain, netMain, altNames #pylint: disable=W0603
    assert 0 < thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `"+os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `"+os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `"+os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = load_net_custom(configPath.encode("ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = load_meta(metaPath.encode("ascii"))
    if altNames is None:
        # In Python 3, the metafile default access craps out on Windows (but not Linux)
        # Read the names file and create a list to feed to detect
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents, re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass
    if initOnly:
        print("Initialized detector")
        return None
    if not os.path.exists(imagePath):
        raise ValueError("Invalid image path `"+os.path.abspath(imagePath)+"`")
    # Do the detection
    #detections = detect(netMain, metaMain, imagePath, thresh)	# if is used cv2.imread(image)
    detections = detect(netMain, metaMain, imagePath.encode("ascii"), thresh)
    A = detections
    if showImage:
        try:
            from skimage import io, draw
            import numpy as np
            image = io.imread(imagePath)
            print("*** "+str(len(detections))+" Results, color coded by confidence ***")
            imcaption = []
            for detection in detections:
                label = detection[0]
                confidence = detection[1]
                pstring = label+": "+str(np.rint(100 * confidence))+"%"
                imcaption.append(pstring)
                print(pstring)
                bounds = detection[2]
                shape = image.shape
                # x = shape[1]
                # xExtent = int(x * bounds[2] / 100)
                # y = shape[0]
                # yExtent = int(y * bounds[3] / 100)
                yExtent = int(bounds[3])
                xEntent = int(bounds[2])
                # Coordinates are around the center
                xCoord = int(bounds[0] - bounds[2]/2)
                yCoord = int(bounds[1] - bounds[3]/2)
                boundingBox = [
                    [xCoord, yCoord],
                    [xCoord, yCoord + yExtent],
                    [xCoord + xEntent, yCoord + yExtent],
                    [xCoord + xEntent, yCoord]
                ]
                # Wiggle it around to make a 3px border
                rr, cc = draw.polygon_perimeter([x[1] for x in boundingBox], [x[0] for x in boundingBox], shape= shape)
                rr2, cc2 = draw.polygon_perimeter([x[1] + 1 for x in boundingBox], [x[0] for x in boundingBox], shape= shape)
                rr3, cc3 = draw.polygon_perimeter([x[1] - 1 for x in boundingBox], [x[0] for x in boundingBox], shape= shape)
                rr4, cc4 = draw.polygon_perimeter([x[1] for x in boundingBox], [x[0] + 1 for x in boundingBox], shape= shape)
                rr5, cc5 = draw.polygon_perimeter([x[1] for x in boundingBox], [x[0] - 1 for x in boundingBox], shape= shape)
                boxColor = (int(255 * (1 - (confidence ** 2))), int(255 * (confidence ** 2)), 0)
                draw.set_color(image, (rr, cc), boxColor, alpha= 0.8)
                draw.set_color(image, (rr2, cc2), boxColor, alpha= 0.8)
                draw.set_color(image, (rr3, cc3), boxColor, alpha= 0.8)
                draw.set_color(image, (rr4, cc4), boxColor, alpha= 0.8)
                draw.set_color(image, (rr5, cc5), boxColor, alpha= 0.8)
                cv2.putText(image, label, (int(bounds[0]), int(bounds[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, boxColor, 1)
            if not makeImageOnly:
                # io.imshow(image)
                io.show()
                imgname = imagePath
            detections = {
                "detections": detections,
                "image": image,
                "caption": "\n<br/>".join(imcaption)
            }
        except Exception as e:
            print("Unable to show image: "+str(e))
    return A

#crawler def
http = httplib2.Http()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',}

def Get_Text(url, saved_dir_text): 
    if not os.path.exists(saved_dir_text):
        os.mkdir(saved_dir_text)

    try:
        response = urllib.request.urlopen(url)      # make request with https url
    except:
        status, response = http.request(url)        # make request with http url
    soup = BeautifulSoup(response, 'html.parser')
    
    #create a crawled file with website title name
    
    file_content = ""
    content = soup.find_all('p') #['h1','h2','h3','h4','div','p'])        #find all text and headlines

    if len(content) == 0:
        print("There is nothing to crawl")
        return 0
    file_text =os.path.join(saved_dir_text, soup.title.string + ".txt")
    with open(file_text, "w", encoding="utf-8") as f:
        print("Website title:"+ soup.title.string)
        print("Text content:")

        for feed in content:
            file_content += feed.get_text() + " "
        print(file_content)
        f.write(file_content)
        f.close()
    
    print("Crawling text succeeded!")

def Get_Img(url, saved_dir_img):
    if not os.path.exists(saved_dir_img):
        os.mkdir(saved_dir_img)

    count_img = 0
    count_download = 0
    
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    browser = webdriver.Chrome('/usr/bin/chromedriver', options=op)
    browser.get(url)
    images = browser.find_elements_by_tag_name('img')
    for image in images:
        image_url = image.get_attribute('src')
        print(image_url)
        try:
            if not validators.url(image_url):
                image_url = url + image_url.split('//')[0]
            r = requests.get(image_url, stream=True, headers=headers)
            print("Status code: " + str(r.status_code))
            if r.status_code == 200:
                filename = os.path.join(saved_dir_img, image_url.split('/')[-1])
                with open(filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    count_download += 1
        except:
            print("Cannot download: " + str(image_url))
    print("Crawling img succeeded!")

#main 

if __name__ == "__main__":  
    output = 0
    url = str(input('URL: '))
    # if url[len(url)-1] != '/':  #url standardization
    #     url += '/'
    # if 'https://' not in url and 'http://' not in url:
    #     url = 'https://' + url
    url_name = url.replace("/", "").replace("https:", "").replace("http:", "")
    saved_dir_text = 'Text' + url_name 
    saved_dir_img = 'Img' + url_name
    Get_Text(url, saved_dir_text)
    Get_Img(url, saved_dir_img)
    porn = 0
    saved_dir_img = saved_dir_img + "/*"
    cls = vn_Bayes()
    cls.load_model("train123.csv")
    CLS = en_Bayes()
    CLS.load_model("TextsProcess/en.NaiveBayes/train.csv")
    files=os.listdir(saved_dir_text)
    i=0
    for file in glob.glob(saved_dir_img):
        imagePath = file
        im = Image.open(imagePath)
        if im.size[0] < 224 and im.size[1] < 224:
            continue
        else:
            A = []
            A = performDetect(imagePath)
            if (A == []):
                continue
            else:
                # print(imagePath)
                porn += 1
    for file in files:
        # root = tk.Tk()
        # root.withdraw()
        fi=os.path.join(saved_dir_text,file)
        x=cls.classifier(fi)             # result text VN
        y=CLS.classifier(fi)             # result text Eng
    #     if x == 1:
    #         print("Web sex co noi dung tieng viet")
    #         messagebox.showwarning('Thong bao', 'Web sex co noi dung tieng Viet')
    #     if y == 1:
    #         print("Web sex co noi dung tieng anh")
    #         messagebox.showwarning('Thong bao', 'Web sex co noi dung tieng Anh')
    #     if x == 0 and y ==0:
    #         messagebox.showwarning('Thong bao', 'Web sex co noi dung binh thuong')
    # messagebox.showwarning('So anh khieu dam la: ', porn)
    # if x == 1:
    #     messagebox.showwarning('Thong bao', "Web sex co noi dung tieng Viet")
    # if y == 1:
    #     messagebox.showwarning('Thong bao','Web sex co noi dung tieng Anh')  
    # messagebox.showwarning('So anh khieu dam la: ', porn)
    if (x == 1 or y == 1) and porn > 0:
        output = 1                # web porn
    else: 
        output = 0                # web normal      
    print(output)
        