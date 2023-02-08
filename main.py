#!/usr/bin/env python
# -*- coding=utf-8 -*-

import click
from file_organizer import organize


@click.command()
@click.option(
    "-s", "--src", required=True, type=click.Path(exists=True), help="整理此路径下的文件"
)
@click.option(
    "-e",
    "--exts",
    required=True,
    help="只整理此后缀的文件。可以同时处理多种后缀，如 -e .png .jpg .jpeg",
)
@click.option(
    "-d", "--dst", required=True, type=click.Path(exists=False), help="整理后的文件放在此路径"
)
@click.option(
    "-m", "--move", is_flag=True, default=False, help="有此选项则移动文件到目标路径，否则复制文件到目标路径"
)
@click.option(
    "-st",
    "--strategy",
    type=click.Choice(["later", "bigger", "both"]),
    default="both",
    help="目标路径中存在同名文件时如何处理。later 保留最新的；bigger 保留最大的；both 两个都保留",
)
def cui(src, exts, dst, move, strategy):
    organize(src, exts, dst, move, strategy)


if __name__ == "__main__":
    cui()
