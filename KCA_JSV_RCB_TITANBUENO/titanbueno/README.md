# RETOTITAN_KCA_JSV_RCB

Paquete minimo con:

- la pagina web en `index.html`;
- las imagenes necesarias en `assets/figures/`;
- el codigo Python de calculos en `src/titan/`.

## Abrir la pagina web

1. Descomprime el zip.
2. Abre `index.html`.
3. Si quieres, abre ese archivo con Google Chrome.
4. Tambien puedes ejecutar `ABRIR_EN_GOOGLE_CHROME.bat`.

## Estructura

- `index.html`: pagina web principal.
- `assets/figures/`: imagenes usadas por la web.
- `src/titan/`: codigo fuente de calculo y generacion.
- `requirements.txt`: dependencias.

## Ejecutar el codigo Python

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
set PYTHONPATH=src
python -m titan.main
```

Si ejecutas `src/titan/main.py` directamente, el script intentara instalar automaticamente las dependencias de `requirements.txt` si faltan en el entorno.
