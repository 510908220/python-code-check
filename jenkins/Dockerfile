FROM jenkins/jenkins:lts
# if we want to install via apt
USER root
RUN apt-get update && apt-get install -y python-pip libmariadbd18 libmariadbd-dev python-mysqldb
RUN pip install virtualenv
# drop back to the regular jenkins user - good practice
USER root