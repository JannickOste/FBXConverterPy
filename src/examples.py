
from Domain.Entities.Document.FBXDocument import FBXDocument
from Infrastructure.Parser.FBXDocumentParser import FBXDocumentParser

def printNames(document: FBXDocument): 
    current = document.topLevelDocument
    names = []
    while current is not None:
        names.append(current.name)
        current = current.parent
    print(", ".join(names))
    

def extractName(document: FBXDocument, name:str = "Vertices"): 
    out = None
    current = document.topLevelDocument
    while current is not None and out is None:
        if current.name == name:
            out = current
            print(out.startOffset)
            print(out.endOffset)
        
        current = current.parent
        
    
def dump(node: FBXDocument, count: int):
    current = node.topLevelDocument
    for i in range(count):
        print("name", current.name)
        print("endOffset", current.endOffset)
        print("propertiesCount", current.propertiesCount)
        print("propertiesLength", current.propertiesLength)
        print("nameLength", len(current.name))
        print("properties", current.properties)
        current = current.parent

if __name__ == "__main__":
    document = None
    with open("/home/jannick/Workspace/Python/FBXConverter/assets/example.fbx", "rb") as file: 
        document = FBXDocumentParser.fromBuffer(file.read())
        file.close()
    
    dump(document, 5)