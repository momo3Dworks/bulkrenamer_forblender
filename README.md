📛 Naming Ruler

Naming Ruler es un addon para Blender que permite renombrar objetos en lote aplicando reglas personalizadas de numeración o letras ascendentes.

Ideal para proyectos arquitectónicos, modelado modular o cualquier escenario donde necesites un esquema de nombres consistente y automatizado.

✨ Características

Renombrar objetos por selección o por colección (incluyendo sub-colecciones).

Prefijo y sufijo personalizados.

Modos de numeración:

🔢 Número fijo (ej: apt_1_south)

📈 Números ascendentes con padding opcional (apt_01_south, apt_02_south…)

🔠 Letras ascendentes (apt_A_A_south, apt_A_B_south…)

Control total:

Define la letra fija (ej: piso A).

Define la letra inicial para el conteo ascendente (ej: empezar desde E en lugar de A).

Evita colisiones de nombres (no sobrescribe objetos existentes).

UI integrada en el Sidebar (N) → pestaña Naming Ruler.

📥 Instalación

Descarga el repositorio como .zip desde GitHub
.

En Blender ve a:

Edit → Preferences → Add-ons → Install...


Selecciona el archivo .zip descargado.

Activa la casilla Naming Ruler.

El panel aparecerá en la Sidebar (atajo N) bajo la pestaña Naming Ruler.

🛠 Uso

Selecciona los objetos que quieras renombrar (Selection Mode) o elige una Collection.

Configura:

Prefix: Texto antes (ej: apt_).

Suffix: Texto después (ej: south).

Numbering Mode:

Fixed → apt_1_south

Ascending → apt_01_south, apt_02_south…

Letters → apt_A_A_south, apt_A_B_south…

Si usas Letters Mode:

Floor Letter = fija (ej: A → piso A).

Start Apartment Letter = desde dónde comienza el conteo (ej: E → empieza en apt_A_E_south).

Haz clic en Apply Rule.

📷 Ejemplos

Entrada:

apt_A, apt_B, apt_C


Configuración:

Prefix: apt_

Numbering: Fixed (1)

Suffix: south

Salida:

apt_1_A_south
apt_1_B_south
apt_1_C_south

📜 Licencia

Este addon está licenciado bajo GPL-3.0.
Consulta el archivo LICENSE
 para más detalles.

🌐 Contribuciones

¡Las contribuciones son bienvenidas!
Si encuentras errores o tienes ideas para mejorar, abre un Issue o un Pull Request en GitHub.