import struct
from typing import Any
from Domain.Entities.DataView.DataViewResult import DataViewResult
from Domain.Entities.DataView.DataViewInterface import DataViewInterface
import numpy as np


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

    def __readValueFromBuffer(self, typeCode: str, offset: int, byteLength: int) -> list[Any, int, int]:
        """
        Read a value from the buffer based on the given type code.

        Args:
            typeCode (str): The type code representing the data type.
            offset (int): The starting offset in the buffer.
            byteLength (int): The length in bytes of the value to be read.

        Returns:
            list[Any, int, int]: A list containing the value read from the buffer, start offset, and end offset.
        """
        return struct.unpack(f"<{typeCode}", self.targetBuffer[offset:offset+byteLength])[0], offset, offset+byteLength

    def readChar(self, offset: int) -> DataViewResult:
        """
        Read a character from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        return DataViewResult(chr(self.targetBuffer[offset]), offset, offset+1)
    
    def readSChar(self, offset: int) -> DataViewResult:
        """
        Read a signed character from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("b", offset, 1);
        return DataViewResult(value, start, end);
    
    def readUChar(self, offset: int) -> DataViewResult:
        """
        Read an unsigned character from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("B", offset, 1);
        return DataViewResult(value, start, end);

    
    def readBool(self, offset: int) -> DataViewResult:
        """
        Read a boolean value from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("?", offset, 1);
        return DataViewResult(bool(value), start, end);
    
    def readShort(self, offset: int) -> DataViewResult: 
        """
        Read a 2-byte signed integer from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("h", offset, 2);
        
        assert value >= -32768 and value <= 32767;
        
        return DataViewResult(np.short(value), start, end);
    
    def readUShort(self, offset: int) -> DataViewResult: 
        """
        Read a 2-byte unsigned integer from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("H", offset, 2);
        
        assert value >= 0 and value <= 65535;
        
        return DataViewResult(np.ushort(value), start, end);
    

    def readInt32(self, offset: int) -> DataViewResult:
        """
        Read a 4-byte signed integer from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("i", offset, 4)
        
        assert value >= -2147483648 and value <= 2147483647;
        
        return DataViewResult(np.int32(value), start, end)


    def readUInt32(self, offset: int) -> DataViewResult:
        """
        Read a 4-byte unsigned integer from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("I", offset, 4)
        
        
        return DataViewResult(value, start, end)
    
    def readLong(self, offset: int) -> DataViewResult:
        """
        Read a 4-byte signedinteger (long) from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("l", offset, 4)
        return DataViewResult(value, start, end)
        
    def readULong(self, offset: int) -> DataViewResult:
        """
        Read a 4-byte unsigned integer (ulong) from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("L", offset, 4)
        return DataViewResult(value, start, end)
        

    def readInt64(self, offset: int) -> DataViewResult:
        """
        Read an 8-byte signed integer (int64) from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("q", offset, 8)
        return DataViewResult(value, start, end)


    def readUInt64(self, offset: int) -> DataViewResult:
        """
        Read an 8-byte unsigned integer (uint64) from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("Q", offset, 8)
        return DataViewResult(value, start, end)


    def readFloat(self, offset: int) -> DataViewResult:
        """
        Read a 4-byte single-precision floating-point number (float) from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("f", offset, 4)
        return DataViewResult(value, start, end)

    def readDouble(self, offset: int) -> DataViewResult:
        """
        Read an 8-byte double-precision floating-point number (double) from the buffer.

        Args:
            offset (int): The starting offset in the buffer.

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        value, start, end = self.__readValueFromBuffer("d", offset, 8)
        return DataViewResult(value, start, end)

    def readString(self, offset: int, length: int, encoding: str = "latin-1") -> DataViewResult:
        """
        Read a string from the buffer.

        Args:
            offset (int): The starting offset in the buffer.
            length (int): The length of the string to read.
            encoding (str, optional): The encoding used to decode the string. Defaults to "latin-1".

        Returns:
            DataViewResult: The result containing the value, start offset, and end offset.
        """
        return DataViewResult(self.__buffer[offset:offset+length].decode(encoding), offset, offset+length)
 