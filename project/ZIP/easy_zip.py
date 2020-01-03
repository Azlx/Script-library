import zipfile

from pathlib import Path

import easy_file


def __get_zip_list(path, zip_list):
    """
    获得要压缩zip对象列表
    :param path:
    :param zip_list:
    :return:
    """
    zip_path = Path(path)

    if not zip_path.exists():
        raise Exception('The path does not exist!')

    if zip_path.is_dir():
        for zip_obj in zip_path.iterdir():
            if zip_obj.name == '.DS_Store':
                continue

            if zip_obj.is_dir():
                __get_zip_list(str(zip_obj), zip_list)
            else:
                zip_list.append(str(zip_obj))
    else:
        zip_list.append(path)


def create_zip(src, dst, dst_name=None, dst_parents=True):
    """
    创建指定目录的ZIP压缩文件
    :param src:
    :param dst:
    :param dst_name:
    :param dst_parents:
    :return:
    """
    zip_list = []
    __get_zip_list(src, zip_list)

    dst_path = Path(dst)
    src_path = Path(src)

    if not dst_path.exists():
        if dst_parents:
            dst_path.mkdir(parents=True)
        else:
            raise Exception('The target path does not exist! '
                            'Please create the target path first, '
                            'or specify the "dst_parents" parameter to be True!'
                            )

    # 如果只是压缩一个文件，无论压缩后的名字后缀给定的是什么都将使用原文件后缀
    if dst_name is None:
        dst_name = '{0}.zip'.format(src_path.name)
    else:
        if src_path.is_file():
            dst_name = '{0}{1}.zip'.format(Path(dst_name).stem,
                                           src_path.suffix)

    dst_path = dst_path / dst_name

    """
    检测目标路径是否已存在压缩后的文件，
    如果存在, 待压缩文件压缩后的名称更改为：
        name[_zip_(num)].suffix
        其中，name: 原始对象名称
             suffix: 原始对象后缀(目录则后缀为空)
             _zip_(num): 压缩后重名所自动生成的名称后缀(num > 0)
    """
    while True:
        if dst_path.exists():
            # 文件和目录不能统一方法，故分类型操作
            if '_zip_' in dst_path.stem:
                if src_path.is_file():
                    num = int(dst_path.stem.split(
                        src_path.suffix)[0].split('_zip_')[-1]) + 1

                    stem = dst_path.stem.split(
                        src_path.suffix)[0].split('_zip_')[0]
                else:
                    num = int(dst_path.stem.split('_zip_')[-1]) + 1
                    stem = dst_path.stem.split('_zip_')[0]
            else:
                num = 1
                if src_path.is_file():
                    stem = dst_path.stem.split(src_path.suffix)[0]
                else:
                    stem = dst_path.stem

            if src_path.is_file():
                dst_name = '{0}_{1}_{2:02}{3}{4}'.format(stem, 'zip', num,
                                                         src_path.suffix,
                                                         dst_path.suffix)
            else:
                dst_name = '{0}_{1}_{2:02}{3}'.format(stem, 'zip', num,
                                                      dst_path.suffix)

            dst_path = Path(dst) / dst_name
        else:
            break

    z = zipfile.ZipFile(str(dst_path), 'w', zipfile.ZIP_DEFLATED)

    if len(zip_list) != 1:
        for zip_file in zip_list:
            file_name = zip_file.split(src)[-1]
            if not file_name.startswith('/'):
                file_name = '/{0}'.format(file_name)
            z.write(zip_file, file_name)
    else:
        z.write(zip_list[0], Path(zip_list[0]).name)
    z.close()

    return {
        'dst_name': dst_path.name,
        'dst_path': str(dst_path),
    }


def extract_zip(src, dst):
    """
    解压指定ZIP文件到指定目录
    :param src:
    :param dst:
    :return:
    """
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists():
        raise Exception('The ZIP file does not exist!')

    z = zipfile.ZipFile(src, 'r')

    dst_path = dst_path / src_path.stem

    """
    检测目标路径是否已存在解压后的文件，
    如果存在, 待解压文件解压后的名称更改为：
        name[_zip_(num)].suffix
        其中，name: 压缩文件原始名称
             suffix: 压缩文件原始后缀(目录则后缀为空)
             _zip_(num): 解压后重名所自动生成的名称后缀(num > 0)
    """
    while True:
        if dst_path.exists():
            if '_zip_' in dst_path.stem:
                num = int(dst_path.stem.split('_zip_')[-1]) + 1
                stem = dst_path.stem.split('_zip_')[0]
            else:
                num = 1
                stem = dst_path.stem
            dst_name = '{0}_{1}_{2:02}{3}'.format(stem, 'zip', num,
                                                  dst_path.suffix)
            dst_path = Path(dst) / dst_name
        else:
            break

    z.extractall(str(dst_path))
    z.close()

    # 待解压对象为文件的后续操作
    this_path = dst_path / src_path.stem
    if this_path.exists() and this_path.is_file():
        easy_file.rename(str(this_path), str(dst_path.name), keep_suffix=False)
        easy_file.rename(str(dst_path), '{0}_cache'.format(str(dst_path.name)),
                    keep_suffix=False)

        this_path = dst_path.parent / '{0}_cache'.format(
            str(dst_path.name)) / str(dst_path.name)

        easy_file.move(str(this_path), str(dst_path.parent))
        easy_file.delete(str(this_path.parent))


if __name__ == '__main__':
    pass
