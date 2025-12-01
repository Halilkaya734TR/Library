from werkzeug.security import check_password_hash
from repository.userRepository import UserRepository

class UserService:

    @staticmethod
    def login(mail, password):
        user = UserRepository.getUserByMail(mail)
        if user and check_password_hash(user.sifre, password):
            return user
        
        return None