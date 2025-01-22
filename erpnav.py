from flask import Flask
app = Flask(__name__)

print("Hello World")

@app.route('/')
def hello():
    print("Hello, World!")
