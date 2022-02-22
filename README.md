# MarkdownUSM
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![CircleCI](https://circleci.com/gh/kbyky/markdownusm/tree/main.svg?style=shield&circle-token=33d038de0f7a2600f831702d67d7887b71f77eea)](https://circleci.com/gh/kbyky/markdownusm/tree/main)
[![codecov](https://codecov.io/gh/kbyky/markdownusm/branch/main/graph/badge.svg?token=ZD51BWEICH)](https://codecov.io/gh/kbyky/markdownusm)
[![Supported Versions](https://img.shields.io/pypi/pyversions/markdownusm.svg)](https://pypi.org/project/markdownusm)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

MarkdownUSM is the best way to draw a beautiful user story mapping diagram from simple markdown file.\
Markdown file will be converted to XML format then you can easily use the diagram on [draw.io](https://app.diagrams.net) and export in another format.

![](https://github.com/kbyky/public/blob/main/img/markdownusm.svg?raw=true)

## Installation
```
$ pip install markdownusm
```

## Examples

### Create it

Create a file sample.md with:

```
<!-- Comment -->

<!-- Release titles -->
- Release 1
- Release 2
- Release 3
- Release 4
- Release 5

# Activity 1
## Task 1
Story 1
--- <!-- Release separator -->
Story 2
---
Story 3

## Task 2
---
Story 4

<!-- Suffix `!` changes story postit color for warning -->
Story 5!

<!--
Multiple line comments
-->
# Activity 2
## Task 3
---
---
Story 6 &lt;br&gt; Next line
<!-- Story can change their colors by setting hex code following story title -->
Story 7 #a6dfb5
```

### Run it

The simplest way with:

```
$ musm sample.md

<mxfile>
    <diagram>
        <mxGraphModel dx="661" dy="316" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0" background="#FFFFFF">
        ...
```

Output XML file with:
```
$ musm -o sample.dio sample.md
```

## License
This project is licensed under the terms of the MIT license.
