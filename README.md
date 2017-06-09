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
#### step1:创建 检查的job
```python
import lintjenkins
lj = LintJenkins('jenkins_url', username='',
                 password='')
lj.add_job('svn_url',
           'username', 'password', job_name='xxx')
```


