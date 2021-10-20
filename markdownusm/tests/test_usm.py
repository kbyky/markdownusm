#!/usr/bin/env python

import pytest
from markdownusm.usm import Usm
from markdownusm.xml import Rectangle


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            [
                dict(text="Activity1", x=0, y=0),
                dict(text="Activity2", x=1, y=0),
            ],
            [
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
            ],
        )
    ],
)
def test_to_activity(source, expected):
    actual = Usm(source=source).to_activities()
    assert actual == expected


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            [
                dict(text="Story 1", x=0, y=0),
            ],
            {
                "text": "Story 1",
                "x": "0",
                "y": "0",
                "fontColor": "#5F5F63",
                "fillColor": "#ebf4fa",
            },
        )
    ],
)
def test_set_story_properties(source, expected):
    usm = Usm(source=source)
    actual = usm._set_story_properties(usm.source[0])
    assert actual == expected


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            [
                dict(text="Story 2!", x=1, y=0),
            ],
            {
                "text": "Story 2",
                "x": "1",
                "y": "0",
                "fontColor": "#5F5F63",
                "fillColor": "#f8d7da",
            },
        )
    ],
)
def test_set_story_properties_warning(source, expected):
    usm = Usm(source=source)
    actual = usm._set_story_properties(usm.source[0])
    assert actual == expected


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            [
                dict(text="Story 1", x=0, y=0),
                dict(text="Story 2!", x=1, y=0),
            ],
            [
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
            ],
        )
    ],
)
def test_to_stories(source, expected):
    actual = Usm(source=source).to_stories()
    assert actual == expected
