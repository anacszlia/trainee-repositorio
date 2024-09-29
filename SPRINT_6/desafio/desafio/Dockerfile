FROM python:3.12

WORKDIR /app

RUN mkdir -p /app/dados_csv

COPY . .

COPY Filmes+e+Series/ ./dados_csv

RUN pip install boto3 python-dotenv

VOLUME /app/dados_csv

CMD ["python", "./scriptDesafio6.py"]