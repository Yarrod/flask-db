#!/usr/bin/env/python3

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm 
from wtforms import SelectField
from wtforms import TextField
import matplotlib.pyplot as plt
import numpy as np
import time

def plot_random(applications):
    mu, sigma = applications, applications/5
    x = mu + sigma * np.random.randn(1000)
    hist, bins = np.histogram(x, bins=50)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plot_address = 'static/images/'+hex(int(time.time()))+'.png'
    plt.savefig(plot_address)
    plt.clf()
    return plot_address

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2))
    name = db.Column(db.String(50))

class Vacancies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(64))
    branch = db.Column(db.String(64))
    brand = db.Column(db.String(64))
    applications = db.Column(db.Float)

class Form(FlaskForm):
    name = TextField("Name Of Student")
    region = SelectField('region', choices=[('Praha','Praha'),('Brno','Brno'),('Ostrava','Ostrava'),('Olomouc','Olomouc')]) 
    branch = SelectField('branch', choices=[('Potravinářství','Potravinářství'),('Lesnictví','Lesnictví'),('IT','IT'),('Ostatní','Ostatní')])
    brand = SelectField('brand', choices=[('Jobs','Jobs'),('Prace','Prace')])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()

    if request.method == 'POST':
        applications_result = Vacancies.query.filter_by(region=form.region.data,branch = form.branch.data, brand=form.brand.data).first()
        
        result = 'Applications: {}'.format(applications_result.applications)
        result_graph_url = plot_random(applications_result.applications)
        return render_template('index.html', form=form, results = result,result_graph_url=result_graph_url)
        
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=54321)