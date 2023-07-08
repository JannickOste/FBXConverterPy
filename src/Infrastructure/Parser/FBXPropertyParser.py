import zlib
from Domain.Entities.DataView.DataView import DataView
from Domain.Entities.DataView.DataViewResult import DataViewResult

class FBXPropertyParser(DataView):
    def readByTypeCode(self: 'FBXPropertyParser', offset: int, typeCode: str) -> DataViewResult:
        """
        Read a property from the FBX file based on its type code.

        Args:
            offset (int): The offset in bytes where the property data starts.
            typeCode (str): The type code representing the property type.

        Returns:
            DataViewResult: The parsed property data.

        Raises:
            ValueError: If the type code is unknown.

        """

        out: DataViewResult = None

        if ["Y", "C", "I", "F", "D", "L", "B"].count(typeCode) > 0:
            out = self.__parsePrimitiveType(offset, typeCode)
        elif ["f", "d", "l", "i", "b"].count(typeCode) > 0:
            out = self.__parseArrayType(offset, typeCode)
        elif ["S", "R"].count(typeCode) > 0:
            out = self.__parseSpecialType(offset, typeCode)

        if out is None:
            raise ValueError(f"Unknown type code: {typeCode}")

        return out

    def __parsePrimitiveType(self: 'FBXPropertyParser', offset: int, typeCode: str) -> DataViewResult:
        """
        Parse a primitive type property from the FBX file.

        Args:
            offset (int): The offset in bytes where the property data starts.
            typeCode (str): The type code representing the property type.

        Returns:
            DataViewResult: The parsed property data.

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

    def __parseArrayType(self: 'FBXPropertyParser', offset: int, typeCode: str) -> DataViewResult:
        """
        Parse an array type property from the FBX file.

        Args:
            offset (int): The offset in bytes where the property data starts.
            typeCode (str): The type code representing the property type.

        Returns:
            DataViewResult: The parsed property data.

        Raises:
            ValueError: If the encoding is invalid.

        """
        arrayLength: DataViewResult = self.readUInt32(offset)
        encoding: DataViewResult = self.readUInt32(arrayLength.endOffset)
        compressedLength: DataViewResult = self.readUInt32(encoding.endOffset)
        content: bytearray = self.targetBuffer[compressedLength.endOffset:compressedLength.endOffset + compressedLength.value]

        contentView: FBXPropertyParser
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

        return DataViewResult(output, offset, offset + (compressedLength.endOffset + compressedLength.value) + current.endOffset)

    def __parseSpecialType(self: 'FBXPropertyParser', offset: int, typeCode: str) -> DataViewResult:
        """
        Parse a special type property from the FBX file.

        Args:
            offset (int): The offset in bytes where the property data starts.
            typeCode (str): The type code representing the property type.

        Returns:
            DataViewResult: The parsed property data.

        """
        length: DataViewResult = None

        if typeCode == "S":  # String
            length = self.readUInt32(offset)
            return self.readString(length.endOffset, length.value)
        elif typeCode == "R":  # raw binary data
            length = self.readUInt32(offset)
            offset = length.endOffset

        return DataViewResult(self.targetBuffer[offset:offset + length.value], offset, offset + length.value)
