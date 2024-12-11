FROM python:3.7
RUN apt-get update && apt-get -y install cron
WORKDIR /app/pynod
COPY pynod-mirror-tool/ .
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
RUN pip install -r /app/pynod/requiments.txt
CMD ["cron", "-f", "-l", "8"]
