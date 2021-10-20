#!/usr/bin/env python

from markdownusm.xml import Line, Rectangle


def test_rectangle():
    expected = "html=1;rounded=0;whiteSpace=wrap;fillColor=#000000;strokeColor=none;fontColor=#000000;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1"
    actual = Rectangle(
        text="test", x=100, y=100, fillColor="#000000", fontColor="#000000"
    )._style()

    assert actual == expected


def test_lint():
    expected = "html=1;endArrow=none;shadow=0;strokeWidth=2;strokeColor=#000000"
    actual = Line(text="text", x=100, y=100, width=100)._style()

    assert actual == expected


def test__geometry():
    expected = 'x="0.0" y="0.0" width="140" height="60"'
    actual = Rectangle(text="", x=0, y=0, fillColor="", fontColor="")._geometry()

    assert actual == expected
