from flask import render_template
from app import app_var

@app_var.route('/')
@app_var.route('/index')
def index():
    user = {'username': 'Coach Pie'}
    posts = [
        {
            'author': {'username':'Orin'},
            'body': 'A Crisp fall day in Seattle'
        },
        {
            'author': {'username': 'Vincent'},
            'body': 'Another day at werk...'
        },
        {
            'author': {'username': 'Josh'},
            'body': 'Money for nothing and my chicks for free :)'
        },
        {
            'author': {'username': 'Jed'},
            'body': 'MY band'
        },
        {
            'author': {'username': 'Brett'},
            'body': 'I love whiskey!'
        }
        
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
