class FBXDocumentNode: 
    __startOffset: int;
    __endOffset: int; 
    __propertiesCount: int; 
    __propertiesLength: int; 
    __name:str; 
    __parent = None
    __properties = []
    
    def __init__(self, startOffset: int, endOffset: int, propertiesCount: int, propertiesLength: int, name: str, properties, parent) -> None:
        self.__endOffset = endOffset
        self.__propertiesCount = propertiesCount
        self.__propertiesLength = propertiesLength
        self.__name = name
        self.__parent = parent
        self.__properties = properties
        
    @property
    def startOffset(self): 
        """ StartOffset is the distance from the beginning of the record to the end of the node record (i.e. the first byte of whatever comes next). This can be used to easily skip over unknown or not required records. """
        return self.__startOffset
    
    @property
    def endOffset(self): 
        """ EndOffset is the distance from the beginning of the file to the end of the node record (i.e. the first byte of whatever comes next). This can be used to easily skip over unknown or not required records. """
        return self.__endOffset
    
    @property
    def propertiesCount(self):
        """ NumProperties is the number of properties in the value tuple associated with the node. A nested list as last element is not counted as property. """
        return self.__propertiesCount
    
    @property
    def propertiesLength(self): 
        """ PropertyListLen is the length of the property list. This is the size required for storing NumProperties properties, which depends on the data type of the properties. """
        return self.__propertiesLength
    
    @property 
    def name(self): 
        """ Name is the name of the object. There is no zero-termination."""
        return self.__name
    
    @property
    def parent(self):
        return self.__parent
    
    @property
    def properties(self): 
        return self.__properties
        
    def __str__(self) -> str:
        serialized = {}
        modulePrefix: str = '_{module}__'
        for prop in [s for s in dir(self) if s.startswith(modulePrefix.format(module=self.__module__))]: 
            propertyName:str = prop.split('__')[-1]
            propertyValue =  getattr(self, propertyName)
            serialized[propertyName] = str(propertyValue) if isinstance(propertyValue, FBXDocumentNode) \
                                                          else propertyValue if propertyValue is not None \
                                                           else ''

        return str(serialized).replace('\\\'', '\'')