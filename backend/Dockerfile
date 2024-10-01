FROM python:3.12.6-slim-bullseye

# Set up the work directory
WORKDIR /app

# User and group IDs
ARG UID=1000
ARG GID=1000

# Install dependencies and set up the user
RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential \
	&& rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
	&& apt-get clean \
	&& groupadd -g "${GID}" escore \
	&& useradd --create-home --no-log-init -u "${UID}" -g "${GID}" escore \
	&& chown -R escore:escore /app

USER escore

# Install the requirements
COPY --chown=escore:escore requirements.txt .
RUN python3 -m venv /home/escore/venv
RUN /home/escore/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY --chown=escore:escore . .
CMD ["/home/escore/venv/bin/python3", "main.py"]
