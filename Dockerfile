FROM ghcr.io/prefix-dev/pixi:0.34.0 AS build

WORKDIR /app

ENV PATH="${PATH}:/root/.pixi/bin:/root/.local/bin"

# Copy in pixi lock to avoid solve time
COPY pixi.lock pyproject.toml README.md ./
COPY .git/ .git/

RUN mkdir classification && pixi install -e prod

# Build the shell-hook script to be used as the container entrypoint
RUN pixi shell-hook -e prod -s bash > /shell-hook
RUN echo "#!/bin/bash" > /app/entrypoint.sh
RUN cat /shell-hook >> /app/entrypoint.sh
RUN echo 'exec "$@"' >> /app/entrypoint.sh

# Initiate second stage build to minimise container size
FROM ubuntu:24.04 AS production

COPY --from=build /app /app
COPY --from=build --chmod=0755 /app/entrypoint.sh /app/entrypoint.sh
COPY ./classification /app/classification

WORKDIR /app
EXPOSE 8080
COPY . .
ENV PATH="${PATH}:/root/.pixi/bin:/root/.local/bin"
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD ["gunicorn", "-b" ,":8080" ,"--workers", "3", "--timeout", "0", "classification.app:app"]