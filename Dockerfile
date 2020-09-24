FROM python:3.8.5

COPY . /opt/apps/news_bot
WORKDIR /opt/apps/news_bot

RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "main.py" ]