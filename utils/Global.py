
class Global:

    @staticmethod
    def getImageFilesAccepted():
        
        return [
            'png', 
            'gif',
            'jpg', 
            'webp', 
            'jpeg'
        ]

    @staticmethod
    def getDocumentFilesAccepted():
        
        return [
            'pdf'
        ]
    
    @staticmethod
    def getFilesAccepted():
        
        return Global.getImageFilesAccepted() + Global.getDocumentFilesAccepted()

