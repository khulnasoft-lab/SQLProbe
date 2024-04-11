FROM python:latest

RUN apt-get update && apt-get install -y git && \
    git clone https://github.com/khulnasoft-lab/sqlprobe.git /sqlprobe

WORKDIR /sqlprobe

RUN pip install --no-cache-dir -r requirements.txt && \
    python setup.py install

ENTRYPOINT ["python", "sqlprobe.py"]
CMD ["--help"]
