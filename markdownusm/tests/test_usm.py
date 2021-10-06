#!/usr/bin/env python

from markdownusm.usm import Usm
from markdownusm.xml import Rectangle


def test_to_activity():
    source = [
        dict(text="Activity1", x=0, y=0),
        dict(text="Activity2", x=1, y=0),
    ]

    usm = Usm(source=source)
    tested = usm.to_activities()
    assert tested == [
        Rectangle(
            text="Activity1",
            y=50.0,
            x=290.0,
            fillColor="#1F568A",
            fontColor="#FFFFFF",
            height=60,
            width=140,
            rounded=0,
            white_space="wrap",
            strokeColor="none",
            horizontal_align="left",
            vertical_align="top",
            spacing_left=5,
            spacing_right=5,
            shadow=1,
        ),
        Rectangle(
            text="Activity2",
            y=50.0,
            x=450.0,
            fillColor="#1F568A",
            fontColor="#FFFFFF",
            height=60,
            width=140,
            rounded=0,
            white_space="wrap",
            strokeColor="none",
            horizontal_align="left",
            vertical_align="top",
            spacing_left=5,
            spacing_right=5,
            shadow=1,
        ),
    ]


def test_set_story_properties():
    source = [
        dict(text="Story 1", x=0, y=0),
        dict(text="Story 2!", x=1, y=0),
    ]

    usm = Usm(source=source)

    tested = usm._set_story_properties(usm.source[1])
    assert tested == {
        "text": "Story 2",
        "x": "1",
        "y": "0",
        "fontColor": "#5F5F63",
        "fillColor": "#f8d7da",
    }

    tested = usm._set_story_properties(usm.source[0])
    assert tested == {
        "text": "Story 1",
        "x": "0",
        "y": "0",
        "fontColor": "#5F5F63",
        "fillColor": "#ebf4fa",
    }


def test_to_stories():
    source = [
        dict(text="Story 1", x=0, y=0),
        dict(text="Story 2!", x=1, y=0),
    ]

    usm = Usm(source=source)

    tested = usm.to_stories()
    assert tested == [
        Rectangle(
            text="Story 1",
            y=50.0,
            x=290.0,
            fillColor="#ebf4fa",
            fontColor="#5F5F63",
            height=60,
            width=140,
            rounded=0,
            whiteSpace="wrap",
            strokeColor="none",
            align="left",
            verticalAlign="top",
            spacingLeft=5,
            spacingRight=5,
            shadow=1,
        ),
        Rectangle(
            text="Story 2",
            y=50.0,
            x=450.0,
            fillColor="#f8d7da",
            fontColor="#5F5F63",
            height=60,
            width=140,
            rounded=0,
            whiteSpace="wrap",
            strokeColor="none",
            align="left",
            verticalAlign="top",
            spacingLeft=5,
            spacingRight=5,
            shadow=1,
        ),
    ]
