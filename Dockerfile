# version python
FROM python:3.10

# file Dir 
WORKDIR /code

# copy to docker pip install on document
COPY ./requirements.txt /code/requirements.txt

# cmd install 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]