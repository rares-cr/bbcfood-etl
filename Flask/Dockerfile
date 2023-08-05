FROM python:3.10.7

WORKDIR /app

COPY . /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
