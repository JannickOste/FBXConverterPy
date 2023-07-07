from Domain.Entities.Document.FBXDocumentHeader import FBXDocumentHeader
from Domain.Entities.Document.FBXDocumentNode import FBXDocumentNode


class FBXDocument:
    __header: FBXDocumentHeader
    __topLevelDocument: FBXDocumentNode

    def __init__(self: 'FBXDocument', header: FBXDocumentHeader, topLevelDocument: FBXDocumentNode):
        """
        Initialize an FBXDocument object.

        Args:
            header (FBXDocumentHeader): The FBX document header.
            topLevelDocument (FBXDocumentNode): The top-level document node.
        """
        self.__header = header
        self.__topLevelDocument = topLevelDocument
    
    @property 
    def header(self: 'FBXDocument') -> FBXDocumentHeader:
        """
        Get the FBX document header.

        Returns:
            FBXDocumentHeader: The FBX document header.
        """
        return self.__header
        
        
    @property
    def topLevelDocument(self: 'FBXDocument') -> FBXDocumentNode: 
        """
        Get the top-level document node.

        Returns:
            FBXDocumentNode: The top-level document node.
        """
        return self.__topLevelDocument
