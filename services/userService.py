from werkzeug.security import check_password_hash, generate_password_hash
from repository.userRepository import UserRepository

class UserService:

    @staticmethod
    def login(email, password):
        user = UserRepository.getUserByMail(email)
        if user and check_password_hash(user.password, password):
            return user
        
        return None
    
    @staticmethod
    def register(username, email, password):
        if UserRepository.getUserByMail(email):
            return "Mail Var"

        hashed = generate_password_hash(password)
        UserRepository.createUser(username, email, hashed)

        return "OK"

    @staticmethod
    def deleteUser(memberID, password):
        return UserRepository.deleteUser(memberID, password)