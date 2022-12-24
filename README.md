# PyMaid

## What is this?
PyMaid is a tool to automatically generate MermaidJS class diagrams from python3 source code. PyMaid uses the native `ast` module to parse a raw text stream of `.py` files and generate the proper syntax for MermaidJS [class diagrams](https://mermaid.js.org/syntax/classDiagram.html). PyMaid is a work in progress and is not yet ready for production use. 

## Details
PyMaid's goal is to be hackable and provide a starting point for future extensions. We are open to contributions and feature requests. We aim to keep PyMaid simple and portable by having 0 external dependencies. 

## Usage
```bash
> python3 pymaid.py <file-path>
```

## Example

![](samples/shapes.png)  
```python
> python3 pymaid.py samples/shapes.py
# generated test.md
classDiagram
  Point3D --o float
  Shape3D <|-- Triangle
  Shape3D <|-- Quadrilateral
  Line3D --o Point3D
  Line3D <|-- Polyline
  Line3D <|-- BezierCurve
...
```

## Limitations
PyMaid is still in development and has a few limitations:
- PyMaid works best when methods are type hinted.
- We cannot yet guarantee comprehensive styling of `UML` relationships.
- Using the native `ast` module provides some robustness over a pattern-matching approach. However, more testing it needed to verify code coverage.

Read more about MermaidJS [here](https://mermaid.js.org/). It is an excellent tool.