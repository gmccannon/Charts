from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Replace this with your logic to fetch dynamic data from a Python file
    data_from_python = [("Name 1", 25), ("Name 2", 30), ("Name 3", 22)]

    return render_template('index.html', data=data_from_python)

if __name__ == '__main__':
    app.run(debug=True)
