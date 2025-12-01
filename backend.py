from flask import Flask
from routes.userRoutes import userBp
from routes.bookRoutes import bookBp

app=Flask(__name__)
app.secret_key = "HeasPoty!l01Zs"

app.register_blueprint(userBp)
app.register_blueprint(bookBp)

if __name__ == "__main__":
    app.run(debug=True)