from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import CombinedSearch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r' % self.id

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')
def dynamic_page():
    desiredCharacs = ['titles', 'locations', 'dates', 'links']
    findJobsFrom('All', "banana", desiredCharacs)
    return CombinedSearch.findJobsFrom()


if __name__ == '__main__':
    app.run(debug=True)