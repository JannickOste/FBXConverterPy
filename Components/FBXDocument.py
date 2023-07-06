from Components.FBXDocumentHeader import FBXDocumentHeader
from Components.FBXDocumentNode import FBXDocumentNode


class FBXDocument:
    __header: FBXDocumentHeader
    __topLevelDocument: FBXDocumentNode

    def __init__(self, header: FBXDocumentHeader, topLevelDocument: FBXDocumentNode):
        self.__header = header
        self.__topLevelDocument = topLevelDocument
    
    @property 
    def header(self) -> FBXDocumentHeader:
        return self.__header
        
        
    @property
    def topLevelDocument(self) -> FBXDocumentNode: 
        return self.__topLevelDovncument
    
