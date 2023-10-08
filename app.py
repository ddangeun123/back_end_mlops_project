from flask import Flask
from Routes import total

app = Flask(__name__)
app.register_blueprint(total.app)


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8000)
