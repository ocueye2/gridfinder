from python:3.12.3-slim

copy . .

Expose 8080

Run pip install -r requirements.txt

CMD ["python","main.py"]