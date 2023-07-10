# FBXConverterPy

![](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=yellow)
![](https://img.shields.io/badge/current_state-working-21a62a?style=for-the-badge)

(library currently in working but some sections are still missing, null record handling and nestedlist support not currently added)

Python library for parsing and working with FBX (Filmbox) files. FBX is a binary file format used for storing 3D models, animations, and other related data in the computer graphics industry.

This is a project aimed to be an introduction to the FBX file standard, so this project will <u>not</u> be long term updated once the primary goals have been achieved. 

The library provides classes and functions to read and extract information from FBX files, including the file header, document structure, nodes, and properties. It aims to simplify the process of working with FBX files and enable developers to integrate FBX functionality into their applications.

## Key Components:
<ol type="1">
    <li><b>FBXDocumentHeader:</b> Represents the header of an FBX file, containing information such as the file magic, null bytes, and version number.</li>
    <li><b>FBXDocumentNode:</b> Represents a node within the FBX document hierarchy, containing properties and child nodes.</li>
    <li><b>FBXDocument:</b> Represents the overall FBX document, consisting of the file header and the top-level document node.</li>
</ol>

The library utilizes a DataView class for efficient byte-level data reading and manipulation. It supports various data types, including strings, integers, floats, and arrays.

The project is currently a work in progress and aims to provide a comprehensive set of features for working with FBX files. It will support parsing and serialization of FBX data, enabling users to read, modify, and create FBX files programmatically.

Please note that this project is not affiliated with Autodesk, the creator of FBX. It is an independent effort to provide a Python-based solution for FBX file handling.

## Project Goals:
<ol type="1">
    <li>Parse and extract information from FBX files.</li>
    <li>Provide an object-oriented interface for working with FBX data.</li>
    <li>Support reading and writing of FBX files.</li>
    <li>Enable modification and creation of FBX files programmatically.</li>
    <li>Provide documentation and examples to assist developers in using the library.</li>
    <li>Ensure compatibility with different versions of FBX files</li>
    <li>JSON Serialization and deserialization.</li>
</ol>

## Usage Example:
```
# Parse an FBX file
with open('example.fbx', 'rb') as file:
    fbx_data = file.read()

fbx_document = FBXDocumentParser.fromBuffer(fbx_data)

# Access the file header
header = fbx_document.header
print("FBX Version:", header.versionNumber)

# Access the top-level document node
top_level_node = fbx_document.topLevelDocument

# Traverse the document hierarchy
def traverse_nodes(node, indent=0):
    print(' ' * indent + node.name)
    for child in node.children:
        traverse_nodes(child, indent + 4)

traverse_nodes(top_level_node)
```