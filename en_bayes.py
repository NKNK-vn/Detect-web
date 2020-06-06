# -*- coding: utf-8 -*-
import os
import codecs
import numpy as np

en_dict=[]
mainwords=[]
stopwords=[]
pornwords=[]
def maindict():
    lines=codecs.open("TextsProcess/en.NaiveBayes/en_dict.txt","rb","utf-8").readlines()
    for line in lines[1:]:
        w=line.strip().lower()
        if len(w)>0:
            en_dict.append(w)

    lines=codecs.open("TextsProcess/en.NaiveBayes/stopwords.txt","rb","utf-8").readlines()
    for line in lines:
        if len(line)>0:
            w=line.strip().lower()
            if len(w)>0:
                stopwords.append(w)

    out1=open( "TextsProcess/en.NaiveBayes/maindict.txt","wb")
    for w in en_dict:
        if w not in stopwords:
           out1.write(w+"\n")
    out1.close()

def getmainwords():
    lines=codecs.open("TextsProcess/en.NaiveBayes/maindict.txt","rb","utf-8").readlines()
    for line in lines[1:]:
        w=line.strip().lower()
        if len(w)>0:
            mainwords.append(w)
            
class en_Bayes:
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
        self.wd=dict()   
        self.posP=0.
        self.negP=0.
        self.listWords=[]
        self.vocabulary=[]
    
    def train_model(self, TrainFile, negTrainFolder, posTrainFolder, Threshold):            
        getmainwords()
        for w in mainwords:
            self.negDict[w]=0
            self.posDict[w]=0
       
        out=codecs.open(TrainFile,'wb',"utf-8")        
        #neg process
        negfiles=os.listdir(negTrainFolder)
        for file in negfiles:           
            fi=os.path.abspath(os.path.join(negTrainFolder,file))
            try:
                data=codecs.open(fi,"rb","utf-8").readlines()
            except:
                continue
            self.negfiles+=1
            print(file)
            
            for line in data:
                for w in line.split(" "):
                    w=w.lower().strip()
                    if (w in mainwords):
                        self.negDict[w]+=1
                        
        #pos process
        posfiles=os.listdir(posTrainFolder)
        for file in posfiles:            
            fi=os.path.abspath(os.path.join(posTrainFolder,file))
            try:
                data=codecs.open(fi,"rb","utf-8").readlines()
            except:
                continue
            self.posfiles+=1
            print(file)            
            for line in data:
                for w in line.split(" "):
                    w=w.lower().strip()
                    w=w.replace(".",'')
                    if (w in mainwords):
                        self.posDict[w]+=1
                        
                
        out.write("files"+","+str(self.negfiles)+","+str(self.posfiles)+"\n")
        for w in mainwords:
            if self.negDict[w]+self.posDict[w]>=Threshold:
                print(w, self.negDict[w], self.posDict[w])
                out.write( w+","+str(self.negDict[w])+","+str(self.posDict[w])+"\n")
        out.close()
       
    
        
    def load_model(self, trainmodelfile):
        lines=open(trainmodelfile).readlines()
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
            for w in nwords:
                #w=self.word(w)
                w=w.strip().lower()
                w=w.replace(".",'')
                if len(w)==0:
                    continue        
                if (w in self.vocabulary):
                    if w not in self.listWords:
                        self.listWords.append(w)
                
        
        p0=0.
        p1=0.       
        for w in self.listWords:
            p0+=np.log((self.negProbDict[w]+1.)/(self.negwords+len(pornwords)))
            p1+=np.log((self.posProbDict[w]+1.)/(self.poswords+len(pornwords)))

        p0+=np.log(self.negfiles*1./(self.negfiles+self.posfiles))
        p1+=np.log(self.posfiles*1./(self.negfiles+self.posfiles))
        if len(self.listWords)==0:
            return 0
        if p1>p0:
            return 1
        return 0
    
    
    
if __name__ == "__main__":
    clf=en_Bayes()
    #maindict()
    import time
    bd=time.time()
    clf.train_model("TextsProcess/en.NaiveBayes/train.csv", "TextsProcess/en.NaiveBayes/Training/clean","TextsProcess/en.NaiveBayes/Training/porn",10)
    clf.load_model("TextsProcess/en.NaiveBayes/trainEN.csv")
    import os
    a=0
    b=0
    bd=time.time()
    for f in os.listdir("TextsProcess/en.NaiveBayes/Training/1"):
        fi=os.path.join("TextsProcess/en.NaiveBayes/Training/1",f)
        x=clf.classifier(fi)
        if x==1:
            a+=1
        b+=1
        #print f,x
        
    print(time.gmtime(time.time()-bd),a,b, a*100./b)
    
    bd=time.time()
    for f in os.listdir("TextsProcess/en.NaiveBayes/Training/2"):
        fi=os.path.join("TextsProcess/en.NaiveBayes/Training/2",f)
        x=clf.classifier(fi)
        if x==1:
            a+=1
        b+=1
        #print f,x
        
    print(time.gmtime(time.time()-bd),a,b, a*100./b)
