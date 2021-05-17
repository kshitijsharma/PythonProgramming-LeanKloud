from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.utils import cached_property
import mysql.connector
import datetime
mysql = mysql.connector.connect(host="localhost",user="root",passwd="Kshitij@123",database="test_db")

cur = mysql.cursor(buffered=True)
cur.execute("use test_db")

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'due': fields.String(required=True, description='Due date for the task'),
    'status': fields.Integer(required=True, description='Current status of the task Not started -> 0, In progress -> 1, and Finished -> 2')
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []
        pass

    def get(self, id):
        try:
            cur.execute("select * from todo")
            result = cur.fetchall()
            for db in result:
                if(db[0]==id):
                    date= db[2].strftime("%Y/%m/%d")
                    todo = {'id':db[0] ,'task':db[1] ,'due':date,'status':db[3]}
                    return todo
        except Exception as e:
            print(e)

        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        try:
            dt = list(map(int,data['due'].split('-')))
            now = datetime.date(dt[0],dt[1],dt[2])
            cur.execute("INSERT INTO todo (task, due, status) VALUES (%s, %s, '%s')",(data['task'], now,data['status']))   
            mysql.commit()

        except Exception as e:
            print(e)
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        



    def update(self, id, data):

        try:
            for d in data:
                cur.execute("update todo set "+str(d)+" = %s where id = %s",(data[d],id)   )
            mysql.commit()

        except Exception as e:
            print(e)

        return self.get(id)

    def delete(self, id):
        try:
            cur.execute("delete from todo where id = %s",(id,))
            mysql.commit()
        except Exception as e:
            print(e)

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        todos = []
        try:
            cur.execute("select * from todo")
            result = cur.fetchall()
            for db in result:
                date= db[2].strftime("%Y/%m/%d")
                todo = {'id':db[0] ,'task':db[1] ,'due':date,'status':db[3]}
                todos.append(todo)
        except Exception as e:
            print(e)
        return todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201
    
    @ns.doc('create_todo1')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post1(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


@ns.route('/finished')
@ns.response(404, 'Todo not found')

class Todo1(Resource):
    '''Show todos that are finished'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self):
        '''Fetch a given resource'''
        todos= []
        try:
            cur.execute("select * from todo")
            result = cur.fetchall()
            for db in result:
                if(db[3]==2):
                    date= db[2].strftime("%Y/%m/%d")
                    todo = {'id':db[0] ,'task':db[1] ,'due':date,'status':db[3]}
                    todos.append(todo)
        except Exception as e:
            print(e)
#        return DAO.get(id)
        return todos
    


@ns.route('/overdue')
@ns.response(404, 'Todo not found')

class Todo2(Resource):
    '''Show todos that are overdue'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self):
        '''Fetch a given resource'''
        todos= []
        try:
            cur.execute("select * from todo")
            result = cur.fetchall()
            today = datetime.date.today()
            for db in result:
                if(db[2]>today):
                    print(today,db[2])
                    date= db[2].strftime("%Y/%m/%d")
                    todo = {'id':db[0] ,'task':db[1] ,'due':date,'status':db[3]}
                    todos.append(todo)
        except Exception as e:
            print(e)
#        return DAO.get(id)
        return todos

@ns.route('/due_on/<date>')
@ns.response(404, 'Todo not found')

class Todo3(Resource):
    '''Get todos on a due date'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self,date):
        '''Fetch a given resource'''
        todos= []
        print(date)
        try:
            dt = list(map(int,date.split('-')))
            now = datetime.date(dt[0],dt[1],dt[2])
            cur.execute("select * from todo")
            result = cur.fetchall() 
            for db in result:
                print(now,db[2])
                if(db[2]==now):                   
                    date= db[2].strftime("%Y/%m/%d")
                    todo = {'id':db[0] ,'task':db[1] ,'due':date,'status':db[3]}
                    todos.append(todo)
        except Exception as e:
            print(e)

        return todos
    

DAO = TodoDAO()
"""Uncomment the following for intitializing the todo list"""
#DAO.create({'task': 'Test 1','due':'2021-5-1','status':1})
#DAO.create({'task': 'Test 2','due':'2021-5-2','status':2})
#DAO.create({'task': 'Test 3','due':'2021-5-20','status':0})
#DAO.create({'task': 'Test 4','due':'2021-6-17','status':0})
#DAO.create({'task': 'Test 5','due':'2021-8-17','status':2})
#DAO.create({'task': 'Test 6','due':'2021-8-1','status':1})

if __name__ == '__main__':
    app.run(debug=True)