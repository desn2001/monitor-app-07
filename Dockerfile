FROM python:3.14-slim

LABEL org.opencontainers.image.title="monitor-app-07" \
      org.opencontainers.image.description="Monitor de estabilidad de Rutas en Bici" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="Diego Sanchez Navarro, Juan Francisco García Díaz " \
      org.opencontainers.image.source="https://github.com/desn2001/monitor-app-07"

WORKDIR /app

COPY monitor_app.py .

CMD ["python", "monitor_app.py"]

