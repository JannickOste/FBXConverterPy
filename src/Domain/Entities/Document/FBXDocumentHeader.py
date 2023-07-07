class FBXDocumentHeader:
    _fileMagic: str
    _nullBytes: bytes
    _versionNumber: int
    
    def __init__(self: 'FBXDocumentHeader', fileMagic: str, nullBytes: bytes, versionNumber: int) -> None:
        """
        Initialize an FBXDocumentHeader object.

        Args:
            fileMagic (str): The file magic string.
            nullBytes (bytes): The null bytes.
            versionNumber (int): The version number.
        """
        self._fileMagic = fileMagic
        self._versionNumber = versionNumber
        self._nullBytes = nullBytes
        
        self.__validateHeader()

    @property
    def fileMagic(self: 'FBXDocumentHeader') -> str:
        """
        Get the file magic string.

        Returns:
            str: The file magic string.
        """
        return self._fileMagic

    @property
    def nullBytes(self: 'FBXDocumentHeader') -> bytes:
        """
        Get the null bytes.

        Returns:
            bytes: The null bytes.
        """
        return self._nullBytes

    @property
    def versionNumber(self: 'FBXDocumentHeader') -> int:
        """
        Get the version number.

        Returns:
            int: The version number.
        """
        return self._versionNumber

    # TODO: Has to be moved to a voter extended class. 
    def __validateHeader(self: 'FBXDocumentHeader') -> None: 
        """
        Validate the fileMagic and nullBytes.

        Raises:
            AssertionError: If the fileMagic or nullBytes are not as expected.
        """
        assert [hex(ord(c)) for c in self.fileMagic] == ['0x4b', '0x61', '0x79', '0x64', '0x61', '0x72', '0x61', '0x20', '0x46', '0x42', '0x58', '0x20', '0x42', '0x69', '0x6e', '0x61', '0x72', '0x79', '0x20', '0x20']
        assert self.nullBytes == bytes([0x1a, 0x00])
