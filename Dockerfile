FROM python:3.10.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "CulturTap.main:app","--host", "0.0.0.0", "--port","8080" ]

# FROM amazon/aws-lambda-python:3.10

# # Install the function's dependencies using file requirements.txt
# # from your project folder.

# COPY requirements.txt  .
# RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# # Copy function code
# COPY . ${LAMBDA_TASK_ROOT}

# # Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
# CMD [ "CulturTap.main.handler" ] 