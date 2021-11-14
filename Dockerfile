FROM python:3.6

RUN mkdir -p /home/app /home/db

COPY ./app /home/app

# set default dir so that next commands executes in /home/app dir
WORKDIR /home/app

# will execute npm install in /home/app because of WORKDIR
RUN pip install -r requirements.txt

EXPOSE 6000

# no need for /home/app/server.js because of WORKDIR
CMD ["python", "main.py"]