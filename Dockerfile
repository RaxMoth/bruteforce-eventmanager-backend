FROM --platform=linux/amd64 python:3.9.5-slim-buster
# set work directory
WORKDIR /usr/

# set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/src/:/usr/src/app/:/usr/src/"

#setting up the virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python -m pip install --upgrade pip

# copy requirements file
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

# copy project
COPY . /usr/

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app



