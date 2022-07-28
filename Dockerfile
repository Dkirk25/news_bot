FROM python:3.7.10

COPY . /opt/apps/news_bot
WORKDIR /opt/apps/news_bot

# --use-deprecated=legacy-resolver until pip 21 is fixed
RUN pip install --no-cache-dir -r requirements.txt --use-deprecated=legacy-resolver
CMD [ "python", "main.py" ]
