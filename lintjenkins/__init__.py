# -*- encoding: utf-8 -*-


import pendulum
try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin

from pyquery import PyQuery as pq
import jenkins

from . import template
from . import credentials


class LintException(Exception):
    pass


class LintJobExistException(LintException):
    pass


class LintJobFailedException(LintException):
    pass


class LintJobRuningdException(LintException):
    pass


class LintJenkins(object):

    def __init__(self, jenkins_url, username, password):
        self.jenkins_url = jenkins_url
        self.username = username
        self.password = password
        self.jenkins_server = jenkins.Jenkins(
            self.jenkins_url,
            username=self.username,
            password=self.password)
        self.svn_credential_manager = credentials.SvnCredentialManager(
            self.jenkins_url,
            username=self.username,
            password=self.password)

    def add_job(self, svn, username, password, job_name, description=""):
        """
        根据svn创建一个支持pylint的jenkins job，进行代码检查.
        """

        # step1: 确保job不存在
        if self.jenkins_server.job_exists(job_name):
            raise LintJobExistException("lint job has exist")

        # step2: 获取创建job需要的认证id
        credential_id = self.svn_credential_manager.get_svn_credential(
            svn,
            username,
            password)

        # step3: 创建支持pylint检查代码的job
        # description, remote, credentialsid
        self.jenkins_server.create_job(
            job_name, template.JOB_CONFIG_PYLINT % ("", svn, credential_id))

    def get_build_numbers(self, job_name):
        """
         以后需要获取全部job构建号.
        """
        job_info = self.jenkins_server.get_job_info(
            job_name, fetch_all_builds=True)
        return [build['number'] for build in job_info['builds']]

    def _get_job_violation(self, job_name, build_no):
        """
        获取violations页面这里的. 由于目前没找到直接获取代码检查结果信息的接口,这里就暂时抓取页面提取信息
        Type	Violations	Files in violation
        pylint	845 (+6)	71 (+1)
        这里只考虑pylint一种检查,如果是多种检查的话应该就需要修改代码了.
        """
        def get_td_value(td_element):
            """
            一般的值都是为<td>666</td>,当有颜色时(比如警格个数变化)会多一个<span>子元素.
            """
            try:
                text = td_element.find('span').text.strip()
            except:
                text = td_element.text.strip()
            return int(text.split("(")[0].strip())

        url = urljoin(self.jenkins_url,
                      "job/{job_name}/{build_no}/violations/".format(
                          job_name=job_name,
                          build_no=build_no)
                      )

        d = pq(url)

        td_elements = d(
            "#main-panel > table:nth-child(3) > tbody > tr:nth-child(2) td")

        return {
            'violation_num': get_td_value(td_elements[1]),
            'violation_file_num': get_td_value(td_elements[2])
        }

    def get_build_info(self, job_name, build_no):
        """
        获取某一次构建信息
        """
        job_build_info = self.jenkins_server.get_build_info(job_name, build_no)
        result = job_build_info['result']  # FAILURE、UNSTABLE、SUCCESS、null
        if result == 'FAILURE':
            raise LintJobFailedException('build number is %s' % build_no)
        if not result:
            raise LintJobRuningdException('build number is %s' % build_no)

        # 1. 基础构建信息
        build_info = {
            'datetime':  pendulum.from_timestamp(job_build_info['timestamp'] / 1000, 'Asia/Shanghai').to_datetime_string(),
            'duration': job_build_info['duration'] / 1000,
            'result': job_build_info['result'],
            'revisions': job_build_info['changeSet']['revisions'],
            'commits': [],
            'violation_info': {

            },
            'result_url': urljoin(
                self.jenkins_url,
                "job/{job_name}/{build_no}/violations/".format(
                    job_name=job_name,
                    build_no=build_no)
            )
        }

        # 2. 开发者提交信息
        for item in job_build_info['changeSet']['items']:
            build_info['commits'].append({
                'author': item['author']['fullName'],
                'revision': item['revision'],
                'msg': item['msg'],
                'datetime': pendulum.from_timestamp(item['timestamp'] / 1000, 'Asia/Shanghai').to_datetime_string(),
                'paths': item['paths']
            })

        # 3. 代码检查信息
        build_info['violation_info'] = self._get_job_violation(
            job_name, build_no)
        return build_info
