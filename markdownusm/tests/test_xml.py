#!/usr/bin/env python

from markdownusm.xml import Line, Rectangle


def test_rectangle():
    rect = Rectangle(
        text="test", x=100, y=100, fillColor="#000000", fontColor="#000000"
    )
    tested = rect._style()
    assert (
        tested
        == "html=1;rounded=0;whiteSpace=wrap;fillColor=#000000;strokeColor=none;fontColor=#000000;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1"
    )

    tested = rect._geometry()
    assert tested == 'x="100.0" y="100.0" width="140" height="60"'


def test_lint():
    line = Line(text="text", x=100, y=100, width=100)
    tested = line._style()

    assert tested == "html=1;endArrow=none;shadow=0;strokeWidth=2;strokeColor=#000000"
