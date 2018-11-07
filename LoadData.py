import re
import os
import sys

import psycopg2 as pg
import pandas.io.sql as psql
from pprint import pprint 





def extractDataFromHeaderLine(dataDescription, line):
    lineS = re.split('^' + dataDescription, line, maxsplit=1)
    #print('lineS is: ')
    #pprint(lineS)
    if(len(lineS) == 2):
        return lineS[1].strip().lower()
    else:
        return ""



#for well formed docs
def getData(file):
    title =""
    author =""
    release =""
    language =""
    text =""
    gutenberId = ""
    charSetEncode=""
    asciiErr = False
    utf8Err = False
    defaultErr = False

    content = None

    currentFileAscii = open(file,"r",encoding='ascii')
    currentFileUtf8 = open(file,"r",encoding='utf-8')
    currentFileDefult = open(file,"r")

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
        
        print('error reading file: ' + file)

    #extract the data

    headerAndContent = re.split('\*\*\*', content, maxsplit=1)
    #print(headerAndContent[0])

    header = headerAndContent[0]
    fullText = headerAndContent[1]
    #print(fullText)

    headerSplit = header.split('\n')

    for line in headerSplit:
        if "Title:" in line:
            title = extractDataFromHeaderLine('Title:',line)
        elif "Author:" in line:
            author = extractDataFromHeaderLine('Author:',line)

        elif "Release Date:" in line:
            release = extractDataFromHeaderLine('Release Date:',line)
            if('[' in release):
                releaseS = release.split('[')
                release = releaseS[0].strip()

        elif "Language:" in line:
            language = extractDataFromHeaderLine('Language:',line)

    '''
    print('The title is: ' + title)
    print('Author: ' + author)
    print('Date: ' + release)
    #pprint(release)
    print('Language: ' + language)
    '''

    return title, author, release, language, fullText


def processAuthorName(authorName):
    firstName = ''
    middleName = ''
    lastName = ''
    suffix = ''
    prefix = ''
    nameL = authorName.split()
    i = 0
    while(i < len(nameL)):
        if('(' in nameL[i] or ')' in nameL[i]):
            print('was in')
            del nameL[i]
            i -= 1

        i += 1

    print('authorName finished loop: ' + authorName)

    nameLen = len(nameL)

    #check for prefix
    comPrefixes = ['mr', 'mrs', 'miss', 'sir', 'lord', 'ms', 'dr']
    comSuffixes = ['sr', 'jr', 'ii', 'iii', 'iv', 'v']


    if(nameLen > 1):
        if(nameL[0].strip('.') in comPrefixes):
            prefix = nameL[0]
            del nameL[0]
            nameLen = len(nameL)

    if(nameLen > 1):
        if(nameL[nameLen - 1].strip('.') in comSuffixes):
            suffix = nameL[nameLen - 1]
            del nameL[nameLen - 1]
            nameLen = len(nameL)

    if(nameLen == 0):
        firstName = 'anonymous'
    elif(nameLen == 1):
        firstName = nameL[0]
    elif(nameLen == 2):
        firstName = nameL[0]
        lastName = nameL[1]

    elif(nameLen == 3):
        firstName = nameL[0]
        middleName = nameL[1]
        lastName = nameL[2]
    else:
        firstName = nameL[0]
        lastName = nameL[nameLen - 1]
        del nameL[nameLen - 1]
        del nameL[0]
        middleName = ' '.join(nameL)

    '''
    print('first name: ' + firstName)
    print('middle name: ' + middleName)
    print('last name: ' + lastName)
    print('suffix: ' + suffix)
    print('prefix: ' + prefix)
    '''

    return firstName, middleName, lastName, suffix, prefix


########## Database Querys

def getBookByPrimaryKey(gutenbergId, cur):
    cur.execute('Select * From public."Book" Where gutenberg_id = %s', (gutenbergId,))
    result = cur.fetchall()
    print('got result book')
    #print(result)
    return result

def bookIsInDatabase(gutenbergId, conn):
    print('book in')
    result = getBookByPrimaryKey(gutenbergId, conn)
    #print('book is:')
    #print(result)
    #sys.exit()

    if(len(result) > 0):
        return True
    else:
        return False

def getAuthorByName(firstName, middleName, lastName, suffix, prefix, cur):
    cur.execute('Select * From public."Author" Where first_name = %s And middle_name = %s And last_name = %s and suffix = %s and prefix = %s',
                    (firstName, middleName, lastName, suffix, prefix))

    result = cur.fetchall()
    print('got auth result')
    return result

def authorIsInDatabase(firstName, middleName, lastName, suffix, prefix, cur):
    print('auth in')

    result = getAuthorByName(firstName, middleName, lastName, suffix, prefix, cur)
    print('got auth')
    if(len(result) > 0):
        return True
    else:
        return False


def getWrittenBy(gutenbergId, authorId, cur):
    cur.execute('Select * From public."Written_By" Where author_id = %s And gutenberg_id = %s', (authorId, gutenbergId)) 
    result = cur.fetchall()
    return result


def writtenByRelationInDatabase(gutenbergId, authorId, cur):
    print('written by in')

    result = getWrittenBy(gutenbergId, authorId, cur)

    if(len(result) > 0):
        return True
    else:
        return False


def insertIntoDatabase(gId, title, release, language, author, fullText, conn, cur, badFiles):
    firstName, middleName, lastName, suffix, prefix = processAuthorName(author)
    #gId = str(gId) + '-' + language
    try:
    
        
        if(not bookIsInDatabase(gId, cur)):
            try:
                #inset book
                cur.execute('INSERT INTO public."Book" (gutenberg_id,release_date,full_text,language,title) VALUES (%s,%s,%s,%s,%s);',
                            (gId, release, fullText, language, title))
                #print('loaded book')
                conn.commit()
            except pg.DataError:
                conn.rollback()
                cur.execute('INSERT INTO public."Book" (gutenberg_id,release_date,full_text,language,title) VALUES (%s,%s,%s,%s,%s);',
                            (gId, None, fullText, language, title))
                print('loaded book wth null date: ' + str(gId))
                conn.commit()
            print('author')
        else:
            print('book is in database, gid: ' + str(gId))
        
        
        #deal with multiple authors
        #authorsL = []
        #if(' and ' in author):
        #    authorsL = author.split(' and ')


        #TODO fix rest of querys
        if(not authorIsInDatabase(firstName, middleName, lastName, suffix, prefix, cur)):

            #inset author
            cur.execute('insert into public."Author" (first_name,last_name,middle_name,suffix,prefix) VALUES (%s, %s, %s, %s, %s) returning author_id',
                        (firstName, lastName, middleName, suffix, prefix))
            #print('loaded author')
            authorId = cur.fetchone()
            conn.commit()
            #print('auth id is: ' + str(authorId[0]))
            print('book')
        else:
            
            authorId = getAuthorByName(firstName, middleName, lastName, suffix, prefix, cur)[0][0]
            print('author is in database, author_id: ' + str(authorId))
        
            

        if(not writtenByRelationInDatabase(gId, authorId, cur)):
            cur.execute('INSERT INTO public."Written_By" (author_id, gutenberg_id) VALUES (%s, %s)', (authorId, gId))
            conn.commit()
            print('written by')
            #print('loaded written by')
        else:
            wb = getWrittenBy(gId, authorId, cur)
            #print(wb[0])
            #print('written by relation in database: ' + str(wb[0][0]), + ', ' + str(wb[0][1]))

            
        
        #inset written_by
    except ZeroDivisionError:
        #pass
        print('broken')
        badFiles.append(gutenbergId)
        print(Exception)
        print(gId)
        


#           MAIN            #

dbname = "gutenberg"
dbhost = "localhost"
dbport = "5432"
dbuser = "postgres"
dbpassword = "password"


conn = pg.connect(database=dbname, host=dbhost, port=dbport, user=dbuser, password=dbpassword)
cur = conn.cursor()
#dirToProcess = '/Users/edwardsja15/desktop/gutenberg/load/extract/_data'
#dirToprocessWindows = '/home/reilly/database/load/_data'

#dirToProcess = '/home/reilly/database/load/_data'
dirToProcess = '/Users/edwardsja15/desktop/gutenberg/load/extract/_data'

fileList = os.listdir(dirToProcess)
#print(fileList[:10])

invalidIds = []
badFiles = []

i = 0
for filename in fileList:
    #can load
    if('.txt' in filename):
        fullfilename = os.path.join(dirToProcess, filename)

        title, author, release, language, fullText = getData(fullfilename)

        if(language == 'en'):
            language = 'english'



        filenameS = filename.split('.')

        gidIsValid = False

        

        if('-' in filenameS[0]):
            gidS = filenameS[0].split('-')

            try:
                int(gidS[1])
                gidIsValid = True

                gutenbergId = filenameS[0]

            except ValueError:
                gidIsValid = False

                invalidIds.append(filename)

            #gutenbergId = filenameS[0].split('-')[0]
        else:
            gutenbergId = filenameS[0]
            gidIsValid = True

        print(gutenbergId)
        if(gidIsValid):
            print('valid gid is: ' + gutenbergId)
            insertIntoDatabase(gutenbergId, title, release, language, author, fullText, conn, cur, badFiles)
            print('inserted')
        i += 1
        if(i > 150):
            break




print('invalid ids are: ')
pprint(invalidIds)
print('bad files are: ')
pprint(badFiles)
        


