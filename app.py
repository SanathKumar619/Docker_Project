from flask import Flask

app = Flask(__name__)
@app.route("/")
def sanath():
    return "Hello World from Sanath Kumar along with his puppy!"

if __name__=="__main__":
    app.run(host="0.0.0.0")
