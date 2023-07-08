
import struct
import zlib
from Domain.Entities.DataView.DataView import DataView
from Domain.Entities.DataView.DataViewResult import DataViewResult
class FBXPropertyParser(DataView):
    def readByTypeCode(self: 'FBXPropertyParser', offset: int, typeCode: str) -> DataViewResult:
        out:DataViewResult = None
        if ["Y", "C","I", "F", "D", "L", "B"].count(typeCode) > 0:
            out = self.__parsePrimitiveType(offset, typeCode)
        elif ["f","d","l","i","b"].count(typeCode) > 0:
            out = self.__parseArrayType(offset, typeCode)
        elif ["S", "R"].count(typeCode) > 0: 
            out = self.__parseSpecialType(offset, typeCode)
        
        if out is None:
            raise ValueError(f"Unknown type code: {typeCode}")

        return out

    
    def __parsePrimitiveType(self: 'FBXPropertyParser', offset: int, typeCode:str) -> DataViewResult: 
        """
        i) Primitive Types

        Y: 2 byte signed Integer
        C: 1 bit boolean (1: true, 0: false) encoded as the LSB of a 1 Byte value.
        I: 4 byte signed Integer
        F: 4 byte single-precision IEEE 754 number
        D: 8 byte double-precision IEEE 754 number
        L: 8 byte signed Integer
        
        For primitive scalar types the Data in the record is exactly the binary representation of the value, in little-endian byte order.
        """
        if typeCode == "Y":
            return self.readShort(offset)
        elif typeCode == "C":
            return self.readBool(offset)
        elif typeCode == "I":
            return self.readInt32(offset)
        elif typeCode == "F":
            return self.readFloat(offset)
        elif typeCode == "D":
            return self.readDouble(offset)
        elif typeCode == "L":
            return self.readInt64(offset)
        elif typeCode == "B":
            return self.readUShort(offset)
    
    def __parseArrayType(self: 'FBXPropertyParser', offset: int, typeCode:str) -> DataViewResult: 
        """
        ii) Array types

        f: Array of 4 byte single-precision IEEE 754 number
        d: Array of 8 byte double-precision IEEE 754 number
        l: Array of 8 byte signed Integer
        i: Array of 4 byte signed Integer
        b: Array of 1 byte Booleans (always 0 or 1)

        For array types, Data is more complex:

            Size (Bytes) 	Data Type 	Name
            4 	Uint32 	ArrayLength
            4 	Uint32 	Encoding
            4 	Uint32 	CompressedLength
            ? 	? 	Contents

        If Encoding is 0, the Contents is just ArrayLength times the array data type. If Encoding is 1, the Contents is a deflate/zip-compressed buffer of length CompressedLength bytes. The buffer can for example be decoded using zlib.

        Values other than 0,1 for Encoding have not been observed.
        """
        arrayLength: DataViewResult      = self.readUInt32(offset)
        encoding: DataViewResult         = self.readUInt32(arrayLength.endOffset)
        compressedLength: DataViewResult = self.readUInt32(encoding.endOffset)
        content: bytearray               = self.targetBuffer[compressedLength.endOffset:compressedLength.endOffset+compressedLength.value]
        
        contentView: FBXPropertyParser;
        if encoding.value == 0: 
            contentView = FBXPropertyParser(content)
        elif encoding.value == 1: 
            contentView = FBXPropertyParser(zlib.decompress(content))
        else: 
            raise ValueError("Invalid encoding. 0/1 allowed")
        
        output = []
        contentOffset = 0
        primitiveTypeCode = (typeCode if typeCode != "b" else "c").upper()
        current: DataViewResult = None
        for _ in range(arrayLength.value): 
            current = contentView.__parsePrimitiveType(contentOffset, primitiveTypeCode)
            contentOffset = current.endOffset
            output.append(current.value)
        
        return DataViewResult(output, offset, offset+(compressedLength.endOffset+compressedLength.value)+current.endOffset)
        
    
    def __parseSpecialType(self: 'FBXPropertyParser', offset: int, typeCode:str) -> DataViewResult: 
        """
        iii) Special types
        
        S: String
        R: raw binary data
        
        Both of these have the following interpretation:

            Size (Bytes) 	Data Type 	Name
            4 	Uint32 	Length
            Length 	byte/char 	Data

        The string is not zero-terminated, and may well contain \0 characters (this is actually used in some FBX properties).

        """
        if typeCode == "S": # String 
            length = self.readUInt32(offset)
            return self.readString(length.endOffset, length.value)
        elif typeCode == "R": # raw binary data
            length = self.readUInt32(offset)
            offset = length.endOffset
            
            return DataViewResult(self.targetBuffer[offset:offset+length.value], offset, offset+length.value)