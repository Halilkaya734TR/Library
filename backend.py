from flask import Flask
from routes.userRoutes import userBp
from routes.bookRoutes import bookBp
from routes.adminRoutes import adminBp

app=Flask(__name__)
app.secret_key = "HeasPoty!l01Zs"

app.register_blueprint(userBp)
app.register_blueprint(adminBp)
app.register_blueprint(bookBp)

if __name__ == "__main__":
    app.run(debug=True)