
from Domain.Entities.DataView.DataView import DataView
from Domain.Entities.DataView.DataViewResult import DataViewResult


class FBXPropertyParser(DataView):
    def readByTypeCode(self, offset: int, type_code: str) -> DataViewResult:
        if type_code == "Y":
            return self.readShort(offset)
        elif type_code == "C":
            return self.readBool(offset)
        elif type_code == "I":
            return self.readInt32(offset)
        elif type_code == "F":
            return self.readFloat(offset)
        elif type_code == "D":
            return self.readDouble(offset)
        elif type_code == "L":
            return self.readInt64(offset)
        elif type_code == "B":
            return self.readUShort(offset)
        elif type_code == "S":
            length = self.readUInt32(offset)
            value = self.readString(length.endOffset, length.value)
            
            return value
        else:
            raise ValueError(f"Unknown type code: {type_code}")
        