import shutil
import click

from loguru import logger
from os import walk
from pathlib import Path
from filecmp import cmp
from tqdm import tqdm


def deal(src: Path, dst: Path, move: bool = False, strategy: str = "both"):
    def copy_or_move():
        shutil.copy2(src, dst)
        if move:
            src.unlink()

    if not dst.exists():
        copy_or_move()
    elif cmp(src, dst):
        if move:
            src.unlink()
    elif strategy == "later":
        if src.stat().st_mtime <= dst.stat().st_mtime:
            if move:
                src.unlink()
        else:
            copy_or_move()
    elif strategy == "bigger":
        if src.stat().st_size <= dst.stat().st_size:
            if move:
                src.unlink()
        else:
            copy_or_move()
    else:
        idx = dst.name.index(".")
        dst = dst.parent / Path(dst.name[:idx] + "_1" + dst.name[idx:])
        shutil.copy2(src, dst)


# @click.command()
# @click.option(
#     "-s", "--src", required=True, type=click.Path(exists=True), help="整理此路径下的文件"
# )
# @click.option(
#     "-e",
#     "--exts",
#     required=True,
#     help="只整理此后缀的文件。可以同时处理多种后缀，如 -e .png .jpg .jpeg",
# )
# @click.option(
#     "-d", "--dst", required=True, type=click.Path(exists=False), help="整理后的文件放在此路径"
# )
# @click.option(
#     "-m", "--move", is_flag=True, default=False, help="有此选项则移动文件到目标路径，否则复制文件到目标路径"
# )
# @click.option(
#     "-st",
#     "--strategy",
#     type=click.Choice(["later", "bigger", "both"]),
#     default="both",
#     help="目标路径中存在同名文件时如何处理。later 保留最新的；bigger 保留最大的；both 两个都保留",
# )
def organize(
    src: str, exts: str, dst: str, move: bool = False, strategy: str = "both"
):
    if not exts or len(exts) < 1:
        raise ValueError('"exts" is invalid')

    lc_exts = [e.lower() for e in exts.split()]

    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists() or not src_path.is_dir():
        raise ValueError('"src" is invalid')

    if not dst_path.exists():
        dst_path.mkdir(parents=True, exist_ok=True)

    i = 0
    for root, _, files in tqdm(walk(src)):
        i += len(files)

    pbar = tqdm(total=i, bar_format='{percentage:3.0f}% {bar} {n_fmt}/{total_fmt}')
    for root, _, files in walk(src):
        for name in files:
            file = Path(root) / Path(name)

            if file.suffix.lower() not in lc_exts:
                pbar.update(1)
                continue

            target = dst_path / Path(name)

            deal(file, target, move, strategy)
            # pbar.set_description(name)
            pbar.update(1)

    if move:
        src_path.rmdir()
