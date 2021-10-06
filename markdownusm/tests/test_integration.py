#!/usr/bin/env python

import pytest
from markdownusm.parser import MarkdownParser
from markdownusm.usm import Usm
from markdownusm.xml import XMLObjects


@pytest.fixture
def markdown():
    return """
- Release1
- Release2
- Release3
- Release4
- Release5

<!-- Comment -->
# Activity
## Task
Story
Story
---
---
Story

## Task
---
Story
Story
Story
---
Story

# Activity
## Task
---
Story
---
Story

## Task
Story
Story
Story
Story
---
---
Story
Story
Story
"""


def test_integration(markdown):
    parser = MarkdownParser(markdown=markdown)

    # Create list of dictionaries
    activities_list = parser.extract_activities_with_position()
    tasks_list = parser.extract_tasks_with_position()
    stories_list = parser.extract_stories_with_position()
    release_texts_list = parser.extract_release_texts_with_position()
    release_bars_list = parser.create_release_bars_with_position()

    # Create XML objects
    usm_activities = Usm(source=activities_list)
    usm_tasks = Usm(source=tasks_list)
    usm_stories = Usm(source=stories_list)
    usm_release_texts = Usm(source=release_texts_list)
    usm_release_bars = Usm(source=release_bars_list)

    # Create XML documents
    activities = usm_activities.to_activities()
    tasks = usm_tasks.to_tasks()
    stories = usm_stories.to_stories()
    release_texts = usm_release_texts.to_release_texts()
    release_bars = usm_release_bars.to_release_bars()

    export = XMLObjects(
        shapes=activities + tasks + stories + release_texts + release_bars
    ).render()

    assert (
        export
        == """
    <mxfile>
        <diagram>
            <mxGraphModel dx="661" dy="316" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0" background="#FFFFFF">
                <root>
                    <mxCell id="0"/>
                    <mxCell id="1" parent="0"/>
                    
                    
        <mxCell value="Activity" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#1F568A;strokeColor=none;fontColor=#FFFFFF;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="290.0" y="50.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Task" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#3288C4;strokeColor=none;fontColor=#FFFFFF;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="290.0" y="130.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Task" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#3288C4;strokeColor=none;fontColor=#FFFFFF;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="450.0" y="130.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Task" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#3288C4;strokeColor=none;fontColor=#FFFFFF;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="610.0" y="130.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Task" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#3288C4;strokeColor=none;fontColor=#FFFFFF;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="770.0" y="130.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="290.0" y="210.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="290.0" y="290.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="290.0" y="770.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="450.0" y="530.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="450.0" y="610.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="450.0" y="690.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="450.0" y="770.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="610.0" y="530.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="610.0" y="770.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="770.0" y="210.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="770.0" y="290.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="770.0" y="370.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="770.0" y="450.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="770.0" y="770.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="770.0" y="850.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Story" style="html=1;rounded=0;whiteSpace=wrap;fillColor=#ebf4fa;strokeColor=none;fontColor=#5F5F63;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="770.0" y="930.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Release1" style="html=1;rounded=0;whiteSpace=wrap;fillColor=none;strokeColor=none;fontColor=#7B8EA0;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="130.0" y="210.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Release2" style="html=1;rounded=0;whiteSpace=wrap;fillColor=none;strokeColor=none;fontColor=#7B8EA0;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="130.0" y="530.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell value="Release3" style="html=1;rounded=0;whiteSpace=wrap;fillColor=none;strokeColor=none;fontColor=#7B8EA0;align=left;verticalAlign=top;spacingLeft=5;spacingRight=5;shadow=1" parent="1" vertex="1">
            <mxGeometry x="130.0" y="770.0" width="140" height="60" as="geometry"/>
        </mxCell>
        
                    
                    
        <mxCell style="html=1;endArrow=none;shadow=0;strokeWidth=2;strokeColor=#5F5F63" edge="1" parent="1">
            <mxGeometry width="50" height="50" relative="1" as="geometry">
                <mxPoint x="130.0" y="202.0" as="sourcePoint"/>
                <mxPoint x="930.0" y="202.0" as="targetPoint"/>
            </mxGeometry>
        </mxCell>
        
                    
                    
        <mxCell style="html=1;endArrow=none;shadow=0;strokeWidth=2;strokeColor=#5F5F63" edge="1" parent="1">
            <mxGeometry width="50" height="50" relative="1" as="geometry">
                <mxPoint x="130.0" y="522.0" as="sourcePoint"/>
                <mxPoint x="930.0" y="522.0" as="targetPoint"/>
            </mxGeometry>
        </mxCell>
        
                    
                    
        <mxCell style="html=1;endArrow=none;shadow=0;strokeWidth=2;strokeColor=#5F5F63" edge="1" parent="1">
            <mxGeometry width="50" height="50" relative="1" as="geometry">
                <mxPoint x="130.0" y="762.0" as="sourcePoint"/>
                <mxPoint x="930.0" y="762.0" as="targetPoint"/>
            </mxGeometry>
        </mxCell>
        
                    
                </root>
            </mxGraphModel>
        </diagram>
    </mxfile>
    """
    )
