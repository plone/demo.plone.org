FROM plone/plone-backend:6.0.0a1

LABEL maintainer="Plone Community <dev@plone.org>" \
      org.label-schema.name="demo-6" \
      org.label-schema.description="Plone 6 Demo: Backend Image" \
      org.label-schema.vendor="Plone Foundation" \
      org.label-schema.docker.cmd="docker run -d -p 8080:8080 plone/demo-6:backend"

RUN rm -Rf /app/var &&\
    mkdir -p /app/var/filestorage /app/var/blobstorage /app/var/cache /app/var/log &&\
    /app/docker-entrypoint.sh create-volto
