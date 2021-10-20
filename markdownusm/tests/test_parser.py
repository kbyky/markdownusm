#!/usr/bin/env python

import pytest
from markdownusm.parser import MarkdownParser


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "line1\nline2\nline3\n\n<!-- -->\nline4",
            4,
        ),
        ("""""", 0),
    ],
)
def test_constructor(markdown, expected):
    """Test line count"""
    obj = MarkdownParser(markdown=markdown)
    assert len(obj.lines) == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "# Activity\n<!-- -->\n## Task1\n## Task2\nStory\n## Task3",
            ["Task1", "Task2", "Task3"],
        ),
        ("", []),
    ],
)
def test_extract_tasks(markdown, expected):
    actual = MarkdownParser(markdown=markdown)._extract_tasks()
    assert actual == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "# Activity1\n## Task1\nStory\n\n## Task2\n# Activity2\n## Task3",
            {"Activity1": "Task1", "Activity2": "Task3"},
        )
    ],
)
def test_extract_activities_with_tasks(markdown, expected):
    actual = MarkdownParser(markdown=markdown)._extract_activities_with_tasks()
    assert actual == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "- Release1\n- Release2\n<!-- -->\n\n- Release3\n-Release4",
            ["Release1", "Release2", "Release3"],
        ),
    ],
)
def test_extract_releases(markdown, expected):
    actual = MarkdownParser(markdown=markdown)._extract_releases()
    assert actual == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "# Activity\n## Task1\nStory1\n# Activity\n## Task2\nStory2\n## Task3\n---\nStory3",
            [
                "## Task1",
                "Story1",
                "## Task2",
                "Story2",
                "## Task3",
                "---",
                "Story3",
            ],
        )
    ],
)
def test__extract_tasks_and_stories(markdown, expected):
    actual = MarkdownParser(markdown=markdown)._extract_tasks_and_stories()
    assert actual == expected


@pytest.mark.parametrize(
    "target, delimiter, expected",
    [
        (["Story1", "---", "Story2"], "---", [["Story1"], ["Story2"]]),
        (["Story1", "## Task1", "Story2"], "##", [["Story1"], ["Story2"]]),
        (["---", "Story", "Story"], "---", [[], ["Story", "Story"]]),
    ],
)
def test_divide_list_by_prefix(target, delimiter, expected):
    actual = MarkdownParser._divide_list_by_prefix(target, delimiter)
    assert actual == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "## Task\nStory\nStory\nStory\n---\nStory\nStory\n---Story\nStory\n## Task\n---\n---\nStory\nStory\nStory",
            [3, 2, 3],
        )
    ],
)
def test_max_number_of_stories_in_each_release(markdown, expected):
    actual = MarkdownParser(markdown=markdown)._max_number_of_stories_in_each_release()
    assert actual == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "# Activity1\n## Task1\nStory1\n## Task2\nStory2\n# Activity2\n## Task3",
            [
                {"text": "Activity1", "x": 0, "y": 0},
                {"text": "Activity2", "x": 2, "y": 0},
            ],
        )
    ],
)
def test_extract_activities_with_position(markdown, expected):
    actual = MarkdownParser(markdown=markdown).extract_activities_with_position()
    assert actual == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "# Activity1\n## Task1\nStory1\n## Task2\nStory2\n# Activity2\n## Task3",
            [
                {"text": "Task1", "x": 0, "y": 1},
                {"text": "Task2", "x": 1, "y": 1},
                {"text": "Task3", "x": 2, "y": 1},
            ],
        )
    ],
)
def test_extract_tasks_with_position(markdown, expected):
    actual = MarkdownParser(markdown=markdown).extract_tasks_with_position()
    assert actual == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "# Activity1\n## Task1\nStory1\n## Task2\nStory2\n# Activity2\n## Task3\n---\nStory3",
            [
                {"text": "Story1", "x": 0, "y": 2},
                {"text": "Story2", "x": 1, "y": 2},
                {"text": "Story3", "x": 2, "y": 3},
            ],
        )
    ],
)
def test_extract_stories_with_position(markdown, expected):
    actual = MarkdownParser(markdown=markdown).extract_stories_with_position()
    assert actual == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "- Release1\n<!-- comment -->\n- Release2\n\n## Task\nStory\n## Task\n---\nStory\nStory\nStory",
            [
                {"text": "Release1", "x": -1, "y": 2},
                {"text": "Release2", "x": -1, "y": 3},
            ],
        )
    ],
)
def test_extract_release_texts_with_position(markdown, expected):
    actual = MarkdownParser(markdown=markdown).extract_release_texts_with_position()
    assert actual == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            "- Release1\n<!-- comment -->\n- Release2\n\n## Task\nStory\n## Task\n---\nStory\nStory\nStory\n## Task",
            [{"x": -1, "width": 3, "y": 1.9}, {"x": -1, "width": 3, "y": 2.9}],
        )
    ],
)
def test_create_release_bars_with_position(markdown, expected):
    actual = MarkdownParser(markdown=markdown).create_release_bars_with_position()
    assert actual == expected
