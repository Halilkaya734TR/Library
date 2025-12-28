from werkzeug.security import check_password_hash, generate_password_hash
from repository.userRepository import UserRepository

class UserService:

    @staticmethod
    def login(email, password):
        user = UserRepository.getUserByMail(email)

        if not user:
            return None, "Kullanıcı bulunamadı"

        if user.status != "Aktif":
            return None, "Hesabınız pasif durumdadır"

        if not check_password_hash(user.password, password):
            return None, "Şifre yanlış"

        return user, None
    
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
       
    
    @staticmethod
    def getUserByID(memberID):
        return UserRepository.getUserById(memberID)
    
    @staticmethod
    def getAllUsers():
        users = UserRepository.getAllUsers()
        return [
            {
                "memberID": u.memberID,
                "username": u.username,
                "email": u.email,
                "joinDate": u.joinDate,
                "status": u.status == "Aktif"
            }
            for u in users
        ]

    
    @staticmethod
    def getStatus(memberID):
        return UserRepository.getStatus(memberID)

    @staticmethod
    def updateUserStatus(memberID, status: bool):
        return UserRepository.updateUserStatus(memberID, status)
    
    @staticmethod
    def updateMember(memberID, username, email):
        return UserRepository.updateMember(memberID, username, email)
    
    @staticmethod
    def changePassword(memberID, oldPassword, newPassword):
        return UserRepository.changePassword(memberID, oldPassword, newPassword)
    
    @staticmethod
    def checkUnreturnedBooks(memberID):
        return UserRepository.checkUnreturnedBooks(memberID)
