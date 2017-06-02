from lintjenkins import LintJenkins


if __name__ == "__main__":
    lj = LintJenkins('jenkins_url', username='username',
                     password='token')

    lj.add_job('svn', 'uusername', 'passwd', job_name='job_name')
