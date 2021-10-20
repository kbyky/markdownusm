#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
from typing import Union

from jinja2 import BaseLoader, Environment
from pydantic import BaseModel, Field

U = Union[str, float]


class XMLObject(BaseModel, metaclass=ABCMeta):
    @abstractmethod
    def to_xml(self) -> str:
        pass


class Rectangle(XMLObject):
    """XML Rectangle Object"""

    text: str = Field(title="Text")

    y: float = Field(title="Vertical Position", ge=0)
    x: float = Field(title="Horizontal Position", ge=0)

    fillColor: str = Field(title="Fill Color")
    fontColor: str = Field(title="Font Color")

    height: float = Field(60, title="Height", gt=0)
    width: float = Field(140, title="Width", gt=0)

    rounded: int = Field(0, title="Rounded", ge=0, le=1)
    whiteSpace: str = Field("wrap", title="White Space")

    strokeColor: str = Field("none", title="Stroke Color")

    align: str = Field("left", title="Horizontal Align")
    verticalAlign: str = Field("top", title="Vertical Align")

    spacingLeft: float = Field(5, title="Left Spacing")
    spacingRight: float = Field(5, title="Right Spacing")
    shadow: int = Field(1, title="Shadow", ge=0, le=1)

    def to_xml(self) -> str:
        return f"""
        <mxCell value="{self.text}" style="{self._style()}" parent="1" vertex="1">
            <mxGeometry {self._geometry()} as="geometry"/>
        </mxCell>
        """

    def _geometry(self) -> str:
        """Position settings
        
        Examples:
            >>> _geometry()
            'x="0.0" y="0.0" width="140" height="60"'
        """
        dic = dict(x=self.x, y=self.y, width=self.width, height=self.height)
        return " ".join([f'{k}="{str(v)}"' for k, v in dic.items()])

    def _style(self) -> str:
        """Style settings"""
        dic = dict(
            html=1,
            rounded=self.rounded,
            whiteSpace=self.whiteSpace,
            fillColor=self.fillColor,
            strokeColor=self.strokeColor,
            fontColor=self.fontColor,
            align=self.align,
            verticalAlign=self.verticalAlign,
            spacingLeft=self.spacingLeft,
            spacingRight=self.spacingRight,
            shadow=self.shadow,
        )

        return ";".join([f"{k}={v}" for k, v in dic.items()])


class Line(XMLObject):
    """XML Line Object"""

    y: float = Field(title="Start/End vertical position")
    x: float = Field(title="Start horizontal positon")
    width: float = Field(title="Line length")

    strokeColor: str = Field("#000000")
    strokeWidth: float = Field(2)

    def _style(self) -> str:
        """Style settings"""
        dic = dict(
            html=1,
            endArrow="none",
            shadow=0,
            strokeWidth=self.strokeWidth,
            strokeColor=self.strokeColor,
        )

        return ";".join([f"{k}={v}" for k, v in dic.items()])

    def to_xml(self) -> str:
        return f"""
        <mxCell style="{self._style()}" edge="1" parent="1">
            <mxGeometry width="50" height="50" relative="1" as="geometry">
                <mxPoint x="{self.x}" y="{self.y}" as="sourcePoint"/>
                <mxPoint x="{self.width}" y="{self.y}" as="targetPoint"/>
            </mxGeometry>
        </mxCell>
        """


class XMLObjects(BaseModel):
    """Merge XML objects into one XML document"""

    shapes: list[XMLObject] = Field(title="XML Objects")

    xml_template = """
    <mxfile>
        <diagram>
            <mxGraphModel dx="661" dy="316" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0" background="#FFFFFF">
                <root>
                    <mxCell id="0"/>
                    <mxCell id="1" parent="0"/>
                    {% for item in shapes %}
                    {{ item }}
                    {% endfor %}
                </root>
            </mxGraphModel>
        </diagram>
    </mxfile>
    """

    def render(self) -> str:
        """Render XML objects

        Returns:
            str: XML document

        """
        template = Environment(loader=BaseLoader()).from_string(self.xml_template)

        return template.render(shapes=self._shapes_to_xml())

    def _shapes_to_xml(self) -> list[str]:
        """Create XML string list"""
        return [x.to_xml() for x in self.shapes]
