# Guía del usuario de Kaleidohedra

Kaleidohedra, de DICTO, es el tercer hermano de [Rhombiverse](https://rhombiverse.vercel.app) y [Polyhedraverse](https://polyhedraverse.vercel.app). Rhombiverse es el **paisaje**: las redes mismas, extendiéndose en todas direcciones. Polyhedraverse es la **galería de retratos**: las formas que viven en esas redes, una a una, de cerca. Kaleidohedra **mueve el paisaje**: puedes cizallar y deslizar toda la red, y cada pieza se mueve con ella. Se queda con los mundos donde eso tiene sentido: las redes de 3D+, sus propios mundos (Euclid–Kepler–Pacioli Cell Network, Targets, Capas y Romboedros áureos) y los Desarrollos, el camino de los desarrollos planos al 3D. Los mundos de 1D y de 4D a 6D están en Rhombiverse.

Aquí cada pieza llena el espacio a la perfección sobre una red cristalina real, así que solo puedes poner una pieza donde la red tenga sitio para ella. Toca para añadir una pieza, mantén pulsado para quitarla y mira lo que has construido en distintas vistas.

La primera parte de esta guía recorre las tareas habituales. La segunda enumera todos los controles.

Los nombres de los botones aparecen tal como se ven en la aplicación (los que la aplicación aún no traduce siguen en inglés).

## Cizallar la red

Los controles propios de Kaleidohedra están en el panel **⟋ Shear**, arriba a la derecha. Mueven toda la red a la vez: todo lo que has construido se desliza con ella, y la construcción sigue como siempre.

- **↺ Reset to FCC** devuelve todo a la red FCC normal con su dodecaedro rómbico regular, si te pierdes.
- **Towards** elige hacia dónde va la red: **DICTO FCC** (de la red FCC normal a la cizallada de DICTO) o **Bain (BCC → FCC)**.
- **Path** desliza a lo largo de ese camino exacto; los botones de parada (como FCC, halfway y DICTO FCC) saltan a sus puntos con nombre.
- **Cell** cambia la forma de la celda sobre la misma red: 0 es la celda simplemente cizallada, 1 la celda con todas las aristas iguales (en la parada DICTO FCC, el dodecaedro rómbico sesgado de DICTO).
- El medidor **Regularity** puntúa la celda por sus ángulos (1 significa que todos los ángulos son especiales: 36, 45, 60, 70,5, 72 o 90°). En el camino de Bain también cuenta cuántos de sus disfenoides son tetraedros regulares.
- **◀ Find** y **Find ▶** saltan por el camino a la siguiente celda más regular o al siguiente momento en que aparece un hexágono regular. Toca primero una parada.
- **Six sliders** fija directamente las longitudes a, b, c y los ángulos α, β, γ de la red.
- **Export member** guarda el estado actual con el nombre que elijas, como un pequeño archivo JSON (un miembro de la población).

En Euclid–Kepler–Pacioli Cell Network el panel Shear mueve solo la red: los centros de las celdas se deslizan y cada pieza sigue siendo un sólido regular. Se oculta en Targets, donde el cizallamiento cambiaría los ángulos. Los hallazgos de Kaleidohedra, y cómo se comprueba cada uno, están en [DISCOVERIES.md](https://github.com/DICTOR-Master/kaleidohedra/blob/master/DISCOVERIES.md).

## Primeros pasos

### Elige una dimensión

Tras **ENTER** se abre el selector de dimensiones: una forma que gira despacio cuyas caras son **2D+** y **3D+**. Toca **3D+** para construir sobre las redes, o **2D+** para plegar desarrollos planos en sólidos (Desarrollos). Arrastra para girar la forma. Los botones **3D+**, **EKP** y **Targets** de la pantalla de bienvenida te llevan directamente.

Puedes cambiar más tarde desde **Menu → Change Dimension** o desde el **Wizard** (arriba a la izquierda): **3D+** muestra cada red con sus piezas como estructuras de alambre giratorias, junto con los mundos propios de Kaleidohedra, y **2D+** abre los Desarrollos.

### Coloca tu primera pieza

Un mundo vacío muestra un **contorno naranja** donde va la primera pieza. Tócalo. Después toca una cara de cualquier pieza para añadir una vecina al otro lado.

Se construye pieza a pieza. En 3D+ empiezas con el **RD** (dodecaedro rómbico) seleccionado. La pieza que estás colocando aparece en el botón **Shape**, abajo a la izquierda; tócalo para elegir otra.

### Quita una pieza

- **Móvil o tableta:** mantén pulsada la pieza.
- **Ratón:** haz clic derecho sobre la pieza. El clic derecho quita piezas en cualquier modo.

Para deshacer tu último cambio, toca **Undo** (↶, abajo a la derecha). Mantenlo pulsado para retroceder varios pasos a la vez. Cada dimensión tiene su propio historial, así que deshacer en los Desarrollos nunca toca tu construcción de 3D+.

### Mueve la cámara

- **Girar:** arrastra con un dedo, o con el botón izquierdo del ratón.
- **Zoom:** pellizca, o usa la rueda del ratón.
- **Desplazar:** arrastra con dos dedos.

## Qué construir

### Las piezas, por red

**Desarrollos 2D** (Wizard → 2D+): de 2D a 3D. Elige un sólido en el panel: las **celdas de Voronoi**, cubo, RD y TO (octaedro truncado), las celdas que llenan el espacio de las redes cúbicas simple, centrada en las caras y centrada en el cuerpo; su desarrollo aparece como un fantasma tenue. Síguelo: toca para construir la primera cara lado a lado, en celdas 1D, y después cada toque construye la cara siguiente. Cuando el desarrollo está completo, toca y se pliega en el sólido (el indicador muestra **2D+/3D+**); el **deslizador de plegado** lo pliega y despliega a mano, y **Abrir en 3D+** lleva allí el sólido terminado. Mantén pulsado para deshacer una cara (o desplegar). Cada sólido guarda su propio progreso. Los **sólidos platónicos** son un segundo grupo: tetraedro, octaedro, icosaedro, dodecaedro y el cubo. **Abrir en 3D+** aparece para los sólidos que el mundo 3D+ tiene como piezas (cubo, RD, TO, octaedro). **⊘** junto a Undo borra el desarrollo en el que estás.

**Pintar** (3D+): el pincel de la fila inferior, o el interruptor Pintar en el centro de la rueda de colores, cambia el color de las piezas ya colocadas. Actívalo, elige un color y toca una pieza; desactívalo para volver a construir. Cambia los colores a Elegir, para que cada pieza muestre su propio color. (Capas, Romboedros áureos, EKP y Targets colorean sus piezas a su manera, así que Pintar no aparece allí, ni en los Desarrollos.) Cuando el hueco de la fila inferior lo ocupa un selector de unión (Rhombohedra y Pyrochlore), el pincel queda justo encima.

**3D+:**

| Red | Piezas |
|---|---|
| FCC | Rhombic Dodecahedron (RD, dodecaedro rómbico), Hemi RD, Hourglass, RD Quarter, Cube, Pyramid |
| DICTO FCC | DICTO RD: el dodecaedro rómbico sesgado de DICTO con varillas azules de Zometool (seis rombos de 60° y seis de 72°, volumen φ² con arista 1), en un FCC cizallado; DICTO Blocks: sus cuatro bloques, dos bloques de rombos y dos romboedros aplanados, cara con cara |
| RD Dual | Cuboctahedron (CO, cuboctaedro), Octahedron (octaedro) |
| BCC | Truncated Octahedron (TO, octaedro truncado) |
| BCC Interstitial | Flattened Octahedron, Disphenoid |
| Elongated Dodecahedron | Elongated Dodecahedron (ED, dodecaedro alargado) |
| Hexagonal | Hex Prism (prisma hexagonal) |
| Rhombohedral | Rhombohedra (romboedros) |
| Pyrochlore (Kagome 3D) | Truncated Tetrahedron (tetraedro truncado; los tetraedros entre ellos se añaden solos) |

Prueba esto en FCC: coloca seis Pyramid para formar un Cube. Después añade una Pyramid en cada cara del Cube y se convierte en un RD. Quita esas seis de nuevo para volver a un Cube.

**RD Quarter** es uno de los 4 romboedros en los que se divide un RD. Toca un RD cerca de una de sus esquinas para rellenar esa esquina y luego toca una cara de un cuarto para colocar su imagen especular al otro lado de esa cara. La imagen especular siempre cae de nuevo en la red RD, así que puedes hacer crecer los cuartos de celda en celda. Para una red libre de romboedros con Copy (copia) además de Mirror (espejo), usa **Rhombohedra**.

### Colores

Las piezas se colorean según el ajuste **Colores** (en Ajustes): **Cian** (todas cian, por defecto), **Tipo** (cada tipo de pieza con su color, editable en la lista que aparece) o **Elegir** (cada pieza conserva el color con que se colocó). Toca el **botón de color** (abajo a la izquierda) para elegir entre 15 colores: en Cian cambia a Elegir y en Tipo cambia el color del tipo de pieza que colocas. Cambiar de modo nunca pierde los colores con que se colocaron las piezas.

## Observa tu construcción

| Vista | Qué muestra | Cómo activarla |
|---|---|---|
| World View | Color, Translúcido o Esqueleto | Toca el botón World View para alternar |
| Lattice View | Tu construcción y todos los huecos libres un paso más allá, para la pieza elegida | Toca el botón Lattice View (o ⬡ en la rueda de la esquina) para recorrer las piezas |
| X-Ray | Un corte. Arrastra el plano a través de la estructura, también en diagonal | Botón X-Ray (⛶) |
| Spherical | Toca para cambiar: cada pieza como una esfera (los RD enteros tocan a sus doce vecinos), luego los huecos entre RD enteros (octaédricos en oro, tetraédricos en rosa, solo donde están cerrados) con todas las esferas tenues. Un control deslizante da tamaño a todas las esferas (se detiene en el tamaño propio de cada forma; menos = separadas, más = solapadas). Con Lattice View activo, cada hueco libre de la red se ve como una esfera tenue. Solo una vista | Botón Spherical (◯): apagado → esferas → huecos |
| Duality | El teselado aperiódico que proyecta esta estructura cristalina | Botón Duality (◐) |
| Dualize | Intercambia FCC y BCC | Ajustes → Dualize Preview |

Ajustes también tiene una **Vista de sección**: elige un eje, arrastra el deslizador para mover el corte y marca **Invertir** para ver el otro lado.

## Capas

Un mundo 3D para construir **envolventes**: capas de dodecaedros rómbicos (RD), cada capa con su banda de color, contadas desde tu primera pieza. Elígelo en la pantalla 3D+ del Wizard.

- **+ Capa** llena la siguiente capa y **− Capa** quita la más exterior. **Envolvente** elige cómo se cuentan: **Pasos** (un cuboctaedro: 13, 55, 147 … piezas), **Distancia** (hacia una esfera) o una forma objetivo (tetraedro, cubo, octaedro, RD u octaedro truncado). **Recortar** deja la envolvente exactamente plana con esa forma.
- Modo **Fragmentar**: toca una pieza y elige una **División** (mitades, tercios, cuartos, sextos, octavos, doceavos, dieciseisavos, veinticuatroavos o cuarentaiochoavos); **Girar** cambia el corte. En el modo Construir, el menú **Pieza** coloca también partes sueltas.
- **Escala** construye con RD más grandes (×2 a ×4). **Fusionar ×2 / ×3** sobre una pieza elegida muestra el contorno del RD grande, y **Confirmar fusión** lo pone en su lugar; el menú División lo vuelve a abrir.
- **Info** muestra el diagrama de anillos: toca un anillo para ocultar o mostrar esa capa y ver el interior, quita cualquier capa y elige los colores de las bandas.

## Romboedros áureos

Un mundo 3D con las dos piezas del teselado de Penrose en 3D. Elígelo en la pantalla 3D+ del Wizard. Toca el contorno naranja y luego una cara para añadir la pieza **Alargada** o **Achatada** elegida en el menú Pieza. El **Control Penrose** pinta de verde las piezas que pertenecen al verdadero teselado aperiódico y de rojo las que se han desviado; Lattice View muestra el teselado verdadero alrededor, y tocar un fantasma lo coloca.

Los mismos dos bloques son las piezas de **RHOMBITURE** de DICTO, un sistema de armazón extraíble para tallar y modelar: [doi:10.5281/zenodo.23173896](https://doi.org/10.5281/zenodo.23173896).

## Euclid–Kepler–Pacioli Cell Network (EKP)

Un mundo 3D sobre una única celda exacta. Pon los tejados de Euclides sobre un cubo y obtienes un dodecaedro regular; dobla los tejados hacia dentro por las caras del cubo y forman un icosaedro regular. Las aristas del cubo, el dodecaedro y el icosaedro están en razón φ² : φ : 1. Elígelo en la pantalla 3D+ del Asistente. Toca el contorno naranja, elige una **Pieza** (cubo, dodecaedro, icosaedro, gran dodecaedro estrellado, octaedro, stella octangula o rectángulos áureos) y toca un sólido: la pieza va a esa celda si aún no está, si no a la celda siguiente al otro lado de la cara tocada. Los sólidos pequeños quedan dentro de los grandes, así que usa **Rayos X** o la vista translúcida para verlos. **Vista** redibuja la misma construcción: dos sólidos alternando según un **Patrón**, un damero o la superficie exterior fusionada de todos los dodecaedros. **Vértices** marca las esquinas del cubo o todos los vértices, e **Info** muestra el grupo espacial (Pm-3 para la celda; cada patrón tiene el suyo). Al crecer dodecaedros por sus caras solo se alcanzan celdas del mismo color en el patrón diagonal; crece por una cara de cubo para llegar a las demás. **Girar cubos impares** gira cada pieza de cada cubo impar un cuarto de vuelta alrededor del eje vertical, de modo que los cubos vecinos alternan. También gira la superficie exterior fusionada.

Tres de esas piezas completan un homenaje a Kepler: el **octaedro** sobre los centros de las caras del cubo, con los vértices del icosaedro en sus aristas en la sección áurea; la **stella octangula**, dos tetraedros regulares en vértices alternos del cubo que se solapan en ese octaedro; y los tres **rectángulos áureos** entrelazados de Pacioli, que son justo donde se encuentran las cumbreras de los tejados de las celdas vecinas. Juntos, los cinco sólidos platónicos se anidan en una celda: icosaedro, octaedro, tetraedros, cubo, dodecaedro.

La celda de este mundo es la **celda Euclid–Kepler–Pacioli**, y los grandes dodecaedros estrellados e icosaedros que solo se tocan por los vértices forman la **red Euclid–Kepler–Pacioli**, ambas de DICTO. Cítalas como [doi:10.5281/zenodo.23173809](https://doi.org/10.5281/zenodo.23173809).

## Estudios

Un mundo 3D+ de construcciones exactas sobre la celda Euclid–Kepler–Pacioli, una a una (Wizard → 3D+ → Studies). Elige un **Estudio**: **Ventanas** (el dodecaedro con las stellas octangulas de sus seis vecinos de cara talladas, que deja 12 rombos gruesos de Penrose en los propios ángulos de cara del dodecaedro), **Ventanas, con las seis stellas**, **Dodecaedros y sus Dogstars** (los dodecaedros regulares de las celdas pares dejan un hueco en cada celda impar: el Dogstar, una estrella de 8 puntas, estelación parcial de un dodecaedro 1/φ³ de su tamaño, dentro de la stella octangula de la celda; juntos llenan el espacio y **Separar** los aparta), **Ventanas y stellas, en damero** (la stella octangula es la otra mitad de las ventanas: ventanas en las celdas pares y stellas en las impares llenan el espacio exactamente, 12 + 4 = dos cubos; el deslizador **Separar** las aparta para ver cómo encajan), **Ventanas convexas** (cada rombo empujado hacia fuera; el deslizador **Empuje** se detiene en el punto áureo, donde aparecen 6 rombos áureos, 74 caras en total), **De las ventanas al icosidodecaedro** y **De las ventanas al dodecaedro rómbico** (el deslizador **Transformar** lleva los rombos a cada uno; la envolvente se dibuja opaca con los rombos incrustados, y sus contornos se ven a través de ella durante el camino) y **Dodecaedro estirado** (8 pentágonos, 4 hexágonos y 2 rectángulos; el deslizador **Estirar** se detiene a una arista, donde los rectángulos son cuadrados, y en el espaciado de la red). Los estudios también se cizallan: como copias exactas en la red o, con un toque, como el propio sólido.

## Stella–Jewel Lattice

Un mundo 3D+ (Wizard → 3D+ → Stella–Jewel Lattice) de dos piezas que llenan el espacio juntas en damero: el **Dragon Jewel** (DJ, el nombre que DICTO dio al sólido de las ventanas del mundo Studies) en las celdas pares y la **stella octangula** en las impares. Toca el Dragon Jewel cian para colocarlo y luego toca cualquier cara para añadir la pieza del otro lado; mantén pulsado para quitar. **Vista** cambia entre ambas piezas y **solo Dragon Jewels**, que se unen cara a cara por sus 12 rombos y dejan huecos con forma de stella. **Cizalla** funciona como en Studies: copias exactas sobre los centros que se mueven, o todo el empaquetado doblado. **Ejes quíntuples** dibuja los seis ejes quíntuples de cada Dragon Jewel y, en cada cara, los cinco lugares donde podría ir una ventana, con el que elige el cubo resaltado. Lattice View muestra las celdas vacías que puedes llenar.

## Sunstar Lattice

Un mundo 3D+ (Wizard → 3D+ → Sunstar Lattice) con dodecaedros regulares en su empaquetado reticular más denso en las celdas pares y, en cada hueco que dejan en las impares, un **Dogstar**: una estrella de 8 puntas, exactamente una estelación parcial de un dodecaedro 1/φ³ de su tamaño, con aristas solo áureas. Un dodecaedro rodeado de sus Dogstars es un **Sunstar**, el sol con sus parhelios (nombres de DICTO). Toca el dodecaedro cian para colocarlo y luego cualquier cara para añadir la pieza del otro lado; mantén pulsado para quitar. **Vista** muestra ambos, **solo Dogstars** (comparten vértices, cuatro en cada esquina del cubo, como un Kagome 3D; un toque añade el Dogstar más cercano que comparte un punto) o **solo dodecaedros**. **Cizalla** y **Ejes quíntuples** funcionan como en Stella–Jewel Lattice. **Sunstars enteros** añade y quita un dodecaedro junto con los 6 Dogstars de sus caras (un Dogstar que otro Sunstar aún tiene se queda). **Dogstars en cada celda** pone también un Dogstar dentro de cada dodecaedro (cabe entero: Dogstar dentro de la stella, dentro del cubo, dentro del dodecaedro), con los dodecaedros transparentes, así que los Dogstars llenan todas las celdas y ocho puntas se juntan en cada esquina del cubo. **Reacción en cadena estelar** (nombre de DICTO, como la reacción en cadena del Sol) muestra dentro de cada dodecaedro la cadena que encaja exactamente en él, cada paso tocándose: su gran estrella (el gran dodecaedro estrellado del núcleo del Dogstar), dentro un Sunstar entero 1/φ³ de su tamaño, dentro de su dodecaedro la siguiente gran estrella y un Sunstar 1/φ⁶. El Dogstar es la estelación 8 del dodecaedro de George W. Hart (1996), quien señaló que llena el espacio alternado con dodecaedros regulares; también aparece en Polyhedra-World.

## Targets

Una galería 3D de las 160 celdas objetivo: toda celda que llena el espacio con todas las aristas iguales y cuyas aristas solo se encuentran en ángulos especiales (36°, 45°, 60°, 70,53°, 72° y 90°), halladas con una búsqueda exacta hecha de dos maneras (véase [TARGETS.md](https://github.com/DICTOR-Master/kaleidohedra/blob/master/TARGETS.md)). Elígelo en la pantalla 3D+ del Asistente. Escoge un **Tipo** (paralelepípedo, prisma hexagonal, dodecaedro rómbico, dodecaedro alargado u octaedro truncado) y una celda, o recórrelas con ◀ ▶. Cada una se nombra por su tipo, su número en TARGETS.md y sus ángulos; ✓ marca las que ya están en Polyhedraverse. **Mostrar** dibuja la celda sola, con sus vecinas de cara o como un bloque 3×3×3 de su red, para verla llenar el espacio. Las caras se colorean por tipo: cuadrados en azul, rombos en rosa, hexágonos regulares en dorado y otros hexágonos en morado. **Info** muestra sus caras, los ángulos entre las direcciones de sus aristas, su volumen (arista 1), la red con la que tesela y si ya está en Polyhedraverse. Aquí no se construye nada, y el panel Shear se oculta para que los ángulos sigan siendo exactos.

## Guarda tu trabajo

Tu mundo se guarda automáticamente en este navegador, en todas las dimensiones, después de cada cambio. Vuelve a aparecer cuando abres el sitio en el mismo dispositivo y navegador.

En **Ajustes**:

- **Exportar Mundo** guarda todo, cada red y mundo de 3D+ y tus desarrollos, en un archivo. Úsalo como copia de seguridad o para llevar tu mundo a otro dispositivo.
- **Importar Mundo** abre un archivo exportado. **Undo** deshace una importación.
- **Clear World** (⊘ en la rueda de la esquina) empieza de nuevo con un mundo vacío. Undo puede recuperarlo.

## Aprende las matemáticas

- **Almanac:** las matemáticas y la geometría detrás de cada pieza y cada red. Ábrelo desde Menú → Almanac.
- **What's New** muestra los cambios recientes.

---

# Referencia de controles

## Botones en pantalla

| Control | Qué hace |
|---|---|
| Wizard (arriba a la izquierda) | Recorre dimensiones y redes, cada una con sus piezas. La etiqueta naranja grande a su lado muestra la dimensión en la que estás |
| Shape (abajo a la izquierda) | La pieza que colocas. Tócalo para cambiarla |
| Color (abajo a la izquierda) | Color de construcción. Tócalo para cambiarlo |
| Lattice View | Alterna entre Off y una vista para cada pieza |
| Cambio de unión | Solo aparece en piezas que se unen de más de una forma (Rhombohedra: Copiar / Reflejar; Pyrochlore: tetraedro pequeño / entero): toca para cambiar |
| Undo (↶, abajo a la derecha) | Toca para deshacer un paso en la dimensión actual. Mantén pulsado para retroceder más |
| Paint (pincel) | Cambia el color de piezas colocadas: actívalo, elige un color y toca una pieza. Ocupa el lugar del selector de unión en la fila inferior; cuando ese selector hace falta, queda justo encima |
| ⊘ Borrar (junto a Undo, Desarrollos) | Borra el desarrollo en el que estás para empezar de nuevo; Undo lo recupera |
| Menú | Abre la rueda del menú (teclado: Tab o Espacio) |

## Rueda de la esquina

Arrastra la pequeña rueda de la esquina para girarla. Toca una cara para usarla.

| Símbolo | Control |
|---|---|
| ⚙ | Ajustes |
| ⛶ | X-Ray |
| ◐ | Duality |
| ⬡ | Lattice View |
| ◇ | Menú |
| ⊘ | Clear World |
| ↻ | Reload (úsalo si algo parece atascado) |
| ◯ | Spherical (apagado → esferas → huecos) |
| — | World View |

## Rueda del menú

El menú es un dodecaedro rómbico. Cada cara es una sección: toca una cara para abrirla y usa **Home** para volver. **Almanac** está siempre en una cara superior.

| Sección | Contenido |
|---|---|
| Home | Piece, Color, Change Dimension |
| Piece | RD family, Cube, Pyramid, TO, Flattened Octahedron, Disphenoid, CO, Octahedron |
| RD family | RD, Hemi RD, Hourglass, RD Quarter, ED, Hex Prism, Rhombohedra, Pyrochlore |
| Change Dimension | 2D+, 3D+ |

## Ajustes

| Ajuste | Qué hace |
|---|---|
| Sensibilidad de la vista | Velocidad de giro de la cámara |
| Invertir eje Y | Invierte el arrastre vertical |
| Campo de visión | Amplitud del objetivo de la cámara |
| Calidad gráfica | Baja, Media o Alta |
| Mostrar medidor de FPS | Contador de fotogramas por segundo |
| Volumen | Nivel de sonido |
| Idioma | English, 日本語, Español, Français, 한국어, 中文, Русский (también con el selector 🌐 de la parte superior de la pantalla de bienvenida y de esta guía) |
| Colores | Cian, Tipo o Elegir: cómo se colorean las piezas |
| Vista de sección, eje, posición, Invertir | Corte a lo largo de un eje |
| Dualize Preview | Modo de construcción especial |
| Exportar Mundo, Importar Mundo | Hacer copia y restaurar (todas las dimensiones) |

## Teclado y ratón

| Entrada | Acción |
|---|---|
| Clic izquierdo en una cara | Añadir una pieza |
| Clic derecho en una pieza | Quitarla |
| Arrastrar con el botón izquierdo | Girar la cámara |
| Rueda del ratón | Zoom |
| Tab o Espacio | Abrir la rueda del menú |
| Escape | Cerrar el menú, el Wizard o el Almanac |
| Enter | Entrar desde la pantalla de bienvenida |

## Táctil

| Gesto | Acción |
|---|---|
| Tocar una cara | Añadir una pieza |
| Mantener pulsada una pieza | Quitarla |
| Arrastrar con un dedo | Girar la cámara |
| Pellizcar | Zoom |
| Arrastrar con dos dedos | Desplazar |
