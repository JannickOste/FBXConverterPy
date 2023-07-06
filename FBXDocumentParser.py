import struct
import zlib
from Components.FBXDocumentHeader import FBXDocumentHeader

from Components.FBXDocumentNode import FBXDocumentNode
from Components.FBXDocument import FBXDocument

class DataViewResult:
    __value = None 
    __startOffset = -1
    __endOffset = -1
    
    def __init__(self, value, startOffset: int, endOffset: int) -> None:
        self.__value = value 
        self.__startOffset = startOffset
        self.__endOffset = endOffset
    
    @property
    def value(self):
        """ The value retrieved from the buffer """
        return self.__value 
    
    @property
    def startOffset(self):
        """ The position where the record has been read """
        return self.__startOffset
    
    @property
    def endOffset(self): 
        """ The position after the record (i.e. the first byte of whatever comes next) """
        return self.__endOffset

class DataView:
    __buffer: bytes

    def __init__(self, buffer: bytes) -> None:
        self.__buffer = buffer
        
        
    @property
    def targetBuffer(self) -> bytes: 
        return self.__buffer

    def readByTypeCode(self, offset: int, type_code: str) -> tuple:
        # Same implementation as in the original code
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

    def readInt16(self, offset: int) -> DataViewResult:
        """ 2 byte signed Integer """
        value, end_offset = self.readByTypeCode(offset, "Y")
        return DataViewResult(value, offset, end_offset)

    def readBoolean(self, offset: int) -> DataViewResult:
        """ 1 bit boolean (1: true, 0: false) encoded as the LSB of a 1 Byte value. """
        value, end_offset = self.readByTypeCode(offset, "C")
        return DataViewResult(value, offset, end_offset)

    def readInt32(self, offset: int) -> DataViewResult:
        """ 4 byte signed Integer """
        value, end_offset = self.readByTypeCode(offset, "I")
        return DataViewResult(value, offset, end_offset)

    def readInt64(self, offset: int) -> DataViewResult:
        """ 8 byte signed Integer """
        value, end_offset = self.readByTypeCode(offset, "L")
        return DataViewResult(value, offset, end_offset)
    
    def readUint8t(self, offset: int) -> DataViewResult: 
        value, end_offset = self.readByTypeCode(offset, "B")
        return DataViewResult(value, offset, end_offset)

    def readFloat(self, offset: int) -> DataViewResult:
        """ 4 byte single-precision IEEE 754 number """
        value, end_offset = self.readByTypeCode(offset, "F")
        return DataViewResult(value, offset, end_offset)

    def readDouble(self, offset: int) -> DataViewResult:
        """ 8 byte double-precision IEEE 754 number """
        value, end_offset = self.readByTypeCode(offset, "D")
        return DataViewResult(value, offset, end_offset)
    
    def readString(self, offset: int, length: int):
        return DataViewResult(self.__buffer[offset:offset+length].decode("latin-1"), offset, offset+length)
    
    def readChar(self, offset:int) -> DataViewResult:
        return DataViewResult(chr(self.__buffer[offset]), offset, offset+1)
 
      

class FBXDocumentParser: 
    parent = None
    __buffer: bytes; 
    __topLevelContentReader: DataView;
    __headerContentReader: DataView;
    
    def __init__(self, buffer: bytes) -> None:
        self.__buffer = buffer
        self.__topLevelContentReader = DataView(buffer[27:])
        self.__headerContentReader = DataView(buffer[:27])
    
    @property
    def __nodeBuffer(self):
        return self.__buffer[27:]
    
        
    def __parseHeader(self): 
        return FBXDocumentHeader(
            self.__headerContentReader.readString(0, 20).value,
            self.__headerContentReader.targetBuffer[21:23],
            self.__headerContentReader.readInt32(23).value
        )

    def __parseNodes(self, offset = 0, document = None) -> FBXDocumentNode: 
        if(offset >= len(self.__nodeBuffer)):
            return document
        
        startOffset = offset
        endOffset, numProps, propsLen, name, offset, properties = self.__readNodeRecord(offset)
        document = FBXDocumentNode(startOffset, endOffset, numProps, propsLen, name, properties, document)
        
        self.__printDebugInfo(document, offset)
            
        return self.__parseNodes(offset, document)
            
    def __printDebugInfo(self, node: FBXDocumentNode, offset: int): 
        for [key, value] in {
            "endOffset": node.endOffset, "numProperties": node.propertiesCount, "propertiesLength": node.propertiesLength, "name": node.name
        }.items():
            print(key, ':', value)
        
        if node.propertiesCount > 0: 
            print('properties:')
            for property in node.properties:
                print("\t- ", property)
        
        print(''.join(['-' for _ in range(20)]))
                
    
        
    def __readNodeRecord(self, offset):
        endOffset, numProperties, propertyListLen = [self.__topLevelContentReader.readInt32((offset+(i*4))) for i in range(3)]
        nameLen = self.__topLevelContentReader.readUint8t(propertyListLen.endOffset)
        name = self.__topLevelContentReader.readString(nameLen.endOffset, nameLen.value)
        offset = name.endOffset
        
        properties = []
        if numProperties.value:
            for _ in range(numProperties.value):
                typeCode = self.__topLevelContentReader.readChar(offset)
                result = self.__topLevelContentReader.readByTypeCode(typeCode.endOffset, typeCode.value)
                if result is None:
                    continue
                
                offset = result[1]
                properties.append(result[0])
            
        
        return [
            endOffset.value, numProperties.value, propertyListLen.value, name.value, offset, properties
        ]

    @staticmethod 
    def fromBuffer(buffer: bytes) -> FBXDocument: 
        parser = FBXDocumentParser(buffer)
        
        return FBXDocument(
            parser.__parseHeader(),
            parser.__parseNodes()
        )


    
        
   
        
    # def __read_property_value(self, offset: int, type_code: str, buffer: bytes):
    #     if type_code == "Y": # Y: 2 byte signed Integer
    #         value = struct.unpack("<h", buffer[offset:offset+2])[0]
    #         return value, offset + 2
    #     elif type_code == "C": # C: 1 bit boolean (1: true, 0: false) encoded as the LSB of a 1 Byte value.
    #         value = bool(buffer[offset])
    #         return value, offset + 1
    #     elif type_code == "I": # I: 4 byte signed Integer
    #         value = struct.unpack("<i", buffer[offset:offset+4])[0]
    #         return value, offset + 4
    #     elif type_code == "F": # F: 4 byte single-precision IEEE 754 number
    #         value = struct.unpack("<f", buffer[offset:offset+4])[0]
    #         return value, offset + 4
    #     elif type_code == "D": # D: 8 byte double-precision IEEE 754 number
    #         value = struct.unpack("<d", buffer[offset:offset+8])[0]
    #         return value, offset + 8
    #     elif type_code == "L": # L: 8 byte signed Integer
    #         value = struct.unpack("<q", buffer[offset:offset+8])[0]
    #         return value, offset + 8
    #     elif type_code == "f" or type_code == "d" or type_code == "l" or type_code == "i" or type_code == "b":
    #         array_length = struct.unpack("<I", buffer[offset:offset+4])[0]
    #         encoding = struct.unpack("<I", buffer[offset+4:offset+8])[0]
    #         compressed_length = struct.unpack("<I", buffer[offset+8:offset+12])[0]
    #         contents = buffer[offset+12:offset+12+compressed_length]

    #         if encoding == 0:
    #             if type_code == "f": # f: Array of 4 byte single-precision IEEE 754 number
    #                 array = struct.unpack("<" + "f" * array_length, contents)
    #             elif type_code == "d": # d: Array of 8 byte double-precision IEEE 754 number
    #                 array = struct.unpack("<" + "d" * array_length, contents)
    #             elif type_code == "l": # l: Array of 8 byte signed Integer
    #                 array = struct.unpack("<" + "q" * array_length, contents)
    #             elif type_code == "i": # i: Array of 4 byte signed Integer
    #                 array = struct.unpack("<" + "i" * array_length, contents)
    #             elif type_code == "b": # b: Array of 1 byte Booleans (always 0 or 1)
    #                 array = struct.unpack("<" + "b" * array_length, contents)

    #             return array, offset + 12 + compressed_length
    #         elif encoding == 1:
    #             uncompressed_data = zlib.decompress(contents)
    #             if type_code == "f": # f: Array of 4 byte single-precision IEEE 754 number
    #                 array = struct.unpack("<" + "f" * array_length, uncompressed_data)
    #             elif type_code == "d": # d: Array of 8 byte double-precision IEEE 754 number
    #                 array = struct.unpack("<" + "d" * array_length, uncompressed_data)
    #             elif type_code == "l": # l: Array of 8 byte signed Integer
    #                 array = struct.unpack("<" + "q" * array_length, uncompressed_data)
    #             elif type_code == "i": # i: Array of 4 byte signed Integer
    #                 array = struct.unpack("<" + "i" * array_length, uncompressed_data)
    #             elif type_code == "b": # b: Array of 1 byte Booleans (always 0 or 1)
    #                 array = struct.unpack("<" + "b" * array_length, uncompressed_data)

    #             return array, offset + 12 + compressed_length
            