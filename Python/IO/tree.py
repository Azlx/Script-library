import os
import shutil
from pathlib import Path


def get_directory_list(src='/'):
    """
    获取指定路径的目录和文件列表
    :param src:
    :return:
    """
    src_path = Path(src)

    if src_path.is_file():
        raise TypeError('Need directory path, not file path')

    file_list = []
    dir_list = []
    for obj in src_path.iterdir():
        if obj.is_file():
            dir_list.append(obj.name)
        if obj.is_dir():
            dir_list.append(obj.name)

    return {
        'dir_path': src,
        'directories': {
            'length': len(dir_list),
            'list': dir_list,
        },
        'files': {
            'length': len(file_list),
            'list': file_list,
        },
    }


def rename(src, new_name, keep_suffix=True):
    """
    给指定路径的目录或者文件重命名
    :param src:
    :param new_name:
    :param keep_suffix: 是否保留原后缀
    :return:
    """
    src_path = Path(src)
    if not src_path.exists():
        raise IOError('No such file or directory')
    if keep_suffix:
        new_name_path = src_path.parent / '{0}{1}'.format(new_name,
                                                          src_path.suffix)
    else:
        new_name_path = src_path.parent / new_name

    src_path.rename(new_name_path)


def copy(src, dst):
    """
    复制文件和文件夹方法: 目标存在则在名称后面加 _copy_[num] (num > 0)
    :param src:
    :param dst:
    :return:
    """
    src_path = Path(src)
    if not src_path.exists():
        raise IOError('No such file or directory')

    if not Path(dst).exists():
        Path(dst).mkdir()

    dst_path = __generate_suffix(src, dst, 'copy')

    # 文件复制方法
    if src_path.is_file():
        shutil.copyfile(src, str(dst_path))

    # 目录复制方法
    if src_path.is_dir():
        shutil.copytree(src, str(dst_path))


def move(src, dst):
    """
    移动文件或目录方法：目标存在则在名称后面加 _move_[num] (num > 0)
    :param src:
    :param dst:
    :return:
    """
    src_path = Path(src)
    if not src_path.exists():
        raise IOError('No such file or directory')

    if not Path(dst).exists():
        Path(dst).mkdir()

    dst_path = __generate_suffix(src, dst, 'move')

    shutil.move(src, str(dst_path))


def delete(src):
    """
    删除指定路径文件或目录
    :param src:
    :return:
    """
    src_path = Path(src)
    if not src_path.exists():
        raise IOError('No such file or directory')

    # 删除文件
    if src_path.is_file():
        os.remove(str(src_path))

    # 删除目录
    if src_path.is_dir():
        shutil.rmtree(src)


def __generate_suffix(src, dst, io_type):
    """
    复制、移动文件时，如果目标存在自动生成后缀：_[io_type]_[num] (num > 0)
    :param src:
    :param dst:
    :return:
    """
    src_path = Path(src)
    dst_path = Path(dst) / src_path.name

    while True:
        if dst_path.exists():
            if '_{0}_'.format(io_type) in dst_path.name:
                num = int(dst_path.stem.split('_{0}_'.format(io_type))[-1]) + 1
            else:
                num = 1

            dst_str = '{0}_{1}_{2:02}{3}'.format(
                src_path.stem, io_type, num, src_path.suffix)

            dst_path = Path(dst) / dst_str
        else:
            break

    return dst_path


if __name__ == '__main__':
    pass
