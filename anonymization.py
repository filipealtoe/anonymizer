'''
Created on Feb 15, 2019
Python: 3.4.3
Packages Used: 
pip install PyPDF2

@author: Filipe Altoe
'''
import argparse
import os, sys
from os import listdir
from os.path import isfile, join
import csv
import PyPDF2

def get_path(directoryName):
    path = os.path.dirname(sys.argv[0])
    if not path:
        path = '.'
    composed_path = os.path.join(path, directoryName)
    return composed_path

def read_csv(dirName, fileName):
    dirPath = get_path(dirName)
    file = open(os.path.join(dirPath, fileName))
    students = csv.reader(file)
    header = next(students, None)
    column = {}
    for h in header:
            column[h] = []
    for student in students:
        for h, v in zip(header, student):
            column[h].append(v)
    file.close
    return column
    
def extract_students(dirName="Students", fileName="Students.csv"):
    #===========================================================================
    # dirPath = get_path(dirName)
    # file = open(os.path.join(dirPath, "Students.csv"))
    # students = csv.reader(file)
    # header = next(students, None)
    # column = {}
    # for h in header:
    #         column[h] = []
    # for student in students:
    #     for h, v in zip(header, student):
    #         column[h].append(v) 
    #===========================================================================
    column = read_csv(dirName, fileName)
    column['ParsedName'] = []
    for Name in column['Name']:
        column['ParsedName'].append(Name.split(" "))       
    column.pop('Name')
    return column

def extract_tokens(dirName="Tokens", fileName="Tokens.csv"):
    column = read_csv(dirName, fileName)
    return column

def extract_Essay_Text(pdfFileName):
    # creating a pdf file object 
    pdfFileObj = open(pdfFileName, 'rb')       
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)      
    # getting number of pages in pdf file 
    numbPages = pdfReader.numPages
    
    fullText = ""
    for page in range(0,numbPages-1):    
        # creating a page object 
        pageObj = pdfReader.getPage(page)       
        # extracting text from page 
        pageText = pageObj.extractText() 
        fullText += pageText      
    # closing the pdf file object 
    pdfFileObj.close()
    return fullText

def save_output_file(textContent, fileName):
    essays_paths = get_path("OutputFiles")
    completeName = os.path.join(essays_paths, fileName +".txt") 
    file1 = open(completeName, "w")
    file1.write(textContent)
    file1.close()
    
def replace_tokens(tokens, textContent):
    pass
    
def anonymizer():
    students = extract_students("Students", "Students.csv")
    tokens = extract_tokens("Tokens", "Tokens.csv")
    essays_paths = get_path("Essays")
    allEssayfiles = [f for f in listdir(essays_paths) if isfile(join(essays_paths, f))]
    testpath = os.path.join(essays_paths, allEssayfiles[0])
    essayText = extract_Essay_Text(testpath)
    save_output_file(essayText, "student1")
    i = 0


if __name__ == '__main__':
    anonymizer()