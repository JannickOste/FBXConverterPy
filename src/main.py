import sys
import os
from Domain.Entities.Document.FBXDocument import FBXDocument

from Infrastructure.Serializers.FBXDocumentSerializer import FBXDocumentSerializer
from Infrastructure.Parser.FBXDocumentParser import FBXDocumentParser

class FBXConverter: 
    @staticmethod 
    def __printProgramInfo() -> None: 
        header = "FBX to JSON - By Oste Jannick"
        size = len(header)
        
        print("{top}\n| {text} |\n{bottom}\n".format(
            top = "-"*(size+4),
            text = header,
            bottom = "-"*(size+4),
        ))
        
        
        
    @staticmethod
    def __init(*args: list[str]) -> dict:
        if len(args) < 1: 
            raise Exception("Source argument not found...")
        elif len(args)< 2:
            raise Exception("Output filepath not found...")
        
        if not os.path.exists(args[0]):
            raise Exception("Source file does not exists...")
 
 
        return {
            "source": args[0],
            "target": args[1]
        }
    
    def __act(**kwargs) -> None:
        document: FBXDocument = None
        output: str = ''
        with open(kwargs["source"], "rb") as file:
            try:
                document = FBXDocumentParser.fromBuffer(file.read())
                output = FBXDocumentSerializer.serialize(document)
            except Exception as e:
                raise e
            finally: 
                if not file.closed:
                    file.close()
        
        with open(kwargs["target"], "w+") as file: 
            file.write(output)
            file.close()
        print("Object succesfully serialized")
        
    @staticmethod 
    def main(*args: list[str]): 
        FBXConverter.__printProgramInfo()
        try:
            kwargs = FBXConverter.__init(*args)
        except Exception as e: 
            print(e)
        finally:
            if not len(kwargs):
                sys.exit(-1)
            
            FBXConverter.__act(**kwargs)

    
        
    

if __name__ == '__main__': 
    FBXConverter.main(*sys.argv[1:])
