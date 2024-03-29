from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
#configure the conexion string to the database = mysql using pysql://Username:Password@hostName:Port/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
#tHIS will show us the commands that SQL is running
app.config['SQLALCHEMY_ECHO'] = True
#create a database object to work with my app
db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False


@app.route('/', methods=['POST','GET'])
def index():

    if request.method == 'POST':
        task_name =request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by (completed=False).all()
    completed_task = Task.query.filter_by (completed =True).all()
    return render_template('todos.html', title='Get It Done', tasks=tasks, completed_task = completed_task)

@app.route ('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form["task-id"])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')

if __name__ == "__main__":
    app.run()