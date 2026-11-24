FROM python:3.12-slim
RUN useradd -m -u 1000 runner
WORKDIR /work
RUN pip install --no-cache-dir pytest coverage
USER runner
# Run with: --network none --memory 512m, and a 60s timeout enforced by the caller.
CMD ["pytest", "-x", "-q"]
