# GIT 提交记录

## 背景
个人习惯使用 git commit 时对 commit 信息进行格式化，如：
> git commit -am "[BRANCH - TYPE] commit msg  # NUM"
>> BRANCH: 当前分支
>>
>> TYPE: 代表本次提交的类型，有 Init、Build、ReBuild、Update、Add、Del 等等
>>
>> NUM: 代表提交次数，用来记录这是第几次提交
>

这样有个问题是我每次提交都要先看一下上次提交的信息，来确定本次是第几次提交

在仓库多和仓库中分支多的时候，查看起来特别麻烦

所以，我写了此脚本用来记录项目中各分支的提交次数

## 使用方法
usage: git_record.py [-h] [-p PROJECT] [-b BRANCH] {get,add,minus,del}
> 查看记录: python git_record.py get   [options]
>
> 添加记录: python git_record.py add   [options]  必须指定 -p 和 -b 参数，如果没有记录则新增
>
> 减少记录: python git_record.py minus [options]  必须指定 -p 和 -b 参数，如果没有记录则提示
>
> 减少记录: python git_record.py del   [options]
>
> 注: get、del 方法参数说明
>> 同时指定 -p 和 -b 参数表示 查看/删除 具体项目分支的记录;
>>
>> 只指定 -p 参数表示 查看/删除 该项目所有记录;
>>
>> 都不指定表示 查看/删除 所有项目所有分支的记录

positional arguments:
> {get,add,minus,del}   操作类型；获取: get; 添加: add; 减少: minus; 删除: del

optional arguments:
> -h, --help            show this help message and exit
>
> -p PROJECT, --project PROJECT 项目名称
>
> -b BRANCH, --branch BRANCH 分支名称

## 注：
本脚本默认使用 ini 文件来记录提交信息。使用前请先新建 ini 文件，并在脚本第 9 行指定文件位置。
