from FBXDocumentParser import FBXDocumentParser


if __name__ == '__main__': 
    with open("./test.fbx", "rb") as file:
        FBXDocumentParser.fromBuffer(file.read())


