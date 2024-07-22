FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD ["gunicorn", "msmeEcomm.wsgi:application", "--bind", "0.0.0.0:8000"]