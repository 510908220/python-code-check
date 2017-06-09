# -*- encoding: utf-8 -*-

# 注意配置要紧邻''',有换行的话jenkins会报错.

JOB_CONFIG_PYLINT = '''<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description>%s</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.scm.SubversionSCM" plugin="subversion@2.6">
    <locations>
      <hudson.scm.SubversionSCM_-ModuleLocation>
        <remote>%s</remote>
        <credentialsId>%s</credentialsId>
        <local>.</local>
        <depthOption>infinity</depthOption>
        <ignoreExternalsOption>true</ignoreExternalsOption>
      </hudson.scm.SubversionSCM_-ModuleLocation>
    </locations>
    <excludedRegions></excludedRegions>
    <includedRegions></includedRegions>
    <excludedUsers></excludedUsers>
    <excludedRevprop></excludedRevprop>
    <excludedCommitMessages></excludedCommitMessages>
    <workspaceUpdater class="hudson.scm.subversion.UpdateUpdater"/>
    <ignoreDirPropChanges>false</ignoreDirPropChanges>
    <filterChangelog>false</filterChangelog>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers>
    <hudson.triggers.SCMTrigger>
      <spec>H/2 * * * *</spec>
      <ignorePostCommitHooks>false</ignorePostCommitHooks>
    </hudson.triggers.SCMTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>if [ ! -d /opt/env/$JOB_NAME ]; then
    virtualenv -p /usr/bin/python /opt/env/$JOB_NAME
fi
source /opt/env/$JOB_NAME/bin/activate
pip install pylint
pip install pylint-django
pip install ${WORKSPACE}/requirements.txt
root_package_file=&quot;${WORKSPACE}/__init__.py&quot;
if [ ! -f $root_package_file ]; then
    touch $root_package_file
fi
pylint --load-plugins pylint_django --rcfile=${WORKSPACE}/pylint.cfg  ${WORKSPACE} &gt; pylint.xml || exit 0
</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <hudson.plugins.violations.ViolationsPublisher plugin="violations@0.7.11">
      <config>
        <suppressions class="sorted-set"/>
        <typeConfigs>
          <entry>
            <string>checkstyle</string>
            <hudson.plugins.violations.TypeConfig>
              <type>checkstyle</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>codenarc</string>
            <hudson.plugins.violations.TypeConfig>
              <type>codenarc</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>cpd</string>
            <hudson.plugins.violations.TypeConfig>
              <type>cpd</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>cpplint</string>
            <hudson.plugins.violations.TypeConfig>
              <type>cpplint</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>csslint</string>
            <hudson.plugins.violations.TypeConfig>
              <type>csslint</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>findbugs</string>
            <hudson.plugins.violations.TypeConfig>
              <type>findbugs</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>fxcop</string>
            <hudson.plugins.violations.TypeConfig>
              <type>fxcop</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>gendarme</string>
            <hudson.plugins.violations.TypeConfig>
              <type>gendarme</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>jcreport</string>
            <hudson.plugins.violations.TypeConfig>
              <type>jcreport</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>jslint</string>
            <hudson.plugins.violations.TypeConfig>
              <type>jslint</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>pep8</string>
            <hudson.plugins.violations.TypeConfig>
              <type>pep8</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>perlcritic</string>
            <hudson.plugins.violations.TypeConfig>
              <type>perlcritic</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>pmd</string>
            <hudson.plugins.violations.TypeConfig>
              <type>pmd</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>pylint</string>
            <hudson.plugins.violations.TypeConfig>
              <type>pylint</type>
              <min>10</min>
              <max>500</max>
              <unstable>500</unstable>
              <usePattern>false</usePattern>
              <pattern> pylint.xml</pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>simian</string>
            <hudson.plugins.violations.TypeConfig>
              <type>simian</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
          <entry>
            <string>stylecop</string>
            <hudson.plugins.violations.TypeConfig>
              <type>stylecop</type>
              <min>10</min>
              <max>999</max>
              <unstable>999</unstable>
              <usePattern>false</usePattern>
              <pattern></pattern>
            </hudson.plugins.violations.TypeConfig>
          </entry>
        </typeConfigs>
        <limit>100</limit>
        <sourcePathPattern></sourcePathPattern>
        <fauxProjectPath></fauxProjectPath>
        <encoding>default</encoding>
      </config>
    </hudson.plugins.violations.ViolationsPublisher>
  </publishers>
  <buildWrappers/>
</project>
'''
