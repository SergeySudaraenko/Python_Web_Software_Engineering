FROM python:3.12.3

RUN pip install personal_assistant

COPY ./HW2_2.py /app/HW2_2.py

WORKDIR /app

CMD ["personal_assistant"]

