FROM python:3
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
CMD python app.py
# CMD uwsgi --http 0.0.0.0:80 --wsgi-file app.py --callable app --processes 4 --threads 2 --stats 0.0.0.0:9191