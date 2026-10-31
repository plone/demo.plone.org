# syntax=docker/dockerfile:1
ARG AURORA_VERSION=1.0.0-alpha.21
FROM plone/aurora-builder:${AURORA_VERSION} AS builder

# The proxy terminates TLS, so React Router sees actions as `http` while the
# browser sends an `https` origin. The hosts listed here are accepted as action
# origins. React Router reads them when building, not when the server runs.
ARG REACT_ROUTER_ALLOWED_ACTION_ORIGINS=aurora.demo.plone.org
ENV REACT_ROUTER_ALLOWED_ACTION_ORIGINS=${REACT_ROUTER_ALLOWED_ACTION_ORIGINS}

COPY --chown=node packages/plone-aurora-demo /app/packages/plone-aurora-demo
COPY --chown=node registry.config.ts /app/
COPY --chown=node Makefile /app/Makefile
COPY --chown=node pnpm-workspace.yaml /app/pnpm-workspace.yaml
COPY --chown=node .pnpmfile.cjs /app/.pnpmfile.cjs
COPY --chown=node package.json /app/package.json
COPY --chown=node pnpm-lock.yaml /app/pnpm-lock.yaml

RUN --mount=type=cache,id=pnpm,target=/app/.pnpm-store,uid=1000 <<EOT
    set -e
    export CI=true
    pnpm install && make build-deps
    pnpm build
    # This is necessary because the build is trying to recreate the node_modules folder
    # by telling it to CI=1 it will just recreate them
    CI=1 pnpm install --prod
EOT

FROM plone/aurora-prod-config:${AURORA_VERSION}

LABEL maintainer="Plone Community <collective@plone.org>" \
      org.label-schema.name="plone-aurora-demo-frontend" \
      org.label-schema.description="Plone Aurora demo site frontend image." \
      org.label-schema.vendor="Plone Community"

COPY --from=builder /app/ /app/

RUN <<EOT
    set -e
    # CI=true keeps corepack/pnpm non-interactive: if it decides to reconcile the
    # copied node_modules it must not block on a modules-purge confirmation
    # prompt (there is no TTY during the image build).
    export CI=true
    corepack enable pnpm
    corepack use pnpm@12.14.0
    corepack prepare pnpm@12.14.0 --activate
EOT

ENTRYPOINT [ "pnpm" ]
CMD ["start:prod"]
