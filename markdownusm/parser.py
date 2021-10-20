#!/usr/bin/env python

from itertools import accumulate
from typing import Optional, Union

from pydantic import BaseModel, Field

U = Union[str, float]


class MarkdownParser(BaseModel):
    markdown: str = Field(title="Text written in markdown")

    # Lines without blank and comments, populated by constructor
    lines: Optional[list[str]] = Field(
        title="List of markdown lines without blanks and comments"
    )

    def __init__(self, **data):
        super().__init__(**data)

        # Remove blank lines and comments
        self.lines = list(
            filter(
                lambda x: x.strip() != "" and not x.startswith("<!--"),
                self.markdown.split("\n"),
            )
        )

    def extract_activities_with_position(self) -> list[dict[str, U]]:
        """Create list of dicts whose keys are activities' texts and positions
        
        Examples:
            >>> extract_activities_with_position()
            [
                {"text": "Activity1", "x": 0, "y": 0},
                {"text": "Activity2", "x": 2, "y": 0},
            ]

        """
        tasks: list[str] = self._extract_tasks()
        activities_with_tasks: dict[str, str] = self._extract_activities_with_tasks()

        return [
            dict(text=k, x=tasks.index(v), y=0)
            for k, v in activities_with_tasks.items()
        ]

    def extract_tasks_with_position(self) -> list[dict[str, U]]:
        """Create list of dicts whose keys are tasks' texts and positions

        Examples:
            >>> extract_tasks_with_position()
            [
                {"text": "Task1", "x": 0, "y": 1},
                {"text": "Task2", "x": 1, "y": 1},
                {"text": "Task3", "x": 2, "y": 1},
            ]

        """
        tasks: list[str] = self._extract_tasks()

        return [dict(text=task, x=i, y=1) for i, task in enumerate(tasks)]

    def extract_stories_with_position(self) -> list[dict[str, U]]:
        """Create list of dicts whose keys are stories' texts and positions

        Examples:
            >>> extract_stories_with_position()
            [
                {"text": "Story1", "x": 0, "y": 2},
                {"text": "Story2", "x": 1, "y": 2},
                {"text": "Story3", "x": 2, "y": 3},
            ]

        """

        # tasks_and_stories: ['## Task', 'Story', '---', 'Story', ...]
        tasks_and_stories = self._extract_tasks_and_stories()

        # [['Story1', 'Story2', '---', 'Story3'], ['---', 'Story4', 'Story5', '---', 'Story6'], ['Story7', '---', 'Story8']]
        split_by_task = self._divide_list_by_prefix(tasks_and_stories, "## ")[
            1:
        ]  # Remove first task

        """
        [
            [ # Task
                ['Story1', 'Story2'], # Release1
                ['Story3'] # Release2
            ],
            [
                [],
                ['Story4', 'Story5'],
                ['Story6']
            ],
            [
                ['Story7'],
                ['Story8']
            ]
        ]
        """

        # Get maximum number of stories to identify release bars positions
        number_of_stories_in_each_release = (
            self._max_number_of_stories_in_each_release()
        )
        # Adjustment in vertical position
        release_adjustment = list(
            accumulate([0] + number_of_stories_in_each_release[:-1])
        )

        split_by_release = list(
            map(lambda x: self._divide_list_by_prefix(x, "---"), split_by_task)
        )

        x = 0
        y = 2
        release_number = 0
        result: list[dict[str, U]] = []

        for task in split_by_release:
            release_number = 0
            for release in task:
                for story in release:
                    result.append(
                        dict(text=story, x=x, y=y + release_adjustment[release_number])
                    )
                    y += 1

                release_number += 1
                y = 2
            x += 1

        return result

    def extract_release_texts_with_position(
        self,
    ) -> list[dict[str, U]]:
        """
        [
            {"text": "Release1", "x": -1, "y": 1},
            {"text": "Release2", "x": -1, "y": 2},
        ]
        """
        releases = self._extract_releases()
        number_of_stories = self._max_number_of_stories_in_each_release()
        release_positions = list(accumulate([2] + number_of_stories[:-1]))

        return [
            dict(text=release, x=-1, y=y)
            for release, y in zip(releases, release_positions)
        ]

    def create_release_bars_with_position(self) -> list[dict[str, U]]:
        from itertools import accumulate

        number_of_stories = self._max_number_of_stories_in_each_release()
        number_of_stories_accumulate = list(accumulate([2] + number_of_stories[:-1]))

        number_of_tasks = len(self._extract_tasks())

        return [
            dict(x=-1, width=number_of_tasks, y=y - 0.1)
            for y in number_of_stories_accumulate
        ]

    def _extract_tasks(self) -> list[str]:
        """Create task list from markdown

        Examples:
            >>> _extract_tasks("#Activity\n## Task1\n## Task2")
            ['Task1', 'Task2', ...]

        """
        return list(
            map(
                lambda x: x.replace("## ", ""),
                filter(lambda x: x.startswith("## "), self.lines),
            )
        )

    def _extract_activities_with_tasks(self) -> dict[str, str]:
        """Create a dictionary whose keys are activities and values are tasks

        Examples:
            >>> _extract_activities_with_tasks("# Activity1\n## Task1\n## Task2")
            {'Activity1': 'Task1', 'Activity1': 'Task2', ...}

        """
        dic: dict[str, str] = {}
        for i, v in enumerate(self.lines):
            if not v.startswith("# "):
                continue

            dic = dic | {v.replace("# ", ""): self.lines[i + 1].replace("## ", "")}

        return dic

    def _extract_releases(self) -> list[str]:
        """Create release list from markdown

        Examples:
            >>> _extract_releases("- Release1\n- Release2\n# Activity\n## Task)
            ['Release1', 'Release2', ...]
        """
        return list(
            map(
                lambda x: x.replace("- ", ""),
                filter(lambda x: x.startswith("- "), self.lines),
            )
        )

    def _extract_tasks_and_stories(self) -> list[str]:
        """Create tasks(with #) and stories list from markdown

        Release separator will be included

        Examples:
            >>> _extract_tasks_and_stories("# Activity\n## Task1\nStory1\n---\nStory2")
            ['## Task1', 'Story1', '---', 'Story2', ...]

        """
        return list(
            filter(
                lambda x: not x.startswith("# ") and not x.startswith("- "), self.lines
            )
        )

    def _max_number_of_stories_in_each_release(self) -> list[float]:
        """Identify maximum number of stories in each release

        Examples:
            >>> _max_number_of_stories_in_each_release("## Task1\nStory1\n---Story2\n## Task2\n---\nStory3\nStory4")
            [1, 2]

        """
        # e.g. ['## Task1', 'Story1', '---', 'Story2', ...]
        tasks_and_stories = self._extract_tasks_and_stories()

        stories: list[list[str]] = []
        # Temporary list
        contents: list[str] = []
        for item in tasks_and_stories:
            if item.startswith("## "):
                if contents == []:
                    continue

                stories.append(contents)
                contents = []
            else:
                contents.append(item)

        # stories: [['Story1'], ['Story2'], ['---', 'Story3']]
        stories.append(contents)

        number_of_releases: int = (
            max([len([item for item in x if item.startswith("---")]) for x in stories])
            + 1
        )

        # number_of_tasks_in_each_release: [[1], [1], [0, 1]]
        number_of_tasks_in_each_release: list[list[int]] = [
            list(map(lambda x: len(x), self._divide_list_by_prefix(x, "---")))
            for x in stories
        ]

        # Arrange lists in length
        # number_of_tasks_in_releases: [[1, 0], [1, 0], [0, 1]]
        number_of_stories_in_releases = list(
            map(
                lambda x: self._extend_list(x, number_of_releases),
                number_of_tasks_in_each_release,
            )
        )

        # Extract maximum number of each release
        return list(map(lambda x: max(x), zip(*number_of_stories_in_releases)))

    @staticmethod
    def _divide_list_by_prefix(target: list[str], prefix: str) -> list[list[str]]:
        """Split a list into multiple lists wrapped as a list

        Examples:
            >>> _divide_list_by_prefix(["Story1", "---", "Story2"], "---")
            [["Story1"], ["Story2"]]

            >>> _divide_list_by_prefix(["---", "Story2"], "---")
            [[], ["Story2"]]

        """
        result: list[list[str]] = []
        child: list[str] = []

        for item in target:
            if item.startswith(prefix):
                result.append(child)
                child = []
            else:
                child.append(item)
        result.append(child)

        return result

    @staticmethod
    def _extend_list(
        source: list[int], disirable_length: int, complement: int = 0
    ) -> list[int]:
        """Extend list for arranging in numbers

        Example:
            >>> _extend_list([1, 2], 4)
            [1, 2, 0, 0]

        """
        if len(source) >= disirable_length:
            return source

        result = [0 for x in range(disirable_length)]

        for i in range(len(source)):
            result[i] = source[i]

        return result
