# syntax=docker/dockerfile:1
ARG PLONE_VERSION=6.0.0
FROM plone/plone-backend:${PLONE_VERSION}


LABEL maintainer="Plone Foundation <collective@plone.org>" \
      org.label-schema.name="demo-backend" \
      org.label-schema.description="Plone 6 Demo Site backend image." \
      org.label-schema.vendor="Plone Foundation"

# Add local code
COPY . .

# Install local requirements and fix permissions
RUN <<EOT
    ./bin/pip install mxdev
    mv requirements-docker.txt requirements.txt
    ./bin/mxdev -c mx.ini
    ./bin/pip install -r requirements-mxdev.txt
    chown -R plone: /app
EOT

# Create a new site with content
RUN <<EOT
    ADDITIONAL_PROFILES=plone6demo:initial
    ./docker-entrypoint.sh create-site
EOT
