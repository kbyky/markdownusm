#!/usr/bin/env python
"""Convert list objects to XML objects"""

from typing import Optional, Union

from pydantic import BaseModel

from markdownusm.xml import Line, Rectangle

U = Union[str, float]


class Usm(BaseModel):
    source: list[dict[str, U]]
    # Source list with absolute position
    source_abs: Optional[list[dict[str, U]]]

    start_x: float = 290
    start_y: float = 50

    width: float = 140
    height: float = 60

    padding: float = 20

    activity_fill_color: str = "#1F568A"
    activity_font_color: str = "#FFFFFF"

    task_fill_color: str = "#3288C4"
    task_font_color: str = "#FFFFFF"

    release_text_fill_color: str = "none"
    release_text_font_color: str = "#7B8EA0"
    release_text_stroke_color: str = "none"

    release_bar_stroke_color: str = "#5F5F63"

    story_font_color: str = "#5F5F63"
    story_default_fill_color: str = "#ebf4fa"
    story_warning_fill_color: str = "#f8d7da"

    def __init__(self, **data):
        super().__init__(**data)

        self.source_abs = [self._update_dic(dic) for dic in self.source]

    def to_activities(self) -> list[Rectangle]:
        colors = dict(
            fillColor=self.activity_fill_color, fontColor=self.activity_font_color
        )

        return [Rectangle(**(dic | colors)) for dic in self.source_abs]

    def to_tasks(self) -> list[Rectangle]:
        colors = dict(fillColor=self.task_fill_color, fontColor=self.task_font_color)

        return [Rectangle(**(dic | colors)) for dic in self.source_abs]

    def to_stories(self) -> list[Rectangle]:
        return [
            Rectangle(**(dic | self._set_story_properties(dic)))
            for dic in self.source_abs
        ]

    def to_release_texts(self) -> list[Rectangle]:
        colors = dict(
            fillColor=self.release_text_fill_color,
            fontColor=self.release_text_font_color,
            strokeColor=self.release_text_stroke_color,
        )

        return [Rectangle(**(dic | colors)) for dic in self.source_abs]

    def to_release_bars(self) -> list[Line]:
        colors = dict(strokeColor=self.release_bar_stroke_color, shadow=1)

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

        update_dic = dict(
            fontColor=self.story_font_color, fillColor=self.story_default_fill_color
        )
        story_text = str(result.get("text"))

        if story_text[-1] == "!":
            # If story's suffix is `!`
            update_dic = update_dic | dict(
                text=story_text[:-1], fillColor=self.story_warning_fill_color
            )
        elif "#" in story_text:
            # If story has hex color code in suffix
            update_dic = update_dic | dict(
                text=story_text.split("#")[0].strip(),
                fillColor="#" + story_text.split("#")[1].strip(),
            )

        return result | update_dic
