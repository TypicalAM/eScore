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
	&& groupadd -g "${GID}" hackyeah \
	&& useradd --create-home --no-log-init -u "${UID}" -g "${GID}" hackyeah \
	&& chown -R hackyeah:hackyeah /app

USER hackyeah

# Install the requirements
COPY --chown=hackyeah:hackyeah requirements.txt .
RUN python3 -m venv /home/hackyeah/venv
RUN /home/hackyeah/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY --chown=hackyeah:hackyeah . .
CMD ["/home/hackyeah/venv/bin/python3", "main.py"]
