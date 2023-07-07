

import struct
from DataView.DataViewResult import DataViewResult


class DataView:
    __buffer: bytes

    def __init__(self, buffer: bytes) -> None:
        """
        Initialize a DataView object.

        Args:
            buffer (bytes): The buffer containing the data.
        """
        self.__buffer = buffer

    @property
    def targetBuffer(self) -> bytes:
        """
        Get the target buffer.

        Returns:
            bytes: The target buffer.
        """
        return self.__buffer

    def readByTypeCode(self, offset: int, type_code: str) -> tuple:
        """
        Read a value from the buffer based on the type code.

        Args:
            offset (int): The starting offset in the buffer.
            type_code (str): The type code representing the data type.

        Raises:
            ValueError: If the type code is unknown.

        Returns:
            tuple: A tuple containing the value read from the buffer and the new offset.
        """
        if type_code == "Y":
            value = struct.unpack("<h", self.__buffer[offset:offset+2])[0]
            return value, offset + 2
        elif type_code == "C":
            value = bool(self.__buffer[offset])
            return value, offset + 1
        elif type_code == "I":
            value = struct.unpack("<i", self.__buffer[offset:offset+4])[0]
            return value, offset + 4
        elif type_code == "F":
            value = struct.unpack("<f", self.__buffer[offset:offset+4])[0]
            return value, offset + 4
        elif type_code == "D":
            value = struct.unpack("<d", self.__buffer[offset:offset+8])[0]
            return value, offset + 8
        elif type_code == "L":
            value = struct.unpack("<q", self.__buffer[offset:offset+8])[0]
            return value, offset + 8
        elif type_code == "B":
            value = struct.unpack("<B", self.__buffer[offset:offset+1])[0]
            return value, offset + 1
        elif type_code == "S":
            print(length)
            length = struct.unpack("<I", self.__buffer[offset:offset+4])[0]
            value = self.__buffer[offset+4:offset+4+length].decode("latin-1")
            return value, offset + 4 + length
        else:
            raise ValueError(f"Unknown type code: {type_code}")

    def readChar(self, offset:int) -> DataViewResult:
        """
        Read a character from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        return DataViewResult(chr(self.__buffer[offset]), offset, offset+1)
    
    def readSChar(self, offset: int) -> DataViewResult:
        return DataViewResult(struct.unpack("b", self.targetBuffer[offset])[0], offset, offset+1 )
    
    def readUChar(self, offset: int) -> DataViewResult:
        return DataViewResult(struct.unpack("B", self.targetBuffer[offset])[0], offset, offset+1)

    
    def readBoolean(self, offset: int) -> DataViewResult:
        """
        Read a boolean value from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, end_offset = self.readByTypeCode(offset, "C")
        return DataViewResult(value, offset, end_offset)
    
    def readShort(self, offset: int) -> DataViewResult: 
        return DataViewResult(struct.unpack("h", self.targetBuffer[offset:offset+2]), offset, offset+2)
    
    def readUShort(self, offset: int) -> DataViewResult: 
        return DataViewResult(struct.unpack("H", self.targetBuffer[offset:offset+2]), offset, offset+2)
    
    def readInt16(self, offset: int) -> DataViewResult:
        """
        Read a 2-byte signed integer from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, end_offset = self.readByTypeCode(offset, "Y")
        return DataViewResult(value, offset, end_offset)
    


    def readInt32(self, offset: int) -> DataViewResult:
        """
        Read a 4-byte signed integer from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, end_offset = self.readByTypeCode(offset, "I")
        return DataViewResult(value, offset, end_offset)

    def readInt64(self, offset: int) -> DataViewResult:
        """
        Read an 8-byte signed integer from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, end_offset = self.readByTypeCode(offset, "L")
        return DataViewResult(value, offset, end_offset)

    def readUint8t(self, offset: int) -> DataViewResult:
        """
        Read an 8-bit unsigned integer from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, end_offset = self.readByTypeCode(offset, "B")
        return DataViewResult(value, offset, end_offset)

    def readFloat(self, offset: int) -> DataViewResult:
        """
        Read a 4-byte single-precision floating-point number from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, end_offset = self.readByTypeCode(offset, "F")
        return DataViewResult(value, offset, end_offset)

    def readDouble(self, offset: int) -> DataViewResult:
        """
        Read an 8-byte double-precision floating-point number from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, end_offset = self.readByTypeCode(offset, "D")
        return DataViewResult(value, offset, end_offset)

    def readString(self, offset: int, length: int) -> DataViewResult:
        """
        Read a string from the buffer.

        Args:
            offset (int): The starting offset in the buffer.
            length (int): The length of the string to read.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        
        return DataViewResult(self.__buffer[offset:offset+length].decode("latin-1"), offset, offset+length)
