from Domain.Entities.Document.FBXDocumentHeader import FBXDocumentHeader
from Domain.Entities.Document.FBXDocumentNode import FBXDocumentNode
from Domain.Entities.Document.FBXDocument import FBXDocument
from Domain.Entities.DataView.DataView import DataView
from Domain.Entities.DataView.DataViewInterface import DataViewInterface
from Infrastructure.Parser.FBXPropertyParser import FBXPropertyParser


class FBXDocumentParser:
    """
    Parser for FBX documents.

    Args:
        buffer (bytes): The FBX file buffer.

    """

    __contentParser: DataViewInterface

    def __init__(self: 'FBXDocumentParser', buffer: bytes) -> None:
        self.__contentParser = FBXPropertyParser(buffer)

    def __parseHeader(self: 'FBXDocumentParser') -> FBXDocumentHeader:
        """
        Parse the FBX document header.

        Returns:
            FBXDocumentHeader: The parsed FBX document header.

        """
        return FBXDocumentHeader(
            self.__contentParser.readString(0, 20).value,
            self.__contentParser.targetBuffer[21:23],
            self.__contentParser.readUInt32(23).value
        )

    def __parseNodes(self: 'FBXDocumentParser', offset=0, document=None) -> FBXDocumentNode:
        """
        Recursively parse the FBX document nodes.

        Args:
            offset (int): The offset in bytes where the node data starts.
            document (FBXDocumentNode): The parent document node.

        Returns:
            FBXDocumentNode: The parsed FBX document node.

        """
        if offset >= len(self.__contentParser.targetBuffer):
            return document

        startOffset = offset
        endOffset, numProps, propsLen, name, offset, properties = self.__readNodeRecord(offset)
        document = FBXDocumentNode(startOffset, endOffset, numProps, propsLen, name, properties, document)

        return self.__parseNodes(offset, document)

    def __readNodeRecord(self: 'FBXDocumentParser', offset: int):
        """
        Read a node record from the FBX file.

        Args:
            offset (int): The offset in bytes where the node record starts.

        Returns:
            tuple: A tuple containing the end offset, number of properties, property list length, name, current offset,
            and the list of properties.

        """
        endOffset, numProperties, propertyListLen = [self.__contentParser.readInt32((offset + (i * 4))) for i in range(3)]
        nameLen = self.__contentParser.readUChar(propertyListLen.endOffset)
        name = self.__contentParser.readString(nameLen.endOffset, nameLen.value)
        offset = name.endOffset

        properties = []
        if numProperties.value:
            for _ in range(numProperties.value):
                typeCode: DataViewInterface = self.__contentParser.readChar(offset)
                result = self.__contentParser.readByTypeCode(typeCode.endOffset, typeCode.value)

                offset = result.endOffset
                properties.append(result.value)

        return endOffset.value, numProperties.value, propertyListLen.value, name.value, offset, properties

    @staticmethod
    def fromBuffer(buffer: bytes) -> FBXDocument:
        """
        Create an FBX document from a buffer.

        Args:
            buffer (bytes): The FBX file buffer.

        Returns:
            FBXDocument: The parsed FBX document.

        """
        parser = FBXDocumentParser(buffer)

        return FBXDocument(
            parser.__parseHeader(),
            parser.__parseNodes(27)
        )
