FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN rm ./.env

RUN rm -r ./media/recipes

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ] 