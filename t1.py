from flask import Flask
app = Flask(__name__)
@app.route("/",defaults={'name':'Progranmmer'})
def index(name):
    return f"123{name}"
if __name__ == "__main__":
    app.run()