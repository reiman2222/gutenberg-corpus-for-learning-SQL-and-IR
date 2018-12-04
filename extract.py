#Directory set up:
#This program need:
#   input folder: for input files
#   output folder: for output files
#   duplicate folder: for duplicate files
#   organized folder: for organized files
#       txt folder: for organized text files
#       other foler: for organized other files
#       orgDuplicate folder: for organized duplicate files
#   extract folder: for extracted data store
#       _data folder: extracted information
#       encodeErr folder: encode error files
#       exist folder: data exist
#       nonExist folder: data could not be determine author, title, language exist or not


#All user need to do is put input file insdie input folder and run the program

'''
directory structure:
.
+--extract.py
+--input
+--output
+--duplicate
+--organized
   +--txt
   +--other
   +--orgDuplicate
+--extract
   +--_data
   +--encodeErr
      +--ascii
      +--utf8
      +--unknown
   +--exist
      +--missInfo
   +--nonExist

'''
#===============================================================================================

#imports
import os
import zipfile
import codecs
#==============================================================================================
def makeDir():
    os.mkdir("input")
    os.mkdir("output")
    os.mkdir("duplicate")
    os.mkdir("organized")
    os.mkdir("organized/txt")
    os.mkdir("organized/other")
    os.mkdir("organized/orgDuplicate")
    os.mkdir("extract")
    os.mkdir("extract/_data")
    os.mkdir("extract/exist")
    os.mkdir("extract/exist/missInfo")
    os.mkdir("extract/nonExist")
    os.mkdir("extract/encodeErr")
    os.mkdir("extract/encodeErr/ascii")
    os.mkdir("extract/encodeErr/utf8")
    os.mkdir("extract/encodeErr/unkown")
#================================================================================================

#Use Recursion to loop into most inner file if it's zip unzip and step back one directory and go to second, so on.....
def unzipFiles(inputDir,outputDir,fileNameList,duplicateCounter,otherFile,duplicateFile,duplicateDir):
    fileList = os.listdir(inputDir)

    for fileName in fileList:
        #if it's directory
        if os.path.isdir(os.path.join(inputDir,fileName)):
            newInputDir = os.path.join(inputDir, fileName)
            unzipFiles(newInputDir,outputDir,fileNameList,duplicateCounter,otherFile,duplicateFile,duplicateDir)
        #if it's zip files
        elif ".zip" in fileName:
            #if file is duplicate unzip to duplicate
            if fileName in fileNameList:
                duplicateCounter+=1
                duplicateFile.write(fileName+" "+duplicateCounter+" \n")
                unzipDir = os.path.join(inputDir,fileName)
                zip_ref = zipfile.ZipFile(unzipDir, 'r')
                zip_ref.extractall(duplicateDir)
                print(fileName+" DONE")
                zip_ref.close()
            #else unzip file to output folder
            else:
                fileNameList.append(fileName)
                unzipDir = os.path.join(inputDir,fileName)
                zip_ref = zipfile.ZipFile(unzipDir, 'r')
                zip_ref.extractall(outputDir)
                print(fileName+" DONE")
                zip_ref.close()
        #else not zip file not directory, record it
        else:
            print("other files")
            otherFile.write(fileName+"\n")
#===================================================================================================

#Organize text file into organized folder, categorize file into text or other.
def organize(inputDir,categorizedTxtDir,categorizedOtherDir,categorizedDuplicateDir,fileNameList):
    outputFileList = os.listdir(inputDir)

    for fileName in outputFileList:
        if os.path.isdir(os.path.join(inputDir,fileName)):
            newInputDir = os.path.join(inputDir, fileName)
            organize(newInputDir,categorizedTxtDir,categorizedOtherDir,categorizedDuplicateDir,fileNameList)
        elif ".txt" or ".TXT" in fileName:
            fileName = fileName.replace(".TXT",".txt")
            if fileName in fileNameList:
                currentFile = os.path.join(inputDir,fileName)
                newFile = os.path.join(categorizedDuplicateDir,fileName)
                os.rename(currentFile,newFile)
                print(fileName+" DONE")
            else:
                fileNameList.append(fileName)
                currentFile = os.path.join(inputDir,fileName)
                newFile = os.path.join(categorizedTxtDir,fileName)
                os.rename(currentFile,newFile)
                print(fileName+" DONE")
        else:
            currentFile = os.path.join(inputDir,fileName)
            newFile = os.path.join(categorizedOtherDir,fileName)
            os.rename(currentFile,newFile)
            print(fileName+" DONE")

#===================================================================================================

def extractData(categorizedTxtDir,extractExistDir,extractNonExistDir,extractDataDir,extractExistMissDir,encodeErrUnkownDir,encodeErrAsciiDir,encdoeErrUtf8Dir):
    categorizedTxtFileList = os.listdir(categorizedTxtDir)

    for fileName in categorizedTxtFileList:
        title =""
        author =""
        release =""
        language =""
        text =""
        charSetEncode=""
        asciiErr = False
        utf8Err = False
        defaultErr = False

        currentFileDir = os.path.join(categorizedTxtDir,fileName)
        currentFileAscii = open(currentFileDir,"r",encoding='ascii')
        currentFileUtf8 = open(currentFileDir,"r",encoding='utf-8')
        currentFileDefult = open(currentFileDir,"r")
        try:
            ascContent = currentFileAscii.read()
        except:
            asciiErr=True

        try:
            utfContent = currentFileUtf8.read()
        except:
            utf8Err=True

        try:
            defaultContent = currentFileDefult.read()
        except:
            defaultErr = True
        
        if asciiErr == False:
            content = ascContent
        elif utf8Err == False:
            content = utfContent
        elif defaultErr == False:
            content = defaultContent
        else:
            currentFileAscii.close()
            currentFileUtf8.close()
            currentFileDefult.close()
            currentFile = os.path.join(categorizedTxtDir,fileName)
            newFile = os.path.join(encodeErrUnkownDir,fileName)
            os.rename(currentFile,newFile)
            continue
        
        splitFile = []
        if "*** START OF THIS PROJECT GUTENBERG EBOOK" in content:
            splitFile = content.split("*** START OF THIS PROJECT GUTENBERG EBOOK")
        elif "*** START OF THE PROJECT GUTENBERG EBOOK" in content:
            splitFile = content.split("*** START OF THE PROJECT GUTENBERG EBOOK")
        elif "***START OF THE PROJECT GUTENBERG EBOOK" in content:
            splitFile = content.split("***START OF THE PROJECT GUTENBERG EBOOK")

        if len(splitFile) == 2:
            info = splitFile[0]
            text = splitFile[1]
            splitLines = info.split("\n")
            for eachLine in splitLines:
                if "Title:" in eachLine:
                    title = eachLine.replace("\n","")
                elif "Author:" in eachLine:
                    author = eachLine.replace("\n","")
                elif "Release Date:" in eachLine:
                    release = eachLine.replace("\n","")
                elif "Language:" in eachLine:
                    language = eachLine.replace("\n","")
                elif "Character set encoding:" in eachLine:
                    charSetEncode =eachLine.replace("Character set encoding: ","")
                    charSetEncode = charSetEncode.replace("\n","")
            
            currentFileAscii.close()
            currentFileUtf8.close()
            currentFileDefult.close()
            if title == "" or author == "" or release == "" or language == "":
                currentFile = os.path.join(categorizedTxtDir,fileName)
                newFile = os.path.join(extractExistMissDir,fileName)
                os.rename(currentFile,newFile)
            else:
                writeNewFileName = os.path.join(extractDataDir,fileName)
                #if "ASCII" in charSetEncode:
                if asciiErr == False:
                    try:
                        writeNewFile = codecs.open(writeNewFileName,"w","ascii")
                        writeNewFile.write(title+"\n"+author+"\n"+release+"\n"+language+"\n Text: "+text)
                    except:
                        writeNewFile.close()
                        os.remove(writeNewFileName)
                        currentFile = os.path.join(categorizedTxtDir,fileName)
                        newFile = os.path.join(encodeErrAsciiDir,fileName)
                        os.rename(currentFile,newFile)
                        continue
                #elif "UTF-8" in charSetEncode:
                elif utf8Err == False:
                    try:
                        writeNewFile = codecs.open(writeNewFileName,"w","utf-8")
                        writeNewFile.write(title+"\n"+author+"\n"+release+"\n"+language+"\n Text: "+text)
                    except:
                        writeNewFile.close()
                        os.remove(writeNewFileName)
                        currentFile = os.path.join(categorizedTxtDir,fileName)
                        newFile = os.path.join(encdoeErrUtf8Dir,fileName)
                        os.rename(currentFile,newFile)
                        continue
                else:
                    try: 
                        writeNewFile = open(writeNewFileName,"w")
                        writeNewFile.write(title+"\n"+author+"\n"+release+"\n"+language+"\n Text: "+text)
                    except:
                        writeNewFile.close()
                        os.remove(writeNewFileName)
                        currentFile = os.path.join(categorizedTxtDir,fileName)
                        newFile = os.path.join(encodeErrUnkownDir,fileName)
                        os.rename(currentFile,newFile)
                        continue
                writeNewFile.close()
                currentFile = os.path.join(categorizedTxtDir,fileName)
                newFile = os.path.join(extractExistDir,fileName)
                os.rename(currentFile,newFile)
        else:
            currentFileAscii.close()
            currentFileUtf8.close()
            currentFileDefult.close()
            currentFile = os.path.join(categorizedTxtDir,fileName)
            newFile = os.path.join(extractNonExistDir,fileName)
            os.rename(currentFile,newFile)
        print(fileName+" Done")
#===================================================================================================

#main
#1
currentDir = os.getcwd()
inputDir = os.path.join(currentDir, "input")
outputDir = os.path.join(currentDir, "output")
otherFile = open(os.path.join(currentDir,"other.txt"),"w")
duplicateDir = os.path.join(currentDir, "duplicate")
duplicateFile = open(os.path.join(currentDir,"duplicate.txt"),"w")
fileNameList = []
duplicateCounter = 0
#2
categorizedTxtDir = os.path.join(currentDir,"organized","txt")
categorizedOtherDir = os.path.join(currentDir,"organized","other")
categorizedDuplicateDir = os.path.join(currentDir,"organized","orgDuplicate")
#3
extractExistDir = os.path.join(currentDir,"extract","exist")
extractExistMissDir = os.path.join(currentDir,"extract","exist","missInfo")
extractNonExistDir = os.path.join(currentDir,"extract","nonExist")
extractDataDir = os.path.join(currentDir,"extract","_data")
encodeErrUnkownDir = os.path.join(currentDir,"extract","encodeErr","unknown")
encodeErrAsciiDir = os.path.join(currentDir,"extract","encodeErr","ascii")
encdoeErrUtf8Dir = os.path.join(currentDir,"extract","encodeErr","utf8")

'''
testDir= "C:\\Users\\olive\\Desktop\\2018-all-text\\_test"
testInput=os.path.join(testDir, "input")
testExist = os.path.join(testDir, "exist")
testNon =os.path.join(testDir, "nonExist")
#testEncode = os.path.join(testDir, "encodeErr")
testWrite = os.path.join(testDir,"_data")
testInfo = os.path.join(testExist,"missInfo")
testEncAscii = os.path.join(testDir, "encodeErr","ascii")
testEncUn = os.path.join(testDir, "encodeErr","unknown")
testEncUtf8 = os.path.join(testDir, "encodeErr","utf8")
extractData(testInput,testExist,testNon,testWrite,testInfo,testEncUn,testEncAscii,testEncUtf8)
'''

print("Select your action:")
print("1. create file directories")
print("2. Unzip all files from input directory")
print("3. organize output folder, categorize it into text files and other files")
print("4. extract data from organized/txt and move file to extract/exist or extract/nonExist")
print("0. quit")

userInput = input()
if userInput == "1":
    makeDir()
if userInput == "2":
    unzipFiles(inputDir,outputDir, fileNameList,duplicateCounter,otherFile,duplicateFile,duplicateDir)
elif userInput == "3":
    otherFile.close()
    duplicateFile.close()
    organize(outputDir,categorizedTxtDir,categorizedOtherDir,categorizedDuplicateDir,fileNameList)
elif userInput == "4":
    extractData(categorizedTxtDir,extractExistDir,extractNonExistDir,extractDataDir,extractExistMissDir,encodeErrUnkownDir,encodeErrAsciiDir,encdoeErrUtf8Dir)
elif userInput == 0:
    exit()

