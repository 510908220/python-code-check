# -*- encoding:utf-8 -*-

"""
Jenkins 证书管理, 基于jenkinsapi. 目前实现功能:
1. 根据svn地址、用户名和密码获取证书id

使用:

jscm = SvnCredentialManager('http://ip:8080', username='username',
                                   password='token')
print jscm.get_svn_credential("svn", 'username',
                              'password')

"""

import hashlib

import requests
from jenkinsapi.credential import UsernamePasswordCredential
from jenkinsapi.jenkins import Jenkins as JenkinsEx


class SvnCredentialManager(object):

    def __init__(self, jenkins_url, username, password):
        self.jenkins_url = jenkins_url
        if self.jenkins_url[-1] == "/":
            self.jenkins_url = self.jenkins_url[:-1]
        self.jenkins = JenkinsEx(self.jenkins_url, username=username,
                                 password=password)

    def _get_svn_md5(self, svn):
        m = hashlib.md5()
        m.update(svn.encode('utf-8'))
        return m.hexdigest()

    def _get_or_create_svn_credential(self, svn, username, password):
        creds_description = self._get_svn_md5(svn)
        if creds_description not in self.jenkins.credentials.keys():
            cred_dict = {
                'description': creds_description,
                'userName': username,
                'password': password
            }
            self.jenkins.credentials[
                creds_description] = UsernamePasswordCredential(cred_dict)

        return self.jenkins.credentials[creds_description].credential_id

    def _check_credential(self, svn, credential_id):
        check_svn_url = "{jenkins_url}/job/tmp/descriptorByName/hudson.scm.SubversionSCM$ModuleLocation/checkCredentialsId".format(
            jenkins_url=self.jenkins_url)

        r = requests.get(check_svn_url, params={
            'value': credential_id,
            'remote': svn
        })
        return r.text == "<div/>"

    def get_svn_credential(self, svn, username, password):
        credential_id = self._get_or_create_svn_credential(
            svn, username, password)
        if not self._check_credential(svn, credential_id):
            del self.jenkins.credentials[self._get_svn_md5(svn)]
            raise Exception("check credential failed")
        return credential_id
