'''
Created on March 01, 2019
Python: 3.4.3
Packages Used: 
pip install pdfminer.six

@author: Filipe Altoe
'''

import os, sys
from os import listdir
from os.path import isfile, join
import csv
import pdf
import re

class Anonymizer:

    replacementTOKEN = "student"
    
    #This is the main method
    @staticmethod    
    def anonymizer(studentsDir="Students", studentsFile="Students.csv", tokensDir="Tokens", tokensFile="Tokens.csv", essaysDir="Essays", outputDir="OutputFiles", replacementTOKEN="[student]"):
        studentNumber = 1
        try:
            students = extract_students(studentsDir, studentsFile)
            tokens = extract_tokens(tokensDir, tokensFile)
            tokens= format_alltokens(tokens)
            essays_paths = get_path(essaysDir)
            allEssayfiles = [f for f in listdir(essays_paths) if isfile(join(essays_paths, f))]
            for essayFile, student in zip(allEssayfiles, students):
                testpath = os.path.join(essays_paths, essayFile)
                essayText = extract_Essay_Text(testpath)
                anonymizedText = replace_tokens(tokens, student, essayText, replacementTOKEN)
                outputFileName = replacementTOKEN + str(studentNumber)
                save_output_file(outputDir, outputFileName, anonymizedText)
                studentNumber += 1
            return (studentNumber-1)
        except Exception as e:
            print(e)
            return (studentNumber-1)
    
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
    students_paths = get_path(dirName)
    completeName = os.path.join(students_paths, fileName)
    with open(completeName) as f:
        allstudents = [{k: str(v) for k, v in row.items()}
             for row in csv.DictReader(f, skipinitialspace=True)]
    f.close()
    for student in allstudents:
        student['Name'] = student['Name'].split(" ")
    return allstudents

def extract_tokens(dirName="Tokens", fileName="Tokens.csv"):
    tokens_paths = get_path(dirName)
    completeName = os.path.join(tokens_paths, fileName)
    with open(completeName) as f:
        reader = csv.reader(f)
        alltokens = list(reader)
    f.close()
    #Remove header line
    del alltokens[0]
    return alltokens

def clean_text(text_str):
    text = (text_str.encode("utf-8", "ignore")).decode("ascii", "ignore")
    text = text.replace("\x0C", " ")
    text = re.sub(r'[\t]+', " ", text)
    text = re.sub(r'[\n\f\r]+', "\n", text)
    return text

def extract_Essay_Text(pdfFileName):
    with open(pdfFileName, "rb") as f:
        blobData = f.read()
    text,metadata = pdf.PDF.extract(blobData)
    text = clean_text(text)
    return text

def save_output_file(dirName, fileName, textContent):
    essays_paths = get_path(dirName)
    completeName = os.path.join(essays_paths, fileName +".txt") 
    file1 = open(completeName, "w")
    file1.write(textContent)
    file1.close()

def format_alltokens(tokens):
    alltokens = []
    for token in tokens:
        token = str(token[0])
        alltokens.append(token)    
    return alltokens
    
#This is where the replacements happen. It uses the input tokens on all parsed names for replacement and replaces the other student parameters without using the tokens
def replace_tokens(alltokens, student, textContent, replacementTOKEN):
    allNames = student.pop('Name')
    # student's name might be contained within their email, so we want to substitute that first
    otherParameters = student.values()
    for parameter in otherParameters:
        if (parameter == ""): continue
        textContent = textContent.replace(parameter, replacementTOKEN)
    # use regexes instead of replace
    for name in allNames:
        namestr = re.sub(r'\W+', '', name)
        namestr = "(\W)*".join(namestr)
        myRegex = re.compile(namestr, re.IGNORECASE)
        textContent = myRegex.sub(replacementTOKEN, textContent)
    return textContent    
