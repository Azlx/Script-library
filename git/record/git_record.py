import os
import sys
import argparse
import configparser

from configparser import NoSectionError 
from pprint import pprint

RECORD_PATH = 'record_data.ini'


def set_argparse():
    """
    设置运行脚本参数
    """
    # RawDescriptionHelpFormatter参数指定description直接输出原始形式(不进行自动换行和消除空白的操作)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.description = \
        '记录git提交记录脚本\n' \
        '使用方法:\n\t' \
        '查看记录: python git_record.py get   [options]  \n\t' \
        '添加记录: python git_record.py add   [options]  必须指定 -p 和 -b 参数，如果没有记录则新增 \n\t' \
        '减少记录: python git_record.py minus [options]  必须指定 -p 和 -b 参数，如果没有记录则提示 \n\t' \
        '减少记录: python git_record.py del   [options]  \n\n\t' \
        '注: get、del 方法参数说明 \n\t\t' \
        '同时指定 -p 和 -b 参数表示 查看/删除 具体项目分支的记录; \n\t\t' \
        '只指定 -p 参数表示 查看/删除 该项目所有记录; \n\t\t' \
        '都不指定表示 查看/删除 所有项目所有分支的记录'

    parser.add_argument(
        'type',
        help='操作类型；获取: get; 添加: add; 减少: minus; 删除: del',
        type=str,
        choices=['get', 'add', 'minus', 'del'])

    parser.add_argument('-p', '--project', help='项目名称')
    parser.add_argument('-b', '--branch', help='分支名称')

    return parser.parse_args()


def check_parameters(func):
    """
    装饰器：如果传递了参数，则检查参数是否存在
    """
    def wraps(project=None, branch=None):
        cp = configparser.ConfigParser()
        cp.read(RECORD_PATH, encoding="utf-8-sig")

        if not project and branch:
            print('参数错误: 传递分支参数时必须要有项目参数')
            sys.exit()

        if project:
            if not cp.has_section(project):
                print('{0} 项目的提交记录不存在，请先调用 add 方法添加'.format(project))
                sys.exit()
            else:
                if branch and not cp.has_option(project, branch):
                    print('{0} 项目没有 {1} 分支的提交记录, 请先调用 add 方法添加'.format(project, branch))
                    sys.exit()

        return func(project, branch)

    return wraps


@check_parameters
def get_record(project=None, branch=None):
    """
    获取项目中分支的提交次数
    project: 指定项目，不指定则获取所有内容
    branch: 指定分支，不指定则获取当前项目所有分支内容(前提: 指定branch时必须指定project)
    """
    cp = configparser.ConfigParser()
    cp.read(RECORD_PATH, encoding="utf-8-sig")

    # 获取指定项目指定分支的提交次数
    if project and branch:
        return cp[project][branch]

    # 获取指定项目所有分支的提交次数
    if project:
        records = {}
        options = cp.options(project)
        for option in options:
            records[option] = cp[project][option]

        return records

    # 获取所有项目所有分支的提交次数
    all_records = []
    sections = cp.sections()
    for section in sections:
        records = {}
        options = cp.options(section)
        for option in options:
            records[option] = cp[section][option]

        all_records.append({section: records})

    return all_records


def add_record(project, branch):
    """
    添加一次记录
    project: 项目, 已有记录中不存在则新建项目记录
    branch: 分支, 已有记录中不存在则新建分支记录
    """
    cp = configparser.ConfigParser()
    cp.read(RECORD_PATH, encoding="utf-8-sig")

    if cp.has_section(project):
        if cp.has_option(project, branch):
            cp.set(project, branch, str(int(cp[project][branch]) + 1))
        else:
            cp.set(project, branch, '1')
    else:
        cp.add_section(project)
        cp.set(project, branch, '1')
    
    with open(RECORD_PATH, 'w') as f:
        cp.write(f)

    return get_record(project, branch)


@check_parameters
def minus_record(project, branch):
    """
    减少一次记录
    project: 项目
    branch: 分支。如果记录数为1，则不会继续减少
    """
    cp = configparser.ConfigParser()
    cp.read(RECORD_PATH, encoding="utf-8-sig")

    sections = cp.sections()
    options = cp.options(project)
    if int(cp[project][branch]) == 1:
        print('{0} 项目 {1} 分支的记录次数已经是最小值1，无法继续减少'.format(project, branch))
        sys.exit()
    else:
        cp.set(project, branch, str(int(cp[project][branch]) - 1))
        with open(RECORD_PATH, 'w') as f:
            cp.write(f)

    return get_record(project, branch)


@check_parameters
def del_record(project=None, branch=None):
    """
    删除记录
    """
    # 清空所有记录
    if not project and not branch:
        confirm = input('WARNING!!! 是否确定清除所有记录？(如果是的话请输入"yes",否则取消该操作)')
        if confirm == 'yes':
            os.system("echo '' > {0}".format(RECORD_PATH))
            print('\n已成功清理所有记录!')
            sys.exit()
        else:
            print('\n已取消清除所有记录的操作！')
            sys.exit()

    cp = configparser.ConfigParser()
    cp.read(RECORD_PATH, encoding="utf-8-sig")

    # 删除指定项目、指定分支的记录
    if project and branch:
        cp.remove_option(project, branch)
        with open(RECORD_PATH, 'w') as f:
            cp.write(f)
        print('已删除 {0} 项目 {1} 分支的记录'.format(project, branch))
        sys.exit()

    # 删除指定项目的记录
    if project and not branch:
        cp.remove_section(project)
        with open(RECORD_PATH, 'w') as f:
            cp.write(f)

        print('已删除 {0} 项目的记录'.format(project))
        sys.exit()


def main():
    """
    脚本入口
    """
    args = set_argparse()
    # 获取记录
    if args.type == 'get':
        result = get_record(args.project, args.branch)
        if args.project:
            if args.branch:
                print('{0} 项目 {1} 分支的提交记录为: {2}'.format(args.project, args.branch, result))
            else:
                print('{0} 项目的所有分支提交记录为:'.format(args.project))
                pprint(result)
        else:
            pprint('所有项目的所有分支的提交记录为:')
            pprint(result)

        sys.exit()

    # 增加记录
    if args.type == 'add':
        if args.project and args.branch:
            result = add_record(args.project, args.branch)
            print('{0} 项目 {1} 分支的提交记录为: {2}'.format(args.project, args.branch, result))
        else:
            print('add 方法必须要指定 -p 和 -b 参数')

        sys.exit()

    # 减少记录
    if args.type == 'minus':
        if args.project and args.branch:
            result = minus_record(args.project, args.branch)
            print('{0} 项目 {1} 分支的提交记录为: {2}'.format(args.project, args.branch, result))
        else:
            print('minus 方法必须要指定 -p 和 -b 参数')

        sys.exit()

    # 删除记录
    if args.type == 'del':
        del_record(args.project, args.branch)


if __name__ == '__main__':
    main()
