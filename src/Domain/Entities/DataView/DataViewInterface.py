import abc
from typing import Any
from Domain.Entities.DataView.DataViewResult import DataViewResult


class DataViewInterface(abc.ABC):
    @abc.abstractproperty
    def targetBuffer(self) -> bytes:
        """ Get the target buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: targetBuffer() not implemented.")

    @abc.abstractmethod
    def readChar(self, offset: int) -> DataViewResult:
        """ Read a character from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readChar() not implemented.")

    @abc.abstractmethod
    def readSChar(self, offset: int) -> DataViewResult:
        """ Read a signed character from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readSChar() not implemented.")

    @abc.abstractmethod
    def readUChar(self, offset: int) -> DataViewResult:
        """ Read an unsigned character from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readUChar() not implemented.")

    @abc.abstractmethod
    def readBool(self, offset: int) -> DataViewResult:
        """ Read a boolean value from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readBool() not implemented.")

    @abc.abstractmethod
    def readShort(self, offset: int) -> DataViewResult:
        """ Read a 2-byte signed integer from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readShort() not implemented.")

    @abc.abstractmethod
    def readUShort(self, offset: int) -> DataViewResult:
        """ Read a 2-byte unsigned integer from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readUShort() not implemented.")

    @abc.abstractmethod
    def readInt32(self, offset: int) -> DataViewResult:
        """ Read a 4-byte signed integer from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readInt32() not implemented.")

    @abc.abstractmethod
    def readUInt32(self, offset: int) -> DataViewResult:
        """ Read a 4-byte unsigned integer from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readUInt32() not implemented.")

    @abc.abstractmethod
    def readLong(self, offset: int) -> DataViewResult:
        """ Read a 4-byte signed integer (long) from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readLong() not implemented.")

    @abc.abstractmethod
    def readULong(self, offset: int) -> DataViewResult:
        """ Read a 4-byte unsigned integer (ulong) from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readULong() not implemented.")

    @abc.abstractmethod
    def readInt64(self, offset: int) -> DataViewResult:
        """ Read an 8-byte signed integer (int64) from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readInt64() not implemented.")

    @abc.abstractmethod
    def readUInt64(self, offset: int) -> DataViewResult:
        """ Read an 8-byte unsigned integer (uint64) from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readUInt64() not implemented.")

    @abc.abstractmethod
    def readFloat(self, offset: int) -> DataViewResult:
        """ Read a 4-byte single-precision floating-point number (float) from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readFloat() not implemented.")

    @abc.abstractmethod
    def readDouble(self, offset: int) -> DataViewResult:
        """ Read an 8-byte double-precision floating-point number (double) from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readDouble() not implemented.")

    @abc.abstractmethod
    def readString(self, offset: int, length: int, encoding: str = "latin-1") -> DataViewResult:
        """ Read a string from the buffer. """
        raise NotImplementedError(f"{self.__class__.__name__}: readString() not implemented.")
