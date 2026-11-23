FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends chromium chromium-driver fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir selenium pytest

WORKDIR /tests
COPY test_site.py .

ENV BASE_URL=http://staging
ENV RESULTS_DIR=/results
RUN mkdir -p /results

CMD ["pytest", "-v", "test_site.py", "--junitxml=/results/junit.xml"]
