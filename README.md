# PyMaid

## What is this?
PyMaid is a tool to automatically generate MermaidJS class diagrams from `python3` source code. PyMaid uses the native `ast` module to parse a raw text stream of `.py` files and generate the proper syntax for MermaidJS [class diagrams](https://mermaid.js.org/syntax/classDiagram.html). 

*Please Note: PyMaid is a work in progress and is not yet ready for production use.* 

## Details
This tool was developed to be hackable and provide users with high-level visualizations of `python3` codebases. We are open to contributions and feature requests. 

## Setup & Installation
```bash
# ensure python3 is installed
> python3 --version
Python 3.8.3
# clone repo
> git clone https://github.com/solzilberman/pymaid.git pymaid_dir
> cd pymaid_dir
```

## Usage
```bash
# ~/pymaid_dir/
> python3 pymaid -h
usage: pymaid -i <input> [-o] <output>

PyMaid version 0.0.1

optional arguments:
  -h, --help      show this help message and exit
  -i , --input    Input file or glob
  -o , --output   Output file to write to
```
*Please Note: PyMaid is not yet packaged for pip installation. We intend to do this in the future.*

## Sample Usage
```bash
# ~/pymaid_dir/
> python3 pymaid samples/shapes.py
# out.md
classDiagram
  Point3D --o float
  Shape3D <|-- Triangle
  Shape3D <|-- Quadrilateral
  Line3D --o Point3D
  Line3D <|-- Polyline
  Line3D <|-- BezierCurve
...

```
*Rendered Mermaid Diagram:*

![](samples/shapes.png)  

## Limitations
PyMaid is still in development and has a few limitations:
- PyMaid works best when methods are type hinted.
- We cannot yet guarantee comprehensive styling of `UML` relationship arrows.
- Using the native `ast` module provides some robustness over a pattern-matching approach. However, more testing it needed to verify syntax coverage.

Read more about MermaidJS [here](https://mermaid.js.org/). It is an excellent tool.

### Alternatives:
- [pyreverse](https://pylint.pycqa.org/en/latest/pyreverse.html) is a production grade tool that can generate UML diagrams of `python3` codebases and comes shipped with recent versions of `pylint`. If you need accurate UML digrams, use pyreverse.
