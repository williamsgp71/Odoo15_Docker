FROM odoo:15.0
USER root
RUN apt-get update || true
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# RUN apt -y install python-pandas || true
RUN chmod 777 -R /home/