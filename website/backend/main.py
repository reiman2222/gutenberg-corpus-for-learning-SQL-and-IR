from flask import Flask, request, render_template, render_template_string
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import *
from flask import Response
import json


app = Flask(__name__)
api = Api(app)

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'gutenburg',
    'host': 'localhost',
    'port': '5432',
    }
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

CORS(app)




#helper function to break author name into parts
#returns firstName, middleName, lastName, suffix, prefix as strings in that order
def processAuthorName(authorName):
    firstName = ''
    middleName = ''
    lastName = ''
    suffix = ''
    prefix = ''
    nameL = authorName.split()

    i = 0
    while(i < len(nameL)):
        if(')' in nameL[i] or '(' in nameL[i]):
            del nameL[i]
            i -=1
        i += 1

    nameLen = len(nameL)

    #check for prefix
    comPrefixes = ['mr', 'mrs', 'miss', 'sir', 'lord', 'ms']
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

#-----------------------------------------------#
#               Database Functions              #
#-----------------------------------------------#

#returns all books with title book_title
#book_title of type string
def get_book_by_title(book_title):
    b = Book.query.filter_by(title= book_title)
    return b

#returns the book with gutenberg_id gid
#gid is of type string
def get_book_by_gutenberg_id(gid):
    b = Book.query.filter_by(gutenberg_id = gid).first_or_404()
    return b

def get_author_by_author_id(author_id):
    a = Author.query.filter_by(author_id=author_id).first_or_404()
    return a

#returns all authors with full name author_name
def get_author_by_full_name(author_name):
    firstName, middleName, lastName, suffix, prefix = processAuthorName(author_name)
    a = Author.query.filter_by(first_name=firstName, middle_name=middleName, last_name=lastName,
        prefix=prefix, suffix=suffix)
    return a

#return all authors with first name first_name
def get_author_by_first_name(first_name):
    a =  Author.query.filter_by(first_name=first_name)
    return a

#return all authors with last name last_name
def get_author_by_last_name(last_name):
    a =  Author.query.filter_by(last_name=last_name)
    return a

#return all authors with first name first_name and last name last_name
def get_author_by_first_and_last_name(first_name, last_name):
    a = Author.query.filter_by(first_name=first_name, last_name=last_name)
    return a

#retuns a list of authors who authored the book with gutenberg_id gid
#gutenber_id is a string
def get_authors_of_book(gutenberg_id):
    author_ids = WrittenBy.query.filter_by(gutenberg_id=gutenberg_id)

    authors = []
    for auth in author_ids:
        authors.append(Author.query.filter_by(author_id=auth.author_id).first_or_404())
    return authors

#returns a list of book who were written by the author with 
#author_id author_id
#author_id is an integer
def get_books_by_author(author_id):
    book_ids = WrittenBy.query.filter_by(author_id=author_id)
    
    books = []
    for b in book_ids:
        books.append(get_book_by_gutenberg_id(b.gutenberg_id))
    return books

#       END Database Functions


#-----------------------------------------------#
#               Server  Routes                  #
#-----------------------------------------------#

#create json respond format
def build_json(result):
    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")

#Search by title name
@app.route('/title', methods=['POST'])
def title_post():
    content = request.get_json(silent=True)
    title = content["bookname"]
    if(title != ''):
        title= title.lower()
        book = get_book_by_title(title)
        numBooks = book.count()

        if(numBooks == 0):
            print("NO BOOK FOUND")
            return build_json({"respond":'No books by title: ' + title})
        else:
            print("FOUND IT")
            return build_json({"respond":book[0].full_text.replace('\n', '<br />')})
    else:
        return build_json({"respond":'Title cannot be empty.'})

#Search by author name
@app.route('/author',methods=['POST'])
def author_post():
    print("Start HERE")
    content = request.get_json(silent=True)
    author = content["authorname"]
    # Not sure if the get_book_by_author is using author name or author id ???

#       END Server Routes


if __name__ == '__main__':
    app.run(port=5008)

'''
@app.route("/")
def hello():
    #book = Book.query.filter_by(gutenberg_id='46630').first()
    #book = Book.query.filter_by(title='two mothers').first()
    #b = get_book_by_title('two mothers')
    #return get_book_by_title('two mothers')

    

    #sample showing titles of works by author 22
    bs = get_books_by_author(22)
    print(len(bs))
    titles = []
    for b in bs:
        print(b.title)
        titles.append(b.title)

    return bs[0].title, bs[0].full_text
'''

'''class Employees(Resource):
    def get(self):
        return {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]} 

class Employees_Name(Resource):
    def get(self, employee_id):
        print('Employee id:' + employee_id)
        result = {'data': {'id':1, 'name':'Balram'}}
        return jsonify(result)       


api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3
'''

'''
@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    titleText = request.form['searchTitle']
    title = titleText.lower()
    if(title != ''):
        book = get_book_by_title(title)
        numBooks = book.count()

        if(numBooks == 0):
            return 'No books by title: ' + title 
        else:
            return book[0].full_text.replace('\n', '<br />')
    else:
        return 'Title cannot be empty.'

    authorText = request.form['searchAuthor']
    authorName = authorText.lower()
    #stoped working here !!!!!!!!!!!!!!!!!
    #if(authorName != ''):
'''

    
