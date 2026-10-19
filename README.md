# Pokémon Battle Web

Aplicación web interactiva desarrollada con **Flask**, **Jinja2** y **CSS** para la gestión de Pokémon y simulación visual de combates en tiempo real.

---

## Descripción

**Pokémon Battle Web** es un proyecto enfocado en la construcción de una aplicación web dinámica. Permite a los usuarios registrarse como Entrenadores, explorar y filtrar un catálogo completo de Pokémon, inspeccionar estadísticas detalladas y participar en enfrentamientos en una arena visual estilo.

---

## Tecnologías 

- **Backend:** Python 3, Flask framework.
- **Frontend:** HTML5, CSS, Jinja2 Templating.
- **Fuente de Datos:** JSON local (`pokemons-ugly.json`).

---

## Instalación y Configuración

### 1. Clonar el repositorio:
```bash
git clone https://github.com/molinaastrid833-spec/Proyecto_pokemon.git

cd Proyecto_pokemon
```

### 2. Crear el entorno virtual:
```bash
python -m venv .venv
```

### 3. Activar el entorno virtual:
- **Windows PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (de instituto por restricciones):**
  ```powershell
  (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)
  ```

### 4. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación:
```bash
python main.py
```
O mediante el CLI de Flask:
```bash
python -m flask --app main run --port 8080
```

---

## Interacción del Usuario

1. **Bienvenida (inicio) (`/`):**
   El usuario ingresa a la aplicación, presencia un Pokémon destacado seleccionado de forma aleatoria y se registra introduciendo su nombre de entrenador.
2. **Catalogo y Filtrado (`/pokemons`):**
   Accede al catálogo de especímenes. Puede realizar búsquedas combinadas mediante un panel de filtro acumulativo (nombre, tipo y peso mínimo).
3. **Detalles (`/pokemons/<id>`):**
   Selecciona un Pokémon para analizar sus características, tipos y barras de estadísticas base. Desde aquí puede presionar **Listo para el combate** para ir directo a la arena.
4. **Preparación del Combate (`/preparar_batalla`):**
   Vía alternativa donde el entrenador puede escribir manualmente el nombre de un Pokémon oponente con validación en servidor.
5. **Estadio de Batalla (`/batalla`):**
   Muestra el enfrentamiento cara a cara (VS) entre el Pokémon seleccionado y un rival aleatorio no repetido, desplegando barras de HP dinámicas, niveles calculados y 4 movimientos de ataque aleatorios.

---

## Vistas y Rutas

| Ruta | Método | Descripción / Lógica asociada |
| :--- | :---: | :--- |
| `/` | `GET`, `POST` | **Portada / Registro:** Formulario `POST` para capturar el nombre del entrenador (validación de 3 a 15 caracteres). Muestra una ficha aleatoria de bienvenida. |
| `/pokemons` | `GET` | **Catálogo y Filtro :** Muestra la cuadrícula de Pokémon filtrada dinámicamente mediante `GET` según 3 criterios: coincidencia de nombre, tipos y peso. |
| `/pokemons/<id>` | `GET` | **Detalles de cada poke:** Vista detallada de un Pokémon con sus imágenes, dimensiones físicas, estadísticas base y acceso directo a la arena de combate. |
| `/preparar_batalla` | `GET`, `POST` | **Selección Manual:** Formulario `POST` que valida la existencia del Pokémon introducido en el catálogo JSON antes de proceder. |
| `/batalla` | `GET` | **Arena de Combate (VS):** Genera la experiencia de combate en formato cara a cara. Selecciona un rival aleatorio distinto al jugador, calcula HP y nivel en tiempo real, y extrae 4 ataques aleatorios con `random.sample()`. |

