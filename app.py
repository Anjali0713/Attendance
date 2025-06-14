from flask import Flask
from views.routes import views

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.register_blueprint(views)

if __name__ == '__main__':
    app.run(debug=True)
