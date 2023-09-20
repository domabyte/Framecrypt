FROM python:latest
COPY . /App 
WORKDIR /App
RUN pip install -r requirements.txt 
CMD ["python", "main.py"]
