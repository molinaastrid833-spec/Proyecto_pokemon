# Pokémon Battle Web

Aplicación web interactiva desarrollada con **Flask**, **Jinja2** y **CSS** para la gestión de Pokémon y simulación visual de combates en tiempo real.

---

## Descripción

**Pokémon Battle Web** es un proyecto enfocado en la construcción de una aplicación web dinámica. Permite a los usuarios registrarse como Entrenadores, explorar y filtrar un catálogo completo de Pokémon, inspeccionar estadísticas detalladas y participar en enfrentamientos en una arena de batalla.

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
   Accede al catálogo de especímenes. Puede realizar búsquedas combinadas mediante un panel de filtro acumulativo (nombre, tipo y peso mínimo). Los filtros aplicados se conservan en la sesión.
3. **Detalles (`/pokemons/<id>`):**
   Selecciona un Pokémon para analizar sus características, tipos y barras de estadísticas base. Desde aquí puede presionar **Listo para el combate** para ir directo a la arena.
4. **Preparación del Combate (`/preparar_batalla`):**
   Vía alternativa donde el entrenador puede escribir manualmente el nombre de un Pokémon oponente con validación en servidor.
5. **Estadio de Batalla (`/batalla`):**
   Muestra el enfrentamiento cara a cara (VS) entre el Pokémon seleccionado y un rival aleatorio no repetido, desplegando barras de HP dinámicas, niveles calculados y 4 movimientos de ataque aleatorios.
6. **Cierre de Sesión (`/logout`)**:
Disponible desde la barra superior de la interfaz mientras exista una sesión activa. Borra los datos almacenados en el servidor/cookie de la sesión y redirige de vuelta a la pantalla de bienvenida.

---

## Vistas y Rutas

| Ruta | Método | Protección | Descripción / Lógica asociada |
| :--- | :---: | :---: |:---|
| `/` | `GET`, `POST` | Pública |**Portada / Registro:** Formulario `POST` para capturar el nombre del entrenador (validación de 3 a 15 caracteres). Muestra una ficha aleatoria de bienvenida. |
|`/logout` | `GET` | Pública |**Cierre de Sesión:** Borra todo el contenido de la sesión mediante session.clear() y redirige al usuario a la portada.|
| `/pokemons` | `GET` | @login |**Catálogo y Filtro :** Muestra la cuadrícula de Pokémon filtrada dinámicamente mediante `GET` según 3 criterios: coincidencia de nombre, tipos y peso. Recupera y guarda los criterios de búsqueda en session["filtros"]. |
| `/pokemons/<id>` | `GET` | @login |**Detalles de cada poke:** Vista detallada de un Pokémon con sus imágenes, dimensiones físicas, estadísticas base y acceso directo a la arena de combate. |
| `/preparar_batalla` | `GET`, `POST` | @login | **Selección Manual:** Formulario `POST` que valida la existencia del Pokémon introducido en el catálogo JSON antes de proceder. |
| `/batalla` | `GET` | @login | **Arena de Combate (VS):** Genera la experiencia de combate en formato cara a cara. Selecciona un rival aleatorio distinto al jugador, calcula HP y nivel en tiempo real, y extrae 4 ataques aleatorios con `random.sample()`. |

## Mantenimiento de Estado con Sesiones
Debido a la naturaleza stateless del protocolo HTTP, el servidor no recuerda las peticiones anteriores del cliente. Para resolver esto y evitar juntar información sensible en la URL (?trainer=...), la aplicación utiliza las sesiones nativas de Flask (flask.session).

### ¿Qué se guarda en la sesión y por qué?



| Dato | Clave en session | Justificación |
| :-- | :--: | :-- | 
| Nombre del Entrenador | ``session["trainer"]`` | **Identificación y Control de Acceso:** Mantiene la identidad del usuario activo durante toda la navegación. Sirve como base para el decorador @login que bloquea el acceso a rutas privadas si no se ha iniciado sesión previa. Elimina la necesidad de pasar el parámetro por URL en cada vista o plantilla.|
| Filtros del Catálogo| ``session["filtros"]`` | **Persistencia de la Experiencia de Usuario (UX):** Almacena los criterios de búsqueda aplicados (nombre, tipo, peso mínimo). Si la entrenadora entra a inspeccionar la ficha detallada de un Pokémon `(/pokemons/<id>)` y regresa al catálogo, los filtros aplicados se mantienen intactos y la lista no se reinicia.|
| Pokémon para la Batalla | ``session["pokemon_batalla"]`` | **Mantenimiento del Contexto de Combate:** Registra el nombre del Pokémon seleccionado para combatir. Permite acceder y recargar la vista del estadio ``(/batalla)`` sin perder la selección realizada en la sala de preparación o desde la ficha de detalles.|


## Medidas de Seguridad Implementadas
- **Firma Criptográfica ``(app.secret_key)``:** Flask convierte la sesión a formato JSON y la firma mediante un secreto antes de enviarla al cliente. Si el usuario modifica el contenido de la cookie en su ordenador, la firma se invalida automáticamente.

- **SESSION_COOKIE_HTTPONLY = True:** Le indica al navegador que la cookie de sesión no debe ser accesible a través de JavaScript, protegiendo a la aplicación ante ataques de tipo XSS (Cross-Site Scripting).

- **SESSION_COOKIE_SAMESITE = 'Lax':** Restringe el envío automático de la cookie desde enlaces de sitios web externos, reduciendo el riesgo de ataques CSRF (Cross-Site Request Forgery).

- **Decorador de Autenticación (@login):** Intercepta las solicitudes a rutas protegidas (/pokemons, /pokemons/<id>, /preparar_batalla, /batalla) e impide el acceso directo escribiendo la URL en el navegador si no existe un entrenador registrado en session["trainer"].