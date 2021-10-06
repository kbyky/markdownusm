#!/usr/bin/env python

import argparse

from markdownusm.parser import MarkdownParser
from markdownusm.usm import Usm
from markdownusm.xml import XMLObjects

parser = argparse.ArgumentParser()
parser.add_argument("file", type=argparse.FileType("r"))
parser.add_argument("-o", required=False, type=argparse.FileType("w"))
args = parser.parse_args()


def main():
    xml = parse(args.file.read())

    if args.o is None:
        print(xml)
        return

    args.o.write(xml)


def parse(markdown: str) -> str:
    parser = MarkdownParser(markdown=markdown)

    activities_list = parser.extract_activities_with_position()
    tasks_list = parser.extract_tasks_with_position()
    stories_list = parser.extract_stories_with_position()
    release_texts_list = parser.extract_release_texts_with_position()
    release_bars_list = parser.create_release_bars_with_position()

    usm_activities = Usm(source=activities_list)
    usm_tasks = Usm(source=tasks_list)
    usm_stories = Usm(source=stories_list)
    usm_release_texts = Usm(source=release_texts_list)
    usm_release_bars = Usm(source=release_bars_list)

    activities = usm_activities.to_activities()
    tasks = usm_tasks.to_tasks()
    stories = usm_stories.to_stories()
    release_texts = usm_release_texts.to_release_texts()
    release_bars = usm_release_bars.to_release_bars()

    export = XMLObjects(
        shapes=activities + tasks + stories + release_texts + release_bars
    )

    return export.render()


if __name__ == "__main__":
    main()
