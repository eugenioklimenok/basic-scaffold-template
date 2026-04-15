# Guía de Usuario

## Qué hace `new-scaffold`

`new-scaffold` crea la estructura base de un proyecto dentro de una ruta destino, siguiendo convenciones comunes y sin instalar paquetes ni modificar la configuración del host.

## Cuándo usarlo

Usalo cuando necesites:

- crear un proyecto nuevo con una estructura consistente
- evitar crear carpetas y archivos base a mano
- estandarizar proyectos `generic`, `api`, `bot` o `worker`
- validar nombres y conflictos antes de escribir archivos

## Qué genera

Base común:

- `src/`
- `config/`
- `scripts/`
- `docs/`
- `tests/`
- `logs/`
- `tmp/`
- `data/`
- `.env.example`
- `README.md`

Extras por tipo:

- `api`: `src/api/entrypoint.example`
- `bot`: `src/bot/entrypoint.example`
- `worker`: `src/worker/entrypoint.example`
- `generic`: no agrega extras específicos

Opcionales:

- `.gitignore` con `--with-gitignore`
- `Makefile` placeholder con `--with-makefile`
- scripts placeholder con `--with-scripts`

## Reglas importantes

- El nombre del proyecto debe estar en `kebab-case`.
- El `--base-path` debe existir y ser escribible.
- Si la carpeta destino existe y está vacía, se requiere `--force`.
- Si la carpeta destino existe y no está vacía, solo se permite continuar si el contenido coincide exactamente con el scaffold esperado.
- `--dry-run` muestra el plan exacto sin escribir archivos.
- La salida puede ser `text` o `json`.

## Comando base

```bash
python3 ./bin/new-scaffold NOMBRE --base-path RUTA
```

Ejemplo:

```bash
python3 ./bin/new-scaffold soporte-bot --base-path /home/alex/apps --type bot --owner alex
```

## Flags disponibles

### `name`

Nombre del proyecto. Es posicional y obligatorio.

### `--base-path`

Ruta raíz donde se creará la carpeta del proyecto. Obligatorio.

### `--type`

Tipo de scaffold:

- `generic`
- `api`
- `bot`
- `worker`

Default: `generic`

### `--owner`

Etiqueta informativa para dejar asentado el propietario esperado del proyecto.

### `--force`

Permite reutilizar una carpeta destino existente solo si está vacía.

### `--dry-run`

Muestra qué directorios y archivos crearía, sin escribir nada.

### `--output json|text`

Define el formato de salida.

- `text`: lectura humana
- `json`: integración con scripts u otras herramientas

### `--with-gitignore`

Agrega `.gitignore` base.

### `--with-makefile`

Agrega `Makefile` neutral con targets placeholder.

### `--with-scripts`

Agrega archivos `.example` en `scripts/` para completar según el stack real.

## Comportamiento esperado

### Ejecución normal

Si el destino no existe, crea la carpeta del proyecto y todo el contenido esperado.

### Ejecución con `--dry-run`

No crea nada. Solo informa qué acciones haría.

### Segunda ejecución sobre el mismo proyecto

Si el contenido ya coincide con lo esperado, responde sin romper nada y marca que no hubo cambios.

### Conflictos

Si encuentra archivos no gestionados o contenido distinto al esperado, devuelve error controlado.

## Exit codes

- `0`: éxito
- `2`: error funcional de validación
- `3`: uso incorrecto del CLI
- `4`: conflicto en destino

## Qué hacer después de generar el scaffold

Después de crear el proyecto, completá los placeholders:

- definir el entrypoint real del proyecto
- reemplazar scripts `.example` por scripts reales
- completar el `Makefile` si aplica
- completar `README.md` y `.env.example` con datos del proyecto
