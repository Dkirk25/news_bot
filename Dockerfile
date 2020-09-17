FROM python:3.7.9

RUN mkdir -p /opt/app/news-bot

WORKDIR /opt/app/news-bot/news_bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]