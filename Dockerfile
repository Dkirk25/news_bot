FROM python:3.7.9

COPY . /opt/app/news_bot
WORKDIR /opt/app/news_bot

RUN apt-get update -y
RUN apt install docker.io -y
RUN apt-get install git -y
RUN systemctl enable --now docker
RUN usermod -aG docker donald

RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "main.py" ]