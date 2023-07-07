
class DataViewResult:
    __value = None 
    __startOffset = -1
    __endOffset = -1
    
    def __init__(self, value, startOffset: int, endOffset: int) -> None:
        """
        Initialize a DataViewResult object.

        Args:
            value: The value retrieved from the buffer.
            startOffset (int): The position where the record has been read.
            endOffset (int): The position after the record.
        """
        self.__value = value 
        self.__startOffset = startOffset
        self.__endOffset = endOffset
    
    @property
    def value(self):
        """
        Get the value retrieved from the buffer.

        Returns:
            The value retrieved from the buffer.
        """
        return self.__value 
    
    @property
    def startOffset(self):
        """
        Get the position where the record has been read.

        Returns:
            int: The position where the record has been read.
        """
        return self.__startOffset
    
    @property
    def endOffset(self): 
        """
        Get the position after the record.

        Returns:
            int: The position after the record.
        """
        return self.__endOffset
