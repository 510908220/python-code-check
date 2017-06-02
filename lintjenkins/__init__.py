# -*- encoding: utf-8 -*-

import jenkins

from . import template
from . import credentials


class LintException(Exception):
    pass


class LintJobExistException(LintException):
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

    def add_job(self, svn, username, password, job_name=None, description=""):

        # step1: 确保job不存在
        if not job_name:
            job_name = svn.split("/")[-1].strip()

        if self.jenkins_server.get_job_name(job_name):
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
