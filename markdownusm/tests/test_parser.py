#!/usr/bin/env python

import pytest
from markdownusm.parser import MarkdownParser


@pytest.fixture
def markdown():
    return """
- Release1
- Release2
- Release3

# Activity1
## Task1
Story1
## Task2
Story2

# Activity2
## Task3
---
Story3
    """


@pytest.fixture
def parser(markdown):
    return MarkdownParser(markdown=markdown)


def test_constructor(parser):
    assert len(parser.lines) == 12


def test_extract_tasks(parser):
    tested = parser.extract_tasks()
    assert tested == ["Task1", "Task2", "Task3"]


def test_extract_activities_with_tasks(parser):
    tested = parser.extract_activities_with_tasks()
    assert tested == {"Activity1": "Task1", "Activity2": "Task3"}


def test_extract_releases(parser):
    tested = parser.extract_releases()
    assert tested == ["Release1", "Release2", "Release3"]


def test_extract_tasks_and_stories(parser):
    tested = parser.extract_tasks_and_stories()
    assert tested == [
        "## Task1",
        "Story1",
        "## Task2",
        "Story2",
        "## Task3",
        "---",
        "Story3",
    ]


def test_divide_list_by_prefix(parser):
    target = ["Story1", "---", "Story2"]
    tested = parser._divide_list_by_prefix(target, "---")
    assert tested == [["Story1"], ["Story2"]]

    target = ["Story1", "## Task1", "Story2"]
    tested = parser._divide_list_by_prefix(target, "##")
    assert tested == [["Story1"], ["Story2"]]

    target = ["---", "Story", "Story"]
    tested = parser._divide_list_by_prefix(target, "---")
    assert tested == [[], ["Story", "Story"]]


def test_max_number_of_stories_in_each_release(parser):
    tested = parser.max_number_of_stories_in_each_release()
    assert tested == [1, 1]


def test_extract_activities_with_position(parser):
    tested = parser.extract_activities_with_position()
    assert tested == [
        {"text": "Activity1", "x": 0, "y": 0},
        {"text": "Activity2", "x": 2, "y": 0},
    ]


def test_extract_tasks_with_position(parser):
    tested = parser.extract_tasks_with_position()
    assert tested == [
        {"text": "Task1", "x": 0, "y": 1},
        {"text": "Task2", "x": 1, "y": 1},
        {"text": "Task3", "x": 2, "y": 1},
    ]


def test_extract_stories_with_position(parser):
    tested = parser.extract_stories_with_position()
    assert tested == [
        {"text": "Story1", "x": 0, "y": 2},
        {"text": "Story2", "x": 1, "y": 2},
        {"text": "Story3", "x": 2, "y": 3},
    ]


def test_extract_release_texts_with_position(parser):
    tested = parser.extract_release_texts_with_position()
    assert tested == [
        {"text": "Release1", "x": -1, "y": 2},
        {"text": "Release2", "x": -1, "y": 3},
    ]


def test_create_release_bars_with_position(parser):
    tested = parser.create_release_bars_with_position()
    assert tested == [{"x": -1, "width": 3, "y": 1.9}, {"x": -1, "width": 3, "y": 2.9}]
