from app import app_var

@app_var.route('/')
@app_var.route('/index')
def index():
    return "Hello, Coach Pie!"
