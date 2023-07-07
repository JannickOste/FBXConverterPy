from Components.FBXDocumentHeader import FBXDocumentHeader

from Components.FBXDocumentNode import FBXDocumentNode
from Components.FBXDocument import FBXDocument
from DataView.DataView import DataView

      

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
    
        device
    def __parseHeader(self): 
        return FBXDocumentHeader(
            self.__headerContentReader.readString(0, 20).value,
            self.__headerContentReader.targetBuffer[21:23],
            self.__headerContentReader.readInt32(23).value
        )

    def __parseNodes(self, offset = 0, document = None) -> FBXDocumentNode: 
        if(offset >= len(self.__topLevelContentReader.targetBuffer)):
            return document
        startOffset = offset
        endOffset, numProps, propsLen, name, offset, properties = self.__readNodeRecord(offset)
        document = FBXDocumentNode(startOffset, endOffset, numProps, propsLen, name, properties, document)
        
        self.__printDebugInfo(document, offset)
            
        return self.__parseNodes(offset, document)
            
    def __printDebugInfo(self, node: FBXDocumentNode, offset: int): 
        for [key, value] in {
            "startOffset": node.startOffset,
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
                    
                    print(typeCode.value, typeCode.endOffset)
                    raise Exception("Woeps this shouldnt be the case")
                    
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
            