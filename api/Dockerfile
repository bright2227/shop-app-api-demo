FROM python:3.7.2

ENV PYTHONUNBUFFERED 1
  
RUN mkdir -p /var/www/html/api
 
WORKDIR /var/www/html/api
 
ADD . /var/www/html/api
 
RUN /usr/local/bin/python -m pip install --upgrade pip
 
RUN pip install -r requirements.txt
 
# 去除windows系统编辑文件中多余的\r回车空格
RUN sed -i 's/\r//' ./start.sh
# 给start.sh可执行权限
RUN chmod +x ./start.sh
