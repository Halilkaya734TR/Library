from werkzeug.security import check_password_hash, generate_password_hash
from repository.adminRepository import AdminRepository

class AdminService:

    @staticmethod
    def login(mail, password):
        admin = AdminRepository.getAdminByMail(mail)
        if admin and check_password_hash(admin.sifre, password):
            return admin
        
        return None

    @staticmethod
    def addAdmin(name, email, client_hashed_password):
        if not name or not email or not client_hashed_password:
            return False, "Tüm alanlar zorunludur"

        if AdminRepository.getAdminByMail(email):
            return False, "Bu email zaten kullanılıyor"

        stored_hash = generate_password_hash(client_hashed_password)
        AdminRepository.insertAdmin(name, email, stored_hash)
        return True, "Admin başarıyla eklendi"

    @staticmethod
    def deleteAdminById(adminId):
        AdminRepository.deleteAdminById(adminId)
        return True, "Admin başarıyla silindi"
    
    @staticmethod
    def getAdminByMail(mail):
        return AdminRepository.getAdminByMail(mail)
    
    @staticmethod
    def getAdminByID(adminID):
        return AdminRepository.getAdminById(adminID)
    
    @staticmethod
    def updateAdmin(adminID, name, mail):
        return AdminRepository.updateAdmin(adminID, name, mail)
    
    @staticmethod
    def changePassword(adminID, oldPassword, newPassword):
        admin = AdminRepository.getAdminById(adminID)
        if not admin:
            return False, "Admin bulunamadı"

        if not check_password_hash(admin.sifre, oldPassword):
            return False, "Eski şifre yanlış"
        return AdminRepository.changePassword(adminID, newPassword)
    
    @staticmethod
    def deleteAdmin(adminID, password):
        admin = AdminService.getAdminById(adminID)
        if not admin:
            return False, "Admin bulunamadı"

        if not check_password_hash(admin.sifre, password):
            return False, "Şifre yanlış"
        return AdminRepository.deleteAdmin(adminID)
    
    @staticmethod
    def getAllAdmins():
        return AdminRepository.getAllAdmins()
    