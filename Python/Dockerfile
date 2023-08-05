FROM python:3.10.7

# Disable SSL verification
ENV PYTHONHTTPSVERIFY=0

# Install necessary packages
RUN apt-get update && \
    apt-get install -y openssl && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install cron package
RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Run the ETL script every Monday at 2am
RUN echo "0 0 * * 4 cd /app && python3 main.py" >> /etc/crontab

CMD ["cron", "-f"]

