import os

from flask import Flask
from flask_cors import CORS
from Routes import total, auth

app = Flask(__name__)
app.register_blueprint(total.app)
app.register_blueprint(auth.app)

# 외부 api호출 허용
print(os.environ.get('FRONTEND_HOST'))
CORS(app, resources={r"/*": {"origins": os.environ.get('FRONTEND_HOST')}})


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8000)
