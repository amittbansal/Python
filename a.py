from __future__ import division 
import Tkinter as tk
import tkFileDialog
#from Tkinter import *
from nltk.corpus import stopwords 
import codecs                                                              
import enchant                                                             
import re 
import os            
import textmining  
import numpy as np
#from datetime import datetime
from sklearn.feature_extraction.text import TfidfTransformer
import peach as p 
from numpy.random import random
import heapq
import skfuzzy as fuzz  
import rpy2.robjects as ro
import pandas as pd
                                                             


class Application(tk.Tk):
    def __init__(self, *args, **Kwargs):
        tk.Tk.__init__(self,*args, **Kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frame = {}
        for F in (startpage,matrixone,matrixtwo,documentspecific,documentspecifictopic,topicspecific,topicspecificword,result):
            frame=F(container,self)
            self.frame[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(startpage)
        
    def show_frame(self,cont):
        frame = self.frame[cont]
        frame.tkraise()
        
    def get_page(self, classname):
        '''Returns an instance of a page given it's class name as a string'''
        for page in self.frame.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None
        
class startpage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        f1 = tk.Frame(self)
        f1.pack(fill = "both",side="top",expand = True)
        lf1 = tk.LabelFrame(f1, text="File Selection",relief = 'raised',bd=5)
        lf1.pack(side="top",fill="both",expand="yes")    
        l1 = tk.Label(lf1, text="Choose the file name",relief = 'raised',bd=6)
        l1.pack(side='left',fill="both")
        self.var = tk.StringVar()
        e1 = tk.Entry(lf1,textvariable = self.var,width=113)
        e1.pack(side='left',fill="both")
        b1 = tk.Button(lf1, text ="Browse File",bd=6,relief = 'raised',command=self.file)
        b1.pack(side='left',fill="both")
              
        f2 = tk.Frame(self)
        f2.pack(fill = "both",side="top",expand = True)
        lf2 = tk.LabelFrame(f2,text="Filteration Technique",relief = 'raised' , bd = 5)
        lf2.pack(fill = "x",expand="yes")
        l2 = tk.Label(lf2,text="Choose the filteration technique : ",bd = 5, relief = 'raised',justify="left")
        l2.pack(anchor = "w")
        self.v1 = tk.IntVar()
        r1 = tk.Radiobutton(lf2,text = "No Numeric Digit",value=1,variable=self.v1,padx = 40,justify="left")
        r1.pack(anchor = "w")
        r11 = tk.Radiobutton(lf2,text = "Number Character together with combination of special character",value=2,variable=self.v1,padx = 40,justify="left")
        r11.pack(anchor = "w")
        r12 = tk.Radiobutton(lf2,text = "Start With Special Character",value=3,variable=self.v1,padx = 40,justify="left")
        r12.pack(anchor = "w")
        r13= tk.Radiobutton(lf2,text="NNo Filteration(Default)",value=4,variable=self.v1,padx = 40,justify="left")
        r13.pack(anchor = "w")
        
        f3 = tk.Frame(self)
        f3.pack(fill = "both",side="top",expand = True)
        lf3 = tk.LabelFrame(f3,text="Dictionary Option",relief = 'raised' , bd = 5)
        lf3.pack(fill = "x",expand="yes")
        l3 = tk.Label(lf3 ,text="Choose the Dictionary Option : ",bd = 5, relief = 'raised',justify="left")
        l3.pack(anchor = "w")
        self.v2 = tk.IntVar()
        r3 = tk.Radiobutton(lf3,text="With Dictionary",value=1,padx = 40,justify="left",variable=self.v2)
        r3.pack(anchor = "w")
        r31 = tk.Radiobutton(lf3,text="Without Dictionary (Default Case)",value=2,justify="left",variable=self.v2)
        r31.pack(anchor = "w")
        
        f4 = tk.Frame(self)
        f4.pack(fill = "both", side="top",expand = True)
        lf4 = tk.LabelFrame(f4,text="Start Matrix Option",relief = 'raised' , bd = 5)
        lf4.pack(fill = "x",expand="yes")
        l4 = tk.Label(lf4 ,text="Choose the Start Matrix Option : ",bd = 5, relief = 'raised',justify="left")
        l4.pack(anchor = "w")
        self.v3 = tk.IntVar()
        r4 = tk.Radiobutton(lf4,text="Start With Document -- (D/T) after clustering option",value=1,padx = 40,justify="left",variable=self.v3)
        r4.pack(anchor = "w")
        r41 = tk.Radiobutton(lf4,text="Start with Words (Default Case) -- (W/T) after clustering option",value=2,justify="left",variable=self.v3)
        r41.pack(anchor = "w")
        
        b1 = tk.Button(self, text="calculate",bd = 6,relief = 'raised',bg="black",command=self.check)
        b1.pack(fill = "both")
        
    def check(self):
        if(self.v3.get())==1:
            self.controller.show_frame(matrixone)
        else:
            self.controller.show_frame(matrixtwo)            
            
    def file(self):
        text = tkFileDialog.askopenfilename()
        self.var.set(text)

class matrixone(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) 
        self.controller=controller
        
        f1 = tk.Frame(self)
        f1.pack(fill="both",expand=True,side="top")
        lf1 = tk.LabelFrame(f1,text="Probability of Document Choice",relief = 'raised' , bd = 5)
        lf1.pack(fill = "x",expand="yes")
        l1 = tk.Label(lf1 ,text="Choose the probability_of_document_method :",bd = 5, relief = 'raised',justify="left")
        l1.pack(anchor = "w")
        self.v1 = tk.IntVar()
        r1 = tk.Radiobutton(lf1,text="Summation of distribution of word frequency in a particular document / summation of word distribution frequency in entire matrix",value=1,padx = 40,justify="left",variable=self.v1)
        r1.pack(anchor = "w")
        r11 = tk.Radiobutton(lf1,text="Individual document / total number of documents (1 / total number of documents)(Default case)",value=2,justify="left",variable=self.v1)
        r11.pack(anchor = "w")
        
        f2 = tk.Frame(self)
        f2.pack(fill = "both",side="top",expand = True)
        lf2 = tk.LabelFrame(f2, text="Cluster/Tpoic process",relief = 'raised',bd=5)
        lf2.pack(side="top",fill="both",expand="yes")    
        l2 = tk.Label(lf2, text="Enter the number of Clusters/Topic :",relief = 'raised',bd=6)
        l2.pack(side='left',fill="both")
        self.var = tk.IntVar()
        e2 = tk.Entry(lf2,textvariable = self.var,width=113)
        e2.pack(side='left',fill="both")
        
        f3 = tk.Frame(self)
        f3.pack(fill = "both",side="top",expand = True)
        lf3 = tk.LabelFrame(f3,text="Deduction technique",relief = 'raised' , bd = 5)
        lf3.pack(fill = "x",expand="yes")
        l3 = tk.Label(lf3,text="Choose the Deduction Technique :",bd = 5, relief = 'raised',justify="left")
        l3.pack(anchor = "w")
        self.v3 = tk.IntVar()
        r3 = tk.Radiobutton(lf3,text = "SVD approach",value=1,variable=self.v3,padx = 40,justify="left")
        r3.pack(anchor = "w")
        r31 = tk.Radiobutton(lf3,text = "Peach approach",value=2,variable=self.v3,padx = 40,justify="left")
        r31.pack(anchor = "w")
        r32 = tk.Radiobutton(lf3,text = "Skfuzzy approach",value=3,variable=self.v3,padx = 40,justify="left")
        r32.pack(anchor = "w")
        
        f4 = tk.Frame(self)
        f4.pack(fill = "both",side="top",expand = True)
        lf4 = tk.LabelFrame(f4,text="Reduction technique",relief = 'raised' , bd = 5)
        lf4.pack(fill = "x",expand="yes")
        l4 = tk.Label(lf4,text="Choose the Reduction Technique :",bd = 5, relief = 'raised',justify="left")
        l4.pack(anchor = "w")
        self.v4 = tk.IntVar()
        r4 = tk.Radiobutton(lf4,text = "Peach approach",value=1,variable=self.v4,padx = 40,justify="left")
        r4.pack(anchor = "w")
        r41 = tk.Radiobutton(lf4,text = "Skfuzzy approach",value=2,variable=self.v4,padx = 40,justify="left")
        r41.pack(anchor = "w")
        
        f5 = tk.Frame(self)
        f5.pack(fill = "both",side="top",expand = True)
        lf5 = tk.LabelFrame(f5,text="Topics of Document",relief = 'raised' , bd = 5)
        lf5.pack(fill = "x",expand="yes")
        l5 = tk.Label(lf5,text="choice to display the topics of Document :",bd = 5, relief = 'raised',justify="left")
        l5.pack(anchor = "w")
        self.v5 = tk.IntVar()
        r5 = tk.Radiobutton(lf5,text = "All Document Topics (Default case)",value=1,variable=self.v5,padx = 40,justify="left")
        r5.pack(anchor = "w")
        r51 = tk.Radiobutton(lf5,text = "Single Document Topics",value=2,variable=self.v5,padx = 40,justify="left")
        r51.pack(anchor = "w")
        
        f6 = tk.Frame(self)
        f6.pack(fill = "both",side="top",expand = True)
        lf6 = tk.LabelFrame(f5,text="Words for Document",relief = 'raised' , bd = 5)
        lf6.pack(fill = "x",expand="yes")
        l6 = tk.Label(lf6,text="choice to display the words for topics :",bd = 5, relief = 'raised',justify="left")
        l6.pack(anchor = "w")
        self.v6 = tk.IntVar()
        r6 = tk.Radiobutton(lf6,text = "All topics word (Default case)",value=1,variable=self.v6,padx = 40,justify="left")
        r6.pack(anchor = "w")
        r61 = tk.Radiobutton(lf6,text = "Single Topic word",value=2,variable=self.v6,padx = 40,justify="left")
        r61.pack(anchor = "w")
        
        b1 = tk.Button(self, text="show",bd = 6,relief = 'raised',bg="black",command=self.check)
        b1.pack(fill = "both")
        
    def check(self):
        if(self.v5.get())==2:
            self.controller.show_frame(documentspecific)        
        else:
            if(self.v6.get())==2:
                self.controller.show_frame(topicspecific)
            
            else:                
                self.controller.show_frame(result)   
             
class matrixtwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) 
        self.controller=controller
        
        f2 = tk.Frame(self)
        f2.pack(fill = "both",side="top",expand = True)
        lf2 = tk.LabelFrame(f2, text="Cluster/Tpoic process",relief = 'raised',bd=5)
        lf2.pack(side="top",fill="both",expand="yes")    
        l2 = tk.Label(lf2, text="Enter the number of Clusters/Topic :",relief = 'raised',bd=6)
        l2.pack(side='left',fill="both")
        self.var = tk.IntVar()
        e2 = tk.Entry(lf2,textvariable = self.var,width=113)
        e2.pack(side='left',fill="both")
        
        f3 = tk.Frame(self)
        f3.pack(fill = "both",side="top",expand = True)
        lf3 = tk.LabelFrame(f3,text="Deduction technique",relief = 'raised' , bd = 5)
        lf3.pack(fill = "x",expand="yes")
        l3 = tk.Label(lf3,text="Choose the Deduction Technique :",bd = 5, relief = 'raised',justify="left")
        l3.pack(anchor = "w")
        self.v3 = tk.IntVar()
        r3 = tk.Radiobutton(lf3,text = "SVD approach",value=1,variable=self.v3,padx = 40,justify="left")
        r3.pack(anchor = "w")
        r31 = tk.Radiobutton(lf3,text = "Peach approach",value=2,variable=self.v3,padx = 40,justify="left")
        r31.pack(anchor = "w")
        r32 = tk.Radiobutton(lf3,text = "Skfuzzy approach",value=3,variable=self.v3,padx = 40,justify="left")
        r32.pack(anchor = "w")
        
        f4 = tk.Frame(self)
        f4.pack(fill = "both",side="top",expand = True)
        lf4 = tk.LabelFrame(f4,text="Reduction technique",relief = 'raised' , bd = 5)
        lf4.pack(fill = "x",expand="yes")
        l4 = tk.Label(lf4,text="Choose the Reduction Technique :",bd = 5, relief = 'raised',justify="left")
        l4.pack(anchor = "w")
        self.v4 = tk.IntVar()
        r4 = tk.Radiobutton(lf4,text = "Peach approach",value=1,variable=self.v4,padx = 40,justify="left")
        r4.pack(anchor = "w")
        r41 = tk.Radiobutton(lf4,text = "Skfuzzy approach",value=2,variable=self.v4,padx = 40,justify="left")
        r41.pack(anchor = "w")
        
        f5 = tk.Frame(self)
        f5.pack(fill = "both",side="top",expand = True)
        lf5 = tk.LabelFrame(f5,text="Topics of Document",relief = 'raised' , bd = 5)
        lf5.pack(fill = "x",expand="yes")
        l5 = tk.Label(lf5,text="choice to display the topics of Document :",bd = 5, relief = 'raised',justify="left")
        l5.pack(anchor = "w")
        self.v5 = tk.IntVar()
        r5 = tk.Radiobutton(lf5,text = "All Document Topics (Default case)",value=1,variable=self.v5,padx = 40,justify="left")
        r5.pack(anchor = "w")
        r51 = tk.Radiobutton(lf5,text = "Single Document Topics",value=2,variable=self.v5,padx = 40,justify="left")
        r51.pack(anchor = "w")
        
        f6 = tk.Frame(self)
        f6.pack(fill = "both",side="top",expand = True)
        lf6 = tk.LabelFrame(f5,text="Words for Document",relief = 'raised' , bd = 5)
        lf6.pack(fill = "x",expand="yes")
        l6 = tk.Label(lf6,text="choice to display the words for topics :",bd = 5, relief = 'raised',justify="left")
        l6.pack(anchor = "w")
        self.v6 = tk.IntVar()
        r6 = tk.Radiobutton(lf6,text = "All topics word (Default case)",value=1,variable=self.v6,padx = 40,justify="left")
        r6.pack(anchor = "w")
        r61 = tk.Radiobutton(lf6,text = "Single Topic word",value=2,variable=self.v6,padx = 40,justify="left")
        r61.pack(anchor = "w")
        
        b1 = tk.Button(self, text="show",bd = 6,relief = 'raised',bg="black",command=self.check)
        b1.pack(fill = "both")

    def check(self):
        if(self.v5.get())==2:
            self.controller.show_frame(documentspecific)        
        else:
            if(self.v6.get())==2:
                self.controller.show_frame(topicspecific)
            
            else:                
                self.controller.show_frame(result)    
         
class documentspecific(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) 
        self.controller=controller
    
        f1 = tk.Frame(self)
        f1.pack(fill = "both",side="top",expand = True)
        lf1 = tk.LabelFrame(f1, text="Document Number",relief = 'raised',bd=5)
        lf1.pack(side="top",fill="both",expand="yes")    
        l1 = tk.Label(lf1, text="Enter the document number to display Topics :",relief = 'raised',bd=6)
        l1.pack(side='left',fill="both")
        self.var1 = tk.IntVar()
        e1 = tk.Entry(lf1,textvariable = self.var1,width=113)
        e1.pack(side='left',fill="both")
        
        f2 = tk.Frame(self)
        f2.pack(fill = "both",side="top",expand = True)
        lf2 = tk.LabelFrame(f2,text="Topic Choice",relief = 'raised' , bd = 5)
        lf2.pack(fill = "x",expand="yes")
        l2 = tk.Label(lf2,text="choice to display the topics of particular Document ",bd = 5, relief = 'raised',justify="left")
        l2.pack(anchor = "w")
        self.v2 = tk.IntVar()
        r2 = tk.Radiobutton(lf2,text = "All Document Topics (Default case)",value=1,variable=self.v2,padx = 40,justify="left")
        r2.pack(anchor = "w")
        r21 = tk.Radiobutton(lf2,text = "Specific Topics",value=2,variable=self.v2,padx = 40,justify="left")
        r21.pack(anchor = "w")
        
        b1 = tk.Button(self, text="Done",bd = 6,relief = 'raised',bg="black",command=self.check)#lambda: controller.show_frame(documentspecifictopic))
        b1.pack(fill = "both")
                
    def check(self):
        if(self.v2.get())==2:
            self.controller.show_frame(documentspecifictopic)        
        else: 
            self.controller.show_frame(result)
            
            

class documentspecifictopic(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) 
        self.controller=controller
        
        f1 = tk.Frame(self)
        f1.pack(fill = "both",side="top",expand = True)
        lf1 = tk.LabelFrame(f1, text="Number of Topic",relief = 'raised',bd=5)
        lf1.pack(side="top",fill="both",expand="yes")    
        l1 = tk.Label(lf1, text="Enter the number of Topics :",relief = 'raised',bd=6)
        l1.pack(side='left',fill="both")
        self.var1 = tk.IntVar()
        e1 = tk.Entry(lf1,textvariable = self.var1,width=113)
        e1.pack(side='left',fill="both")
        
        b1 = tk.Button(self, text="Done",bd = 6,relief = 'raised',bg="black",command=lambda: controller.show_frame(result))
        b1.pack(fill = "both")
        

class topicspecific(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) 
        self.controller=controller
    
        f1 = tk.Frame(self)
        f1.pack(fill = "both",side="top",expand = True)
        lf1 = tk.LabelFrame(f1, text="Topic Number",relief = 'raised',bd=5)
        lf1.pack(side="top",fill="both",expand="yes")    
        l1 = tk.Label(lf1, text="Enter the topic number to display words :",relief = 'raised',bd=6)
        l1.pack(side='left',fill="both")
        self.var1 = tk.IntVar()
        e1 = tk.Entry(lf1,textvariable = self.var1,width=113)
        e1.pack(side='left',fill="both")
        
        f2 = tk.Frame(self)
        f2.pack(fill = "both",side="top",expand = True)
        lf2 = tk.LabelFrame(f2,text="Words Choice",relief = 'raised' , bd = 5)
        lf2.pack(fill = "x",expand="yes")
        l2 = tk.Label(lf2,text="choice to display the words of particular topic ",bd = 5, relief = 'raised',justify="left")
        l2.pack(anchor = "w")
        self.v2 = tk.IntVar()
        r2 = tk.Radiobutton(lf2,text = "All word of a topic (Default case)",value=1,variable=self.v2,padx = 40,justify="left")
        r2.pack(anchor = "w")
        r21 = tk.Radiobutton(lf2,text = "Specific words",value=2,variable=self.v2,padx = 40,justify="left")
        r21.pack(anchor = "w")
        
        b1 = tk.Button(self, text="Done",bd = 6,relief = 'raised',bg="black",command=self.check)
        b1.pack(fill = "both")
        
    def check(self):
        if(self.v2.get())==2:
            self.controller.show_frame(topicspecificword)        
        else: 
            self.controller.show_frame(result)
        

class topicspecificword(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) 
        self.controller=controller
        
        f1 = tk.Frame(self)
        f1.pack(fill = "both",side="top",expand = True)
        lf1 = tk.LabelFrame(f1, text="Number of words",relief = 'raised',bd=5)
        lf1.pack(side="top",fill="both",expand="yes")    
        l1 = tk.Label(lf1, text="Enter the number of words :",relief = 'raised',bd=6)
        l1.pack(side='left',fill="both")
        self.var1 = tk.IntVar()
        e1 = tk.Entry(lf1,textvariable = self.var1,width=113)
        e1.pack(side='left',fill="both")
        
        b1 = tk.Button(self, text="Done",bd = 6,relief = 'raised',bg="black",command=lambda: controller.show_frame(result))
        b1.pack(fill = "both")
        
class result(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) 
        self.controller=controller
        
        f1 = tk.Frame(self)
        f1.pack(fill = "both",side="top",expand = True)
        lf1 = tk.LabelFrame(f1, text="Display Top topic and words",relief = 'raised',bd=5)
        lf1.pack(side="top",fill="both",expand="yes") 
        l1 = tk.Label(lf1, text="Top Topics and word as per your choice are",relief = 'raised',bd=6)
        l1.pack(side='left',fill="x")
        
        s1 = tk.Scrollbar(lf1)     
        self.t1 = tk.Text(lf1,bd=5,yscrollcommand=s1.set)
        s1.config(command = self.t1.yview)
        s1.pack(side = 'left' , fill = 'y')
        self.t1.pack(side = 'left',fill="both",expand=True)
        s2 = tk.Scrollbar(lf1)     
        self.t2 = tk.Text(lf1,bd=5,yscrollcommand=s2.set)
        s2.config(command = self.t2.yview)
        s2.pack(side = 'right' , fill = 'y')
        self.t2.pack(side = 'left',fill="both",expand=True)
        
        b1 = tk.Button(self, text="words",bd = 6,relief = 'raised',bg="black",command=self.check)
        b1.pack(fill = "both",side="bottom",expand=True)
    
    def check(self):
        p1=self.controller.get_page("result")
        p2=self.controller.get_page("startpage")
        p3=self.controller.get_page("matrixone")
        p4=self.controller.get_page("matrixtwo")
        p5=self.controller.get_page("documentspecific")
        p6=self.controller.get_page("documentspecifictopic")
        p7=self.controller.get_page("topicspecific")
        p8=self.controller.get_page("topicspecificword")

        with codecs.open(p2.var.get()) as ins,open("Filtered_file1.txt","w") as inst:
            Special_characters = "[~\!\?\@#\$%\^&\*\(\)\=\|\/\>\<\,\._\+{}\"':;'\[\]]"                                                                                                  
            Alphabets = "[a-z]"                                                                                                                                                        
            Numbers = "[0-9]"                                                                                                                                                           
            Alpha_Num = "[a-z0-9]"                                                                                                                                                      
            Alpha_Num_Special = "[~\!\?\@#\$%\^&\*\(\)\=\|\/\>\<\,\._\+{}\":;'\[\]a-z0-9]"                                                                                              
            for line in ins:                                                                                                                                                            
                text = ' '.join([word for word in line.lower().split() if word not in(re.findall(r"^"+Special_characters+"+$", word))])                                                  
                text = ' '.join([word for word in text.split() if not word.startswith("http")])                                                                                         
                if (p2.v1.get())==1:                                                                                                                                               
                    text = ' '.join([word for word in text.split() if word in(re.findall(r"^"+Alphabets+"*"+Special_characters+"*"+Alphabets+"*$", word))])
                elif (p2.v1.get())==2:                                                                                                                                         
                    text = ' '.join([word for word in text.split() if word in(re.findall(r"^.*(?=.*"+Numbers+").(?=.*"+Alphabets+")"+Alpha_Num_Special+"+$", word))])
                elif (p2.v1.get())==3:                                                                                                                                            
                    text = ' '.join([word for word in text.split() if word in(re.findall(r"^"+Special_characters+"+"+Alpha_Num+"*$", word))])
                else:   
                    text = ' '.join([word for word in text.split()])            
                text = ' '.join(re.sub(Special_characters," ",word)for word in text.split())                                                                                            
                text = ' '.join([word for word in text.split() if word not in (stopwords.words('english'))])                                                                            
                if (p2.v1.get())==1:                                                                                                                                            
                    text = ' '.join([word for word in text.split() if (enchant.Dict("en_US").check(word) == True)])       
                else :                                                                                                                                                                     
                    pass                       
                text = ' '.join([word for word in text.split() if (len(word) > 2)])                                                                                                     
                inst.write(text + '\n')                                                                                                                                                 
            inst.close() 
            
        with codecs.open("Filtered_file1.txt") as input,open("Filtered_file.txt","w") as output:
            for line in input:
                if not line in ['\n', '\r\n']:           
                    output.write(line)                  
        output.close() 
        os.remove("Filtered_file1.txt")                 
    
        self.fileinput  = open("Filtered_file.txt").readlines()
        self.num_documents = 0                                                         
        for line in self.fileinput:
            self.num_documents = self.num_documents + 1                                                                                    
            self.reading_file_info = [item.rstrip('\n') for item in self.fileinput]           
            self.tdm = textmining.TermDocumentMatrix()                                                                        
            for i in range(0,self.num_documents):                                                             
                self.tdm.add_doc(self.reading_file_info[i])                                                                              
        self.tdm.write_csv('TermDocumentMatrix_1.csv',cutoff=1)                                                             
        self.temp = list(self.tdm.rows(cutoff=1))                                                                                
        self.vocab = tuple(self.temp[0])
        self.num_words = len(self.vocab)
        
        if (p2.v3.get()) == 1:                                                                            
             self.x = np.array(self.temp[1:])                                                                                                                                      
        
        else :                                                                                             
             self.x = np.array(self.temp[1:])                                                                             
             self.x=np.transpose(self.x)                                                                               
    
        
        self.words_textfile=open("words_listed_textfile.txt","w")    
        self.words_textfile.write('All words of the Document Term frequency Matrix are :' + '\n')
        self.words_textfile.write( '\n' )
        for i in range (0,len(self.vocab)):
            self.words_textfile.write("%d. %s"  %((i)+1,self.vocab[i]))                                          
            self.words_textfile.write( '\n' ) 
        
        self.transformer = TfidfTransformer()
        self.tfidf = self.transformer.fit_transform(self.x)    
        self.x =  self.tfidf.toarray()
        
        self.numrows = len(self.x)
        self.numcolumns = len(self.x[0])
        self.sum_of_columns = self.x.sum(axis = 0)
        self.sum_of_rows = self.x.sum(axis = 1)
        self.sum_of_array = self.x.sum()    
        self.sum_of_columns = self.sum_of_columns [:,None]
        self.sum_of_rows = self.sum_of_rows[:,None]
        self.probability_of_word_in_document = np.zeros((self.numrows, self.numcolumns))    
        if (p2.v3.get()) == 1 :      
            self.probability_of_word = np.zeros((1,self.numcolumns))
            self.probability_of_document = np.zeros((1,self.numrows))  
            for i in range(0,self.numrows):     
                if (p3.v1.get()) == 1 :                                                          # calculation of the p(d) matrix based on user input
                    self.probability_of_document[0][i] = self.sum_of_rows[i][0]/ self.sum_of_array
                else :
                    self.probability_of_document[0][i] = 1/self.num_documents 
                for j in range(0,self.numcolumns):
                    self.probability_of_word[0][j] = self.sum_of_columns[j][0] / self.sum_of_array
                    self.probability_of_word_in_document[i][j] = self.x[i][j] / self.sum_of_rows[i][0]
        else :
            self.probability_of_word = np.zeros((1,self.numrows))
            self.probability_of_document = np.zeros((1,self.numcolumns)) 
            for i in range(0,self.numrows):
                self.probability_of_word[0][i] = self.sum_of_rows[i][0] / self.sum_of_array        # p(w)
                for j in range(0,self.numcolumns):
                    self.probability_of_document[0][j] = self.sum_of_columns[j][0] / self.sum_of_array         # p(d)
                    self.probability_of_word_in_document[i][j]=self.x[i][j] / self.sum_of_columns[j][0]        # p(w/d)


        #normalization of p(w/d)            
        self.rows_probability_of_word_in_document_array = len(self.probability_of_word_in_document)
        self.columns_probability_of_word_in_document_array = len(self.probability_of_word_in_document[0])
        self.probability_of_word_in_documen_after_normalization = np.zeros((self.rows_probability_of_word_in_document_array,self.columns_probability_of_word_in_document_array))
        if (p2.v3.get()) == 1 :
            self.summation = self.probability_of_word_in_document.sum(axis = 1 )
            self.summation = self.summation[:, None]  
            for i in range(0,self.rows_probability_of_word_in_document_array):
                for j in range(0,self.columns_probability_of_word_in_document_array):
                    self.probability_of_word_in_documen_after_normalization[i][j]=self.probability_of_word_in_document[i][j]/self.summation[i][0]                 
        else :
            self.summation = self.probability_of_word_in_document.sum(axis = 0)
            self.summation = self.summation[:, None]
            for i in range(0,self.rows_probability_of_word_in_document_array):
                for j in range(0,self.columns_probability_of_word_in_document_array):
                    self.probability_of_word_in_documen_after_normalization[i][j]=self.probability_of_word_in_document[i][j]/self.summation[j][0]
                                      
        if p3.var.get()== 0 or p4.var.get()==0:        
            self.Number_of_cluster = 10                             # default topic/cluster is 10
        else:
           self.Number_of_cluster = ((p3.var.get()) or (p4.var.get())) 
             
        self.Assign_number_of_cluster = self.Number_of_cluster 
        
        if ((p3.v3.get() or p4.v3.get()) in (1,2,3)):        
            self.Deduction_technique = p3.v3.get()                                  # assign the choice to the variable 
        else:   
            self.Deduction_technique = 1
        
        if(p2.v3.get()) == 1 :
            self.num_lines = int(self.num_documents)        
        else:
            self.num_lines = int(self.num_words)

        if (self.Deduction_technique == 2) :                                                        # peach approach
            mu = random((self.num_lines,self.Number_of_cluster ))               # random number as a input for peach library function to calculate the topic matrix and initial cluster mention by user                                                                      
            self.fcm = p.FuzzyCMeans(self.x, mu, 2)                             # calculate the fuzzycmeans where x is a initial documentterm matrix , mu random number   
            self.fcm = self.fcm.mu                                              # access the fcm matrix with the random number extension              
            if (self.Number_of_cluster < 10):                              # if cluster are less than 10 then in each step reduce the size of input cluster by 1 till 2 is encounter with previous fcm matrix as input  
                 self.b = 1
                 while (self.Number_of_cluster > 2):
                     self.Number_of_cluster = self.Number_of_cluster - self.b 
                     mu = random((self.num_lines, self.Number_of_cluster))                                                                                      
                     self.fcm = p.FuzzyCMeans(self.fcm, mu, 2)
                     self.fcm = self.fcm.mu
            elif (self.Number_of_cluster > 10 and self.Number_of_cluster <= 200 ):    # clusters between 10 and 200, reduce the clusters by number get by divide by 10 n take upper value till 
                 self.b = self.Number_of_cluster / 10
                 self.b = np.ceil(self.b)
                 while (self.Number_of_cluster > 2):
                     self.Number_of_cluster = self.Number_of_cluster - self.b            
                     if (self.Number_of_cluster > 2):                                        # run till cluster greater than 2
                         mu = random((self.num_lines, self.Number_of_cluster))                                                                                      
                         self.fcm = p.FuzzyCMeans(self.fcm, mu, 2)
                         self.fcm = self.fcm.mu
                     mu = random((self.num_lines, 2))                                            # final reduction with 2 clusters for better result                                            
                     self.fcm = p.FuzzyCMeans(self.fcm,mu, 2)
                     self.fcm = self.fcm.mu
            else:                                                                       # cluster greater than 200 and reduce clusters by number divide by 10
                self.b = self.Number_of_cluster / 10
                self.b = np.ceil(self.b)
                while (self.Number_of_cluster > 10):                                        # run till greater than 10
                     self.Number_of_cluster = self.Number_of_cluster - self.b            
                     if (self.Number_of_cluster > 10):
                         mu = random((self.num_lines, self.Number_of_cluster))                                                                                      
                         self.fcm = p.FuzzyCMeans(self.fcm, mu, 2)
                         self.fcm = self.fcm.mu    
                mu = random((self.num_lines, 10))                                           # reduction with 10 clusters                                                                  
                self.fcm = p.FuzzyCMeans(self.fcm, mu, 2)
                self.fcm = self.fcm.mu    
                mu = random((self.num_lines, 2))                                            # reduction with 2 clusters                                                                
                self.fcm = p.FuzzyCMeans(self.fcm, mu, 2)
                self.fcm = self.fcm.mu       
        if (self.Deduction_technique == 3) :
            self.fpc = fuzz.cluster.cmeans(self.x, self.Number_of_cluster, 2, error=0.005, maxiter=1000, init=None)
            self.fpc = self.fpc[0].T
            if (self.Number_of_cluster < 10):                                
                self.b = 1
                while (self.Number_of_cluster > 2):
                    self.Number_of_cluster = self.Number_of_cluster - self.b 
                    self.fpc = fuzz.cluster.cmeans(self.fpc, self.Number_of_cluster, 2, error=0.005, maxiter=1000, init=None)
                    self.fpc = self.fpc[0].T
            elif (self.Number_of_cluster > 10 and self.Number_of_cluster <= 200 ):    
                self.b = self.Number_of_cluster / 10
                self.b = np.ceil(self.b)
                while (self.Number_of_cluster > 2):
                    self.Number_of_cluster = self.Number_of_cluster - self.b            
                    if (self.Number_of_cluster > 2):                                        
                        self.fpc = fuzz.cluster.cmeans(self.fpc, self.Number_of_cluster, 2, error=0.005, maxiter=1000, init=None)
                        self.fpc = self.fpc[0].T
                    self.fpc = fuzz.cluster.cmeans(self.fpc, 2 , 2, error=0.005, maxiter=1000, init=None)
                    self.fpc = self.fpc[0].T               
            else:                                                                       
                self.b = self.Number_of_cluster / 10
                self.b = np.ceil(self.b)
                while (self.Number_of_cluster > 10):                                        
                    self.Number_of_cluster = self.Number_of_cluster - self.b            
                    if (self.Number_of_cluster > 10):
                        self.fpc = fuzz.cluster.cmeans(self.fpc, self.Number_of_cluster, 2, error=0.005, maxiter=1000, init=None)
                        self.fpc = self.fpc[0].T 
                    self.fpc = fuzz.cluster.cmeans(self.fpc, 10, 2, error=0.005, maxiter=1000, init=None)
                    self.fpc = self.fpc[0].T    
                    self.fpc = fuzz.cluster.cmeans(self.fpc, 2, 2, error=0.005, maxiter=1000, init=None)
                    self.fpc = self.fpc[0].T
        else:
            self.Method_SVD = np.linalg.svd(self.x,full_matrices=True)         # SVD implementation and output assign to a list variable 
            self.Matrix_S = self.Method_SVD[0]                                  # extraction of s matrix
            self.Matrix_S_Rows = self.Matrix_S.shape[0]                         # calculation of rows of s matrix      
            self.Array_for_Fcm = np.zeros((self.Matrix_S_Rows, 2))              # initialize the array for storing two rows of s matrix 
            for i in range(0,self.Matrix_S_Rows):
                for j in range(0,2):
                    self.Array_for_Fcm[i][j] = self.Matrix_S[i][j]              # shifthing the values to array from s matrix
            self.fcm = self.Array_for_Fcm
        
        if (p3.v4.get() or p4.v4.get())==2:
            self.fpc = fuzz.cluster.cmeans(self.fpc, self.Assign_number_of_cluster, 2, error=0.005, maxiter=1000, init=None)
            self.fpc = self.fpc[0].T        
            self.fcm = self.fpc
        else:    
            mu = random((self.num_lines, self.Assign_number_of_cluster))                              # final topic matrix with initial cluster input by user
            self.fcm = p.FuzzyCMeans(self.fcm,mu, 2)
            self.fcm = self.fcm.mu   
        
        #normalization of p(t/d) matrix
        self.num_arra =  self.fcm
        self.rows_of_cluster_array = len(self.num_arra)
        self.columns_of_cluster_array = len(self.num_arra[0]) 
        self.Sum_of_cluster_array_rows = self.num_arra.sum(axis=1)
        self.num_arra=self.num_arra.astype(float) 
        self.Sum_of_cluster_array_rows=self.Sum_of_cluster_array_rows[:,None]
        for i in range(0,self.rows_of_cluster_array):
            for j in range(0,self.columns_of_cluster_array):
                self.num_arra[i][j] = self.num_arra[i][j]/self.Sum_of_cluster_array_rows[i][0]   #normalization  p(t/d) and p(t/w) for choice 2
    
        if(p2.v3.get()) == 1:
            self.probability_of_term_in_document=np.zeros((self.rows_of_cluster_array,self.columns_of_cluster_array))   #p(t,d)
            for i in range(0,self.rows_of_cluster_array):
                for j in range(0,self.columns_of_cluster_array):
                    self.probability_of_term_in_document[i][j] = self.num_arra[i][j] * self.probability_of_document[0][i]
            self.sum_of_column_probability_of_term_in_document = self.probability_of_term_in_document.sum(axis = 0)
            self.sum_of_column_probability_of_term_in_document = self.sum_of_column_probability_of_term_in_document[:,None]
            self.probability_of_document_in_term = np.zeros((self.rows_of_cluster_array,self.columns_of_cluster_array)) #p(d/t)
            for i in range(0,self.rows_of_cluster_array):
                for j in range(0,self.columns_of_cluster_array):
                    self.probability_of_document_in_term[i][j] = self.probability_of_term_in_document[i][j] / self.sum_of_column_probability_of_term_in_document[j][0]   #normalization
        
            self.probability_of_word_in_documen_after_normalization = np.transpose(self.probability_of_word_in_documen_after_normalization)
            self.probability_of_word_in_term = np.dot(self.probability_of_word_in_documen_after_normalization,self.probability_of_document_in_term)    #p(w/t)
        else:
            self.probability_of_term_in_word=np.zeros((self.rows_of_cluster_array,self.columns_of_cluster_array))   # p(t,w)
            for i in range(0,self.rows_of_cluster_array):
                for j in range(0,self.columns_of_cluster_array):
                    self.probability_of_term_in_word[i][j] = self.num_arra[i][j] * self.probability_of_word[0][i]    
            self.sum_of_column_probability_of_term_in_word = self.probability_of_term_in_word.sum(axis = 0)
            self.sum_of_column_probability_of_term_in_word = self.sum_of_column_probability_of_term_in_word[:,None]
            self.probability_of_word_in_term = np.zeros((self.rows_of_cluster_array,self.columns_of_cluster_array)) # p(w/t)
            for i in range(0,self.rows_of_cluster_array):
                for j in range(0,self.columns_of_cluster_array):
                    self.probability_of_word_in_term[i][j] = self.probability_of_term_in_word[i][j] / self.sum_of_column_probability_of_term_in_word[j][0]   # normalization p(w/t)        
            self.num_arra = np.transpose(self.num_arra)
            self.probability_of_document_in_term = np.dot(self.num_arra,self.probability_of_word_in_documen_after_normalization)    #p(t/d)
            self.probability_of_document_in_term = np.transpose(self.probability_of_document_in_term)
    
        if(p2.v3.get()) == 1:
            self.rows_of_probability_of_word_in_term = len(self.probability_of_word_in_term)
            self.columns_of_probability_of_word_in_term = len(self.probability_of_word_in_term[0])
            self.sum_of_probability_of_word_in_term = self.probability_of_word_in_term.sum( axis = 0 )
            self.sum_of_probability_of_word_in_term = self.sum_of_probability_of_word_in_term[:,None]
            self.probability_of_word_in_term_after_normlization = np.zeros((self.rows_of_probability_of_word_in_term,self.columns_of_probability_of_word_in_term))
            for i in range(0,self.rows_of_probability_of_word_in_term):
                for j in range(0,self.columns_of_probability_of_word_in_term):
                    self.probability_of_word_in_term_after_normlization[i][j] = self.probability_of_word_in_term[i][j] / self.sum_of_probability_of_word_in_term[j][0]
        else:            
            self.rows_of_probability_of_document_in_term = len(self.probability_of_document_in_term)
            self.columns_of_probability_of_document_in_term = len(self.probability_of_document_in_term[0])
            self.sum_of_probability_of_document_in_term = self.probability_of_document_in_term.sum( axis = 1 )
            self.sum_of_probability_of_document_in_term = self.sum_of_probability_of_document_in_term[:,None]
            self.probability_of_document_in_term_after_normlization = np.zeros((self.rows_of_probability_of_document_in_term,self.columns_of_probability_of_document_in_term))
            for i in range(0,self.rows_of_probability_of_document_in_term):
                for j in range(0,self.columns_of_probability_of_document_in_term):
                    self.probability_of_document_in_term_after_normlization[i][j] = self.probability_of_document_in_term[i][j] / self.sum_of_probability_of_document_in_term[i][0]  #p(t/d after normalization  row wise
            """
            self.rows_of_probability_of_document_in_term = len(self.probability_of_document_in_term)
            self.columns_of_probability_of_document_in_term = len(self.probability_of_document_in_term[0])
            self.sum_of_probability_of_document_in_term = self.probability_of_document_in_term.sum( axis = 0 )
            self.sum_of_probability_of_document_in_term = self.sum_of_probability_of_document_in_term[:,None]
            self.probability_of_document_in_term_after_normlization = np.zeros((self.rows_of_probability_of_document_in_term,self.columns_of_probability_of_document_in_term))
    
            for i in range(0,self.rows_of_probability_of_document_in_term):
                for j in range(0,self.columns_of_probability_of_document_in_term):
                    self.probability_of_document_in_term_after_normlization[i][j] = self.probability_of_document_in_term[i][j] / self.sum_of_probability_of_document_in_term[j][0]  #p(t/d after normalization  row wise
   
           
            np.savetxt('Words_topics_probability.txt',array) 
            """                                                                                                   # create the txt file of this matrix
        
        if((p3.v5.get()or p4.v5.get())in(1,2)): 
            self.Topic_choice = p3.v5.get()
        else:
            self.Topic_choice = 1
        if(p2.v3.get()) == 1:
            self.rows_for_top_topics = len(self.num_arra)
            self.columns_for_top_topics = len(self.num_arra[0])
            self.array = self.num_arra     
        else :
            self.rows_for_top_topics = len(self.probability_of_document_in_term_after_normlization)
            self.columns_for_top_topics = len(self.probability_of_document_in_term_after_normlization[0])
            self.array = self.probability_of_document_in_term_after_normlization    
        if (self.Topic_choice == 2) :
            self.List_for_topic=[]        
            self.Topic_list = [] 
            
            if(p5.var1.get()==0):
                self.Document_number = 1
            else:    
                self.Document_number = p5.var1.get()
            
            if (p5.v2.get()in(1,2)): 
                self.Number_of_Topic=p5.v2.get()   
            else:
                self.Number_of_Topic = 1
            for i in range(0,self.rows_for_top_topics):
                if (i+1 == self.Document_number):                                                                                                # matches the document entered by the user
                    for j in range(0,self.columns_for_top_topics):
                        self.List_for_topic.append(self.array[i][j])                                                                                  # entering all topics value of document to list to retrive the decreasing order values
                  
                    if(p6.var1.get()== 0):    
                        self.Number_of_topic_display = 2                         
                    else:
                        self.Number_of_topic_display = p6.var1.get()                                                                                     
                    if(self.Number_of_Topic == 2):
                        self.indexes = heapq.nlargest(self.Number_of_topic_display, range(len(self.List_for_topic)), self.List_for_topic.__getitem__)           # retrieve the top topic index number as topic user want to display 
                        p1.t1.insert("end",('Top %d topic for Document %d is' %(self.Number_of_topic_display,(i)+1)))
                        p1.t1.insert("end", "\n")
                        #Topics_file.write('Top %d topic for Document %d is' %(Number_of_topic_display,Document_number))                     # writing the document number in the text file
                        #Topics_file.write('\n')        
                        for i in range(0,len(self.indexes)):
                            p1.t1.insert("end",("%d. t%d - %f "  %((i)+1,self.indexes[i]+1,(self.List_for_topic[self.indexes[i]]))))
                            #topic_list.append(str('%d. t%d - %f ' %((i)+1,indexes[i]+1,(List_for_topic[indexes[i]]))))                                                            
                            #Topics_file.write('%d. t%d - %f ' %((i)+1,indexes[i]+1,(List_for_topic[indexes[i]])))                            # writing the topic in the text file as topic user want to display
                            #Topics_file.write('\n')           
                    else :    
                        self.indexes = heapq.nlargest(len(self.List_for_topic), range(len(self.List_for_topic)), self.List_for_topic.__getitem__)                # retrieve the index number of all topic in decreasing order n store in list
                        p1.t1.insert("end",('Topic for Document %d is' %self.Document_number))
                        p1.t1.insert("end", "\n")
                        #Topics_file.write('Topic for Document %d is' %Document_number)                                                       # writing the document number in the text file
                        #Topics_file.write('\n')                        
                        for i in range(0,len(self.indexes)):
                            #print('%d. t%d - %f ' %((i)+1,indexes[i]+1,(List_for_topic[indexes[i]])))                        
                            self.Topic_list.append(str('%d. t%d - %f ' %((i)+1,self.indexes[i]+1,(self.List_for_topic[self.indexes[i]]))))
                            #Topics_file.write('%d. t%d - %f ' %((i)+1,indexes[i]+1,(List_for_topic[indexes[i]])))                            # writing the topics in tet file in decreasing order
                            #Topics_file.write('\n')
                    p1.t1.insert("end",("  ".join(self.Topic_list)))
                    p1.t1.insert("end", "\n")
                    #Topics_file.write("  ".join(topic_list))        
                    #Topics_file.write('\n')'''           
    
        else :                                                                             
            # every topic display on screen
            self.List_for_topic=[]        
            self.Topic_list = []    
            for i in range(0,self.rows_for_top_topics):
                for j in range(0,self.columns_for_top_topics):
                    self.List_for_topic.append(self.array[i][j])
                self.indexes_for_topic = heapq.nlargest(len(self.List_for_topic), range(len(self.List_for_topic)), self.List_for_topic.__getitem__)  
                p1.t1.insert("end",("topic for Document %d is :" %((i)+1)))
                p1.t1.insert('end', "\n")
                for k in range(0,len(self.indexes_for_topic)):
                    self.Topic_list.append(str( "%d t%d - %f" %((k)+1,self.indexes_for_topic[k],(self.List_for_topic[self.indexes_for_topic[k]]))))
                p1.t1.insert("end",("  ".join(self.Topic_list)))
                p1.t1.insert("end",("\n"))
                del self.Topic_list[ : ]  
                del self.List_for_topic[ : ]
        
        if ((p3.v6.get()or p4.v6.get()) in (1,2)):        
            self.Word_choice = p3.v6.get()                                       # assign choice to variable 
        else:
            self.Word_choice = 1                                                                  # default print all words
        if(p2.v3.get()) == 1:
            self.rows_for_top_words = len(self.probability_of_word_in_term_after_normlization)
            self.columns_for_top_words = len(self.probability_of_word_in_term_after_normlization[0])
            self.wordsarray = self.probability_of_word_in_term_after_normlization         
        else :
            self.rows_for_top_words = len(self.probability_of_word_in_term)
            self.columns_for_top_words = len(self.probability_of_word_in_term[0])
            self.wordsarray = self.probability_of_word_in_term
        if (self.Word_choice == 2) :
            self.List_for_words=[]        
            self.Words_list = [] 
            if(p7.var1.get()==0):
                self.Topic_number = 1
            else:
               self.Topic_number = p7.var1.get()
            if (p7.v2.get()in(1,2)):   
                self.Number_of_Words = p7.v2.get()
            else:
                self.Number_of_Words = 1
        
            for i in range(0,self.columns_for_top_words):
                if (i+1 == self.Topic_number):                                                                                                # matches the document entered by the user
                    for j in range(0,self.rows_for_top_topics):
                        self.List_for_words.append(self.wordsarray[j][i])                                                                                  # entering all topics value of document to list to retrive the decreasing order values
                       
                    if(self.Number_of_Words == 2):
                        if(p8.var1.get()==0):                        
                            self.Number_of_words_display = 2                         
                        else:
                            self.Number_of_words_display = p8.var1.get() 
                        self.indexes = heapq.nlargest(self.Number_of_words_display, range(len(self.List_for_words)), self.List_for_words.__getitem__)           # retrieve the top topic index number as topic user want to display 
                        p1.t1.insert("end",('Top %d words for Topic %d is' %(self.Number_of_words_display,(i)+1)))
                        p1.t1.insert("end","\n")
                        #Words_file.write('Top %d topic for Document %d is' %(Number_of_topic_display,Document_number))                     # writing the document number in the text file
                        #Words_file.write('\n')        
                        for i in range(0,len(self.indexes)):
                            p1.t1.insert("end",('%d. %s - %f' %((i)+1,self.vocab[self.indexes[i]],self.List_for_words[self.indexes[i]])))
                            #Words_list.append(str('%d. %s - %f' %((i)+1,vocab[indexes[i]],indexes[ab[i]]))) 
                    else :    
                        self.indexes = heapq.nlargest(len(self.List_for_words), range(len(self.List_for_words)), self.List_for_words.__getitem__)                # retrieve the index number of all topic in decreasing order n store in list
                        p1.t1.insert("end",('Words for Topic %d is' %self.Topic_number))
                        p1.t1.insert("end", "\n")
                        #Words_file.write('Words for Topic %d is' %Topic_number)                                                       # writing the document number in the text file
                        #Words_file.write('\n')                        
                        for i in range(0,len(self.indexes)):
                            #print('%d. t%d - %f ' %((i)+1,indexes[i]+1,(List_for_topic[indexes[i]])))                        
                            self.Words_list.append(str('%d. %s - %f ' %((i)+1,self.vocab[self.indexes[i]+1],(self.List_for_words[self.indexes[i]]))))
                            #Words_file.write('%d. t%d - %f ' %((i)+1,indexes[i]+1,(List_for_topic[indexes[i]])))                            # writing the topics in tet file in decreasing order
                            #Words_file.write('\n')
                        p1.t1.insert("end",("  ".join(self.Words_list)))
                        p1.t1.insert("end", "\n")
                        #Words_file.write("  ".join(Words_list))        
                        #Words_file.write('\n')         
    
        else :                                                                             
            # every topic display on screen
            self.List_for_words=[]        
            self.Words_list = []    
            for i in range(0,self.columns_for_top_words):
                for j in range(0,self.rows_for_top_words):
                    self.List_for_words.append(self.wordsarray[j][i])
                self.indexes_for_words = heapq.nlargest(len(self.List_for_words), range(len(self.List_for_words)), self.List_for_words.__getitem__)  
                p1.t2.insert("end",("Words for Topic %d is :" %((i)+1))) 
                p1.t2.insert("end",("\n"))
                for k in range(0,len(self.indexes_for_words)):
                    self.Words_list.append(str( "%d %s - %f" %((k)+1,self.vocab[self.indexes_for_words[k]],(self.List_for_words[self.indexes_for_words[k]]))))
                p1.t2.insert("end",("  ".join(self.Words_list)))
                p1.t2.insert("end",("\n"))
                p1.t2.insert("end",("\n"))
                del self.Words_list[ : ]  
                del self.List_for_words[ : ] 
                      
app = Application()
app.mainloop()        
    
    
