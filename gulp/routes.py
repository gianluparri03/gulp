from . import app

@app.route('/')
def index():
    return '<h1>Hello from GULP!</h1>'
