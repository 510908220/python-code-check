FROM ubuntu:14.04

MAINTAINER WestDoorBlowCola

# 国内安装软件太慢,更新为阿里云源
COPY ./config/apt/sources.list.14.04 /etc/apt/sources.list
# Install required packages and remove the apt packages cache when done.
# 监控要用到ssh,所以这里加上了openssh-server
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        build-essential \
        libssl-dev \
        libffi-dev \
        python \
        python-dev \
         python-pip \
        nginx \
        git \
        supervisor \
        sqlite3 \
        python-mysqldb \
        openssh-server \
        p7zip-full \
        curl \
  && rm -rf /var/lib/apt/lists/*

# 安装nodejs
RUN curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
RUN apt-get update && sudo apt-get install -y nodejs
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org

# 设置阿里云pypi源,加快下载速度
COPY  ./config/pip/pip.conf /root/.pip/pip.conf
# 更新PIP并且清除整个缓存保证pip是最新的
# RUN pip install -U pip
# RUN hash -r

# setup all the configfiles
# RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY ./config/nginx/nginx-app.conf /etc/nginx/sites-available/default
#COPY supervisor-app.conf /etc/supervisor/conf.d/

COPY ./src/  /docker/src/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installinig (all your) dependencies when you made a change a line or two in your app.
RUN pip install -r /docker/src/requirements/prod.txt

RUN export TERM=xterm # 会出现错误TERM environment variable not set

# add (the rest of) our code
WORKDIR /docker/src/

# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
# ENTRYPOINT ["python","/code/upgrade.py"]
# CMD ["--help"]
