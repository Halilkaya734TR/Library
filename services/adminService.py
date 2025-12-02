from werkzeug.security import check_password_hash
from repository.adminRepository import AdminRepository

class AdminService:

    @staticmethod
    def login(mail, password):
        admin = AdminRepository.getAdminByMail(mail)
        if admin and check_password_hash(admin.sifre, password):
            return admin
        
        return None