FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pillow

COPY src/ /app/src/
COPY generate.py /app/

ENTRYPOINT ["python", "generate.py"]
CMD ["MakdumIbrohim", "game.svg"]
