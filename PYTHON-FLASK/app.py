# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__) #For initializing web app
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# class Todo(db.Model):
#     sno = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(200), nullable = False)
#     desc = db.Column(db.String(500), nullable = False)
#     date_created =db.Column(db.DateTime, default = datetime.utcnow)

#     def __repr__ (self) -> str :
#         return f"{self.sno} - {self.title}"
#         # return super().__repr__()


# @app.route("/")  #Endpoints
# def hello_world():
#     return render_template('index.html')
#     # return "<p>Hello, World!</p>"

# @app.route("/product")  #Endpoints
# def products():
#     return "<p>Welcome!This is my Product page</p>"

# #The below 2 lines are requred to run any web app
# if __name__ == '__main__': 
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # Initialize web app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods = ['GET', 'POST'])  # Endpoints
def hello_world():
    if request.method == 'POST':
        title = request.form.get("title")
        desc = request.form.get("desc")
        # title = print(request.form["title"])
        # desc = print(request.form["desc"])
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)


@app.route("/show")  # Endpoints
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "<p>Welcome! This is my Product page</p>"

@app.route("/update/<int:sno>", methods = ['GET', 'POST'])  # Endpoints
def update(sno):
    if request.method == 'POST':
        title = request.form.get("title")
        desc = request.form.get("desc")
        # title = print(request.form["title"])
        # desc = print(request.form["desc"])
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo)
    # return "<p>Welcome! This is my Product page</p>"

@app.route("/delete/<int:sno>")  # Endpoints
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    # ⚡ Add this to create database tables
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
