import sys
import os
from FBXDocumentParser import FBXDocumentParser

class FBXConverter: 
    __argv: list[str]; 
    
    @staticmethod
    def __init(*args) -> None:
        try:
            if len(args) < 1: 
                raise Exception("Source argument not found...");
            if not os.path.exists(args[0]):
                raise Exception("Source file not found");
        except Exception as e:
            print(e)
            sys.exit(-1)
        
        return {
            "filepath": args[0]
        }
        
    @staticmethod 
    def main(*args): 
        kwargs = FBXConverter.__init(*args)
        
        with open(kwargs["filepath"], "rb") as file:
            try:
                FBXDocumentParser.fromBuffer(file.read())
            except Exception as e:
                raise e
            finally: 
                if not file.closed:
                    file.close()
        
        
    

if __name__ == '__main__': 
    FBXConverter.main(*sys.argv[1:])
