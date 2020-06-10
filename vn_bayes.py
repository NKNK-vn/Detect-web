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
    
    
if __name__ == "__main__":
    # negPath="TextsProcess/vntokenizer/results/tot"
    # posPath="TextsProcess/vntokenizer/results/xau"
    # Threshold=25
    cls=vn_Bayes()
    import time
    bd=time.time()
    # cls.train_model("train123.csv",negPath, posPath,Threshold)
    # print(time.gmtime(time.time()-bd))
    cls.load_model("train123.csv")
    #print cls.classifier("tot.txt")
    
    # bd=time.time()
    # files=os.listdir("TextsProcess/vntokenizer/Testing/tot")
    # i=0
    # for file in files:
    #     fi=os.path.join("TextsProcess/vntokenizer/Testing/tot",file)
    #     x=cls.classifier(fi)
    #     #print x
    #     i+=(x%2)
    # print(i, len(files), i*100./len(files))
    # # print(time.gmtime(time.time()-bd))
    
    # #xau
    # bd=time.time()
    # files=os.listdir("TextsProcess/vntokenizer/Testing/xau")
    # i=0
    # for file in files:
    #     fi=os.path.join("TextsProcess/vntokenizer/Testing/xau",file)
    #     x=cls.classifier(fi)
    #     #print x
    #     i+=(x%2)
    # print(i, len(files), i*100./len(files))
    # # print(time.gmtime(time.time()-bd))

    #xau
    bd=time.time()
    files=os.listdir("Test")
    i=0
    for file in files:
        fi=os.path.join("Test",file)
        x=cls.classifier(fi)
        print(x, file)
    #     i+=(x%2)
    # print(i, len(files), i*100./len(files))
    # print(time.gmtime(time.time()-bd))