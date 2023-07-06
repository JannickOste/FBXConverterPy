
import struct


class FBXDocumentHeader: 
    _fileMagic, _nullBytes, _versionNumber = [None, None, None]
    
    def __init__(self, _fileMagic, _nullBytes, _versionNumber) -> None:
        self._fileMagic     = _fileMagic
        self._versionNumber = _versionNumber
        self._nullBytes     = _nullBytes
        
        self.__validateHeader()

    @property
    def fileMagic(self) -> str:
        """Kaydara FBX Binary  \x00 (file-magic, with 2 spaces at the end, then a NULL terminator). Bytes 0 - 20"""
        return self._fileMagic

    @property
    def nullBytes(self) -> bytes:
        """[0x1A, 0x00] (unknown but all observed files show these bytes). Bytes 21-22"""
        return self._nullBytes

    @property
    def versionNumber(self) -> int:
        """Bytes 23 - 26: unsigned int, the version number. 7300 for version 7.3 for example."""
        return self._versionNumber

    def __validateHeader(self): 
        """ Validate the fileMagic and nullBytes, no checks for version number """
        assert [hex(ord(c)) for c in self.fileMagic] == ['0x4b', '0x61', '0x79', '0x64', '0x61', '0x72', '0x61', '0x20', '0x46', '0x42', '0x58', '0x20', '0x42', '0x69', '0x6e', '0x61', '0x72', '0x79', '0x20', '0x20']
        assert self.nullBytes == bytes([0x1a, 0x00])
