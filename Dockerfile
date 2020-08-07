FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY . /visionlabs_test_task

RUN pip install -U pip
RUN pip install -r /visionlabs_test_task/requirements.txt

WORKDIR /visionlabs_test_task
