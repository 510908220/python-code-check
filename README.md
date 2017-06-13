# python-code-check
实现一个基于[jenkins](https://jenkins.io/) + [pylint](https://www.pylint.org/)的代码检查工具. 使用:

## 要求

被检查的python代码所在目录符合包的形式,如:

- `__init__.py`
- `requirements.txt`
- `pylint.cfg`



## 配置

- 生成配置:`pylint --generate-rcfile > pylint.cfg`
- 将`output-format`项的值改为`parseable`
- `init-hook`添加`'import sys; sys.path.append("/var/lib/jenkins/workspace/xxx")'`,`xxx`为jenkins job名. 否则会出现`W0403 Relative import 'xxxx'警告`


## 例子
#### 创建检查的支持pylint的job
```python
import lintjenkins
lj = LintJenkins('jenkins_url', username='',
                 password='')
lj.add_job('svn_url',
           'username', 'password', job_name='xxx')
```

#### 获取代码检查结果
```python
lj = LintJenkins('jenkins_url', username='',
                password='')

numbers = lj.get_build_numbers('job_name') # 全部的任务构建号
for number in numbers:
    try:
        print(lj.get_build_info('job_name',number))
    except Exception as e:
        print('bad number:', number,e)
```

获取一次`number`检查结果格式为:
```json
{
    "violation_info": {
        "violation_num": 1844,
        "violation_file_num": 75
    },
    "commits": [
        {
            "msg": "svn提交信息",
            "paths": [
                {
                    "editType": "add",
                    "file": "新增的文件"
                },
                {
                    "editType": "edit",
                    "file": "编辑的文件"
                }
            ],
            "revision": 18830,
            "datetime": "2017-06-12 09:44:38",
            "author": "huzhongzhong"
        }
    ],
    "datetime": "2017-06-12 09:55:13",
    "result_url":'http://x.x.x.x:8080/job/job_name/7/violations/'
    "result": "UNSTABLE",
    "duration": 49,
    "revisions": [
        {
            "module": "svn地址",
            "revision": 18830
        }
    ]
}
```
各个字段说明:

| 字段                                | 含义                                      |
| --------------------------------- | --------------------------------------- |
| violation_info.violation_num      | pylint 告警数(高、中、低之和)                     |
| violation_info.violation_file_num | pylint检查的文件个数                           |
| datetime                          | 触发构建时间                                  |
| duration                          | 任务持续时间,即代码检查耗时                          |
| result                            | 检查结果,取值为: FAILURE、UNSTABLE、SUCCESS、null |
| result_url                        | 检查结果详细页面,可以看到每一个被检查文件的变化等.              |
| revisions.module                  | svn地址                                   |
| revisions.revision                | svn分支版本号                                |
| commits.msg                       | 本次提交信息                                  |
| commits.paths                     | 修改文件信息(修改类型、文件)                         |
| commits.revision                  | 本次修改分支号                                 |
| commits.author                    | 提交者                                     |
| commits.datetime                  | 提交日期                                    |



## 后续
目前已经可以通过命令行去创建一个支持pylint检查的job,以及获取每一次检查的结果(告警数等). 可以基于此实现一个代码检查系统(web版). 

## 参考
- https://github.com/pycontribs/jenkinsapi/tree/master/examples/how_to

## TODO
- 将lintjenkins单独打包

