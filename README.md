# 🧨 Buscaminas en Python

## 📌 Descripción

Este proyecto consiste en un bot para jugar automáticamente al clásico juego del **Buscaminas**. Existen **dos versiones del programa**:

- Una versión **completa y funcional**, ubicada en el directorio principal, que utiliza la biblioteca **PyAutoGUI**.
- Una versión **incompleta**, ubicada en un subdirectorio, que fue desarrollada inicialmente con **Selenium**.

## 🚀 Motivación y evolución

Comencé desarrollando el bot con Selenium. Conseguí que identificara las minas e hiciera clic en las casillas seguras. Sin embargo, el rendimiento era muy lento, así que busqué alternativas más rápidas. Fue entonces cuando descubrí **PyAutoGUI**, que resultó mucho más eficiente para este caso.

---

## 🧪 Versión con Selenium

Esta versión necesita un **driver de Chrome**. Al ejecutar el programa, se abre una ventana del navegador con un mensaje que indica que está siendo automatizado. Esto puede ser un inconveniente en páginas que bloquean la automatización y es algo para tener en cuenta en proyectos futuros.

### ❌ Limitaciones

- Selenium carga todos los elementos de la página (HTML, CSS...), lo cual lo hace **muy lento**.
- Cada vez que se hace clic en una casilla segura, la página se **recarga parcialmente**, haciendo el proceso más pesado.
- En mis pruebas:
  - El nivel **principiante** se resolvía en unos **7 segundos**.
  - El nivel **intermedio** en aproximadamente **18 segundos**.
  - Esto es **demasiado lento** para un bot eficiente.

### ✅ Ventajas

- Al trabajar directamente con los elementos del **DOM**, Selenium permite una mayor **flexibilidad** en cuanto a resolución de pantalla, posición de los elementos y precisión en la interacción.
- Los elementos del juego son **fáciles de identificar** gracias a sus clases e identificadores bien estructurados.

---

### 🧾 Datos del DOM del Buscaminas

Al inspeccionar el HTML del juego, es posible identificar con facilidad la información relevante de cada casilla. Por ejemplo:

- La **clase (`class`)** indica el **estado de la casilla** (en blanco, descubierta, número de minas cercanas, etc.).
- El **identificador (`id`)** proporciona la **posición** de la casilla en formato `fila_columna`.

#### Ejemplos de casillas:

- **Casilla en blanco**, sin descubrir. Podría contener una mina.  
  (x = 20, y = 8)  
  `<div class="square blank" id="8_20"></div>`

- **Casilla descubierta con el número 2**, lo que indica que hay dos minas alrededor.  
  (x = 16, y = 7)  
  `<div class="square open2" id="7_16"></div>`

---

### 🎮 Estado de la partida

También es posible detectar el **estado del juego** (en curso, ganado o perdido) a través de un elemento del DOM con identificador `"face"` y una clase que cambia dinámicamente:

- Si la clase es `"facesmile"`, significa que la partida **sigue activa**.  
  `<div class="facesmile" style="margin-left:182px; margin-right: 182px;" id="face"></div>`

---

### 📋 Resumen de clases útiles

| Clase              | Significado                             |
|-------------------|------------------------------------------|
| `square blank`     | Casilla no descubierta (posible mina)    |
| `square open0`     | Casilla descubierta, 0 minas alrededor   |
| `square open1`     | Casilla descubierta, 1 mina alrededor    |
| `square open2`     | Casilla descubierta, 2 minas alrededor   |
| `square bombdeath` | Casilla donde explotó una mina           |
| `facesmile`        | Partida en curso                         |
| `facewin`          | Has ganado                               |
| `facedead`         | Has perdido                              |



## 🧪 Versión con PyAutoGUI (versión final)

Esta versión no necesita nada en cambio, actua por screenshots, analizando los pixeles del screenshots y con los pixeles de tu pantalla. Y actua como si fueses tu.

Limitaciones
- Aunque puede buscar imagenes y patrones y con cierta relacion de precision, cuanto más amplio seas mas lento es pero más flexibilidad tienes. Aunque si usa pixeles exacto, significa que si la página se desplaza un pixel ya no funciona.
- Cuanto más preciso menos margen de error.
- Para averiguar que pixel quieres o te interesa tienes que hacer un data mining de las imagenes pixeles, etc.  Para obtener la informacion que quieres.

Ventajas
- Si usas pixeles exactos es superrápido.
- Tienes mucho mas margen de optimización.
- Al hacer clic no necesitas recargar nada.

Conclusion
Aunque pyautogui no permite errores y hay que hacer pruebas manuales para avariguar los pixeles utiles, en este caso buscaba velocidad por lo que era lo

