FROM python:3.7.2

ENV PYTHONUNBUFFERED 1
  
RUN mkdir -p /var/www/html/api
WORKDIR /var/www/html/api
COPY ./backend /var/www/html/api
 
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
 
# because github don't upload empty folder, static is not in the repo.
# Docker-compose will generate static folder because it is written in volume.
# This static folder is owned by root. Not newuser, chmod in dockerfile can 't
# change it.
# but media has product image, the repo has media folder.

# don't work as root  
RUN useradd -ms /bin/bash newuser
RUN chown -R newuser:newuser /var/www/html/
RUN chmod -R 755 /var/www/html/api
USER newuser

# 去除windows系统编辑文件中多余的\r回车空格
RUN sed -i 's/\r//' ./start.sh
RUN chmod +x ./start.sh
