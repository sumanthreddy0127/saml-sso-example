FROM python:3.9-slim

WORKDIR /app

RUN python -m pip install flask xmltodict

ENV PYTHONBUFFERED=1

# mount the file sp_server.py into /app as a volume externally

CMD ["python", "-u", "/home/sp_server.py"]
