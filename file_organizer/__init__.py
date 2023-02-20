import shutil

from loguru import logger
from os import walk, listdir
from pathlib import Path
from filecmp import cmp


def rename(file_name: str) -> str:
    idx = file_name.index(".")
    return file_name[:idx] + "_1" + file_name[idx:]


def deal(src: Path, dst: Path, copy: bool = True, strategy: str = "both"):
    if not dst.exists():
        shutil.copy2(src, dst)
        logger.info("迁移原文件到 {}", dst)
    elif cmp(src, dst):
        logger.info("无需迁移文件 {}", dst)
    elif strategy == "later" and src.stat().st_mtime > dst.stat().st_mtime:
        shutil.copy2(src, dst)
        logger.info("迁移新文件到 {}", dst)
    elif strategy == "bigger" and src.stat().st_size > dst.stat().st_size:
        shutil.copy2(src, dst)
        logger.info("迁移大文件到 {}", dst)
    else:
        dst = dst.parent / Path(rename(dst.name))
        shutil.copy2(src, dst)
        logger.info("重命名文件到 {}", dst)

    if not copy:
        src.unlink()


def organize(src: str, exts: str, dst: str, copy: bool = True, strategy: str = "both"):
    if not exts or len(exts) < 1:
        raise ValueError('"exts" is invalid')

    lc_exts = [e.lower() for e in exts.split()]

    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists() or not src_path.is_dir():
        raise ValueError('"src" is invalid')

    if not dst_path.exists():
        dst_path.mkdir(parents=True, exist_ok=True)

    for root, _, files in walk(src):
        for name in files:
            file = Path(root) / Path(name)
            if file.suffix.lower() not in lc_exts:
                continue

            target = dst_path / Path(name)
            try:
                deal(file, target, copy, strategy)
            except Exception as e:
                pass

    if not copy and len(listdir(src_path)) < 1:
        src_path.rmdir()
