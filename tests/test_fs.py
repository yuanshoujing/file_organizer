from os import walk
from pathlib import Path
from loguru import logger

from file_organizer import organize


def test_walk():
    for root, dirs, files in walk("."):
        logger.debug("root: {}, dirs: {}, files: {}", root, dirs, files)
        for name in files:
            file = Path(root) / Path(name)
            logger.debug("file: {}", file)


def test_organize():
    # organize(
        # "/Volumes/opt/Docs",
        # [".jpg", ".jpeg", ".png", ".gif"],
        # "/Volumes/opt/Images",
        # strategy="later",
    # )
    # organize("/Volumes/opt/Docs", [".doc", ".docx"], "/Volumes/opt/wordocs")
    # organize(
    # "/Volumes/opt/wordocs", [".doc", ".docx"], "/Users/rocker/ddd", strategy="later"
    # )
    organize("e:\\dev_docs", ".doc .docx", "e:/ttttt/docs")
