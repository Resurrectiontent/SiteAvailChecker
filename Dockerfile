FROM python:3
ADD main.py /
RUN pip3 install -r ./requirements.txt
CMD [ "python3", "./main.py" ]