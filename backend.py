from flask import Flask
from routes.userRoutes import userBp
from routes.bookRoutes import bookBp
from routes.adminRoutes import adminBp
from routes.authorRoutes import authorBp
from routes.categoryRoutes import categoryBp
from routes.publishesRoutes import publisherBp
from flask_jwt_extended import JWTManager

app=Flask(__name__)
app.secret_key = "HeasPoty!l01Zs"
app.config["JWT_SECRET_KEY"] = "MeoliWiud7ooz1!MeowayLet94521InH7a0P0P23E73Nlo2VeM!<<3^k==!s^yaxetyTro1Zs"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
jwt = JWTManager(app)

app.register_blueprint(userBp)
app.register_blueprint(adminBp)
app.register_blueprint(bookBp)
app.register_blueprint(authorBp)
app.register_blueprint(categoryBp)
app.register_blueprint(publisherBp)

if __name__ == "__main__":
    app.run(debug=True)