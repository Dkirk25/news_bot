FROM python:3.7.9

COPY . /opt/app/news_bot
WORKDIR /opt/app/news_bot

RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "main.py" ]