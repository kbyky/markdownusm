#!/usr/bin/env python
"""Convert list objects to XML objects"""

from typing import Optional, Union

from pydantic import BaseModel

from markdownusm.xml import Line, Rectangle

U = Union[str, float]


class Usm(BaseModel):
    source: list[dict[str, U]]
    source_abs: Optional[list[dict[str, U]]]

    start_x: float = 290
    start_y: float = 50

    width: float = 140
    height: float = 60

    padding: float = 20

    def __init__(self, **data):
        super().__init__(**data)

        self.source_abs = [self._update_dic(dic) for dic in self.source]

    def to_activities(self) -> list[Rectangle]:
        colors = dict(fillColor="#1F568A", fontColor="#FFFFFF")

        return [Rectangle(**(dic | colors)) for dic in self.source_abs]

    def to_tasks(self) -> list[Rectangle]:
        colors = dict(fillColor="#3288C4", fontColor="#FFFFFF")

        return [Rectangle(**(dic | colors)) for dic in self.source_abs]

    def to_stories(self) -> list[Rectangle]:
        return [
            Rectangle(**(dic | self._set_story_properties(dic)))
            for dic in self.source_abs
        ]

    def to_release_texts(self) -> list[Rectangle]:
        colors = dict(fillColor="none", fontColor="#7B8EA0", strokeColor="none")

        return [Rectangle(**(dic | colors)) for dic in self.source_abs]

    def to_release_bars(self) -> list[Line]:
        colors = dict(strokeColor="#5F5F63", shadow=1)

        return [Line(**dic | colors) for dic in self.source_abs]
    def _relative_to_absolute_vertical(self, y: float) -> float:
        """Convert relative vertical position to absolute position"""
        return self.start_y + (self.height + self.padding) * y

    def _relative_to_absolute_horizontal(self, x: float) -> float:
        """Convert relative horizontal position to absolute position"""
        return self.start_x + (self.width + self.padding) * x

    def _relative_to_absolute_width(self, width: float) -> float:
        """Convert relative width to absolute width"""
        return self.start_x + (self.width + self.padding) * width

    def _update_dic(self, dic: dict[str, U]) -> dict[str, U]:
        """Update dictonary to convert positions

        Called from constructor

        """
        result = dic.copy()

        if (x := result.get("x")) is not None:
            result = result | dict(x=self._relative_to_absolute_horizontal(float(x)))

        if (y := result.get("y")) is not None:
            result = result | dict(y=self._relative_to_absolute_vertical(float(y)))

        if (width := result.get("width")) is not None:
            result = result | dict(width=self._relative_to_absolute_width(float(width)))

        return result

    def _set_story_properties(self, source_dic: dict[str, U]) -> dict[str, U]:
        """Set story properties

        Story suffix `!` express warning point

        Examples:
            >>> _set_story_properties(dict(text="Story X!", fillColor="#000000", ...))
            dict(text="Story X", fillColor="#f8d7da", ...)

            >>> _set_story_properties(dict(text="Story X", fillColor="#000000", ...))
            dict(text="Story X", fillColor="#ebf4fa", ...)

        """
        result: dict[str, U] = source_dic.copy()
        result = result | dict(fontColor="#5F5F63")

        if (story := str(result.get("text")))[-1] == "!":
            result = result | dict(text=story[:-1])
            result = result | dict(fillColor="#f8d7da")
        else:
            result = result | dict(fillColor="#ebf4fa")

        return result

