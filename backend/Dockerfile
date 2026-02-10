# syntax=docker/dockerfile:1
ARG SEED=1000
ARG PLONE_VERSION=6.1.4
FROM plone/server-builder:${PLONE_VERSION} AS builder

WORKDIR /app


# Add local code
COPY scripts/ scripts/
COPY . src

# Install local requirements and pre-compile mo files
RUN <<EOT
    set -e
    bin/pip install mxdev uv
    mv src/requirements-docker.txt src/requirements.txt
    sed -i 's/-e .\[test\]/./g' src/mx.ini
    cd /app/src
    # remove potentially existing virtualenv from local build
    rm -rf .venv
    ../bin/mxdev -c mx.ini
    ../bin/uv pip install -r requirements-mxdev.txt
    ../bin/python /compile_mo.py
    cd /app
    rm -Rf src/
EOT

FROM plone/server-prod-config:${PLONE_VERSION}

LABEL maintainer="Plone Foundation <collective@plone.org>" \
    org.label-schema.name="demo-backend" \
    org.label-schema.description="Plone 6 Demo Site backend image." \
    org.label-schema.vendor="Plone Foundation"

# Copy /app from builder
COPY --from=builder /app /app

RUN <<EOT
    set -e
    ln -s /data /app/var
    # Create a new site with content
    cat ${SEED} > /app/__created__.txt
    SEED=${SEED} ./docker-entrypoint.sh create-site
EOT
