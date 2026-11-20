# Monitor de estabilidad de la aplicación APP-07

Programa de menú que analiza las descargas y las caídas semanales de una aplicación móvil
publicada: listado, resumen, estabilidad de cada semana, búsqueda por umbral, mejor racha,
previsión de crecimiento, consulta de una semana y comprobación de los datos.

**Módulo:** IC44 — Fundamentos de programación en Python
**Unidad:** 2 — Estructuras de control, depuración y excepciones
**Pareja:** 07
**Autores:** Juan Francisco García Díaz · Diego Esteban Sánchez Navarro

## Aplicación analizada

| Dato | Valor |
|---|---|
| Código | APP-07 |
| Nombre | Rutas en Bici |
| Semanas | 12 |

## Ejecución desde Docker Hub

No hace falta descargar el repositorio ni tener Python instalado. Solo Docker. El programa
pide datos por teclado, así que se ejecuta con `-it`.

```bash
docker run --rm -it desn2001/monitor-app-07:1.0.0
```

Página de la imagen: https://hub.docker.com/r/desn2001/monitor-app-07

## Ejecución en local

Requiere Python 3.10 o superior.

```bash
python3 -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
python monitor_app.py
```

## Construir la imagen

```bash
docker build -t monitor-app-07 .
docker run --rm -it monitor-app-07
```

## Estructura del proyecto

```
.
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
└── monitor_app.py
```
