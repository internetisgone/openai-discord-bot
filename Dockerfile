FROM python:3.11.3
WORKDIR /bot
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python3 main.py