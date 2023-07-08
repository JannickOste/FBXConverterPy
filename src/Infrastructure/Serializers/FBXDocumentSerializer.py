import json
from typing import Any
from Domain.Entities.Document.FBXDocument import FBXDocument, FBXDocumentNode, FBXDocumentHeader

class FBXDocumentSerializer(json.JSONEncoder):
    """
    Serializer for FBX documents to JSON.

    """

    def default(self: "FBXDocumentSerializer", obj: Any):
        """
        Override the default JSON encoder to handle specific types.

        Args:
            obj (Any): The object to serialize.

        Returns:
            Any: The serialized object.

        """
        if isinstance(obj, bytes):
            return obj.hex()
        elif isinstance(obj, (FBXDocument, FBXDocumentHeader, FBXDocumentNode)):
            return self.__serializeObject(obj)
        return super().default(obj)

    def __serializeObject(self: "FBXDocumentSerializer", target: Any, filterKeys: list[str] = []) -> dict:
        """
        Serialize an object to a dictionary.

        Args:
            target (Any): The object to serialize.
            filterKeys (list[str], optional): A list of keys to filter out. Defaults to [].

        Returns:
            dict: The serialized object as a dictionary.

        """
        serialized = {}
        for key, value in target.__dict__.items():
            key = key.split("__")[-1]

            if isinstance(value, (FBXDocument, FBXDocumentHeader, FBXDocumentNode)):
                value = self.__serializeObject(value, filterKeys)

            serialized[key] = value

        return serialized

    @staticmethod
    def serialize(target: FBXDocument) -> str:
        """
        Serialize the FBXDocument object to a JSON string.

        Args:
            target (FBXDocument): The FBX document to serialize.

        Returns:
            str: The JSON representation of the FBXDocument.

        Raises:
            AssertionError: If the target is None.

        """
        assert target is not None

        return json.dumps(
            {
                'header': target.header,
                'document': target.topLevelDocument,
            },
            cls=FBXDocumentSerializer
        )
