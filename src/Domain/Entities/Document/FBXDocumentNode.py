from typing import Any, List, Self


class FBXDocumentNode: 
    __startOffset: int
    __endOffset: int
    __propertiesCount: int
    __propertiesLength: int
    __name: str
    __parent: 'FBXDocumentNode'
    __properties: List[Any]
    
    def __init__(self: 'FBXDocumentNode', startOffset: int, endOffset: int, propertiesCount: int, propertiesLength: int, name: str, properties: List[Any], parent: 'FBXDocumentNode' = None) -> None:
        """
        Initialize an FBXDocumentNode object.

        Args:
            startOffset (int): The starting offset of the node in the document.
            endOffset (int): The ending offset of the node in the document.
            propertiesCount (int): The count of properties in the node.
            propertiesLength (int): The length of properties in bytes.
            name (str): The name of the node.
            properties (List[Any]): The list of properties in the node.
            parent (FBXDocumentNode, optional): The parent node. Defaults to None.
        """
        self.__startOffset = startOffset
        self.__endOffset = endOffset
        self.__propertiesCount = propertiesCount
        self.__propertiesLength = propertiesLength
        self.__name = name
        self.__parent = parent
        self.__properties = properties
        
    @property
    def startOffset(self: 'FBXDocumentNode') -> int: 
        """Get the starting offset of the node."""
        return self.__startOffset
    
    @property
    def endOffset(self: 'FBXDocumentNode') -> int: 
        """Get the ending offset of the node (ie: the next byte after the node / start of next entry)."""
        return self.__endOffset
    
    @property
    def propertiesCount(self: 'FBXDocumentNode') -> int:
        """Get the count of properties in the node."""
        return self.__propertiesCount
    
    @property
    def propertiesLength(self: 'FBXDocumentNode') -> int: 
        """Get the length of properties in bytes."""
        return self.__propertiesLength
    
    @property 
    def name(self: 'FBXDocumentNode') -> str: 
        """Get the name of the node."""
        return self.__name
    
    @property
    def parent(self: 'FBXDocumentNode') -> 'FBXDocumentNode':
        """Get the parent node."""
        return self.__parent
    
    @property
    def properties(self: 'FBXDocumentNode') -> List[Any]: 
        """Get the list of properties in the node."""
        return self.__properties
    