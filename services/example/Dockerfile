FROM python:3
WORKDIR /code/
ENV PYTHONUNBUFFERED=1

# Install Requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && \
	rm /tmp/requirements.txt

# Install module into container
ENV PYTHONPATH "${PYTHONPATH}:/code/"
COPY example /code/example

# Run module
ENTRYPOINT ["python3", "-m", "example"]
