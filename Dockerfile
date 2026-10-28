FROM ghcr.io/fedlearnnet/python-tool-api/base-python-dep:0.7.15.dev

USER 0

RUN set -eux; \
    if command -v apk >/dev/null 2>&1; then \
        apk add --no-cache python-3.11-dev make; \
    elif command -v apt-get >/dev/null 2>&1; then \
        apt-get update; \
        apt-get install -y --no-install-recommends python-3.11-dev make; \
        rm -rf /var/lib/apt/lists/*; \
    else \
        echo "Unsupported package manager: need python3 headers and a C++ compiler for PyTensor"; \
        exit 1; \
    fi

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /home/nonroot/.pytensor \
 && chown -R nonroot:nonroot /app /opt/venv /home/nonroot \
 && chmod -R u+rwX,g+rwX /app

ENV MPLBACKEND=Agg

USER nonroot:nonroot
CMD ["python", "-m", "main"]
