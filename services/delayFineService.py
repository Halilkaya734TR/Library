from repository.delayFineRepository import DelayFineRepository

class delayFineService:

    @staticmethod
    def countActiveFine(memberID):
        return DelayFineRepository.countactiveFine(memberID)
  
    @staticmethod
    def getFineByID(memberID):
        return DelayFineRepository.getByUserID(memberID)
    
    @staticmethod
    def getAllFine():
        return DelayFineRepository.getAll()
    
    @staticmethod
    def deleteByID(memberID):
        return DelayFineRepository.deleteByUserID(memberID)
        
