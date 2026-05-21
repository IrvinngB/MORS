# ═══════════════════════════════════════════════════════════════
# GENERAL NARRATIVE TEMPLATES & CONSTANTS
# ═══════════════════════════════════════════════════════════════

# Introducción
INTRO_TEMPLATES = [
    "La niebla del valle se mezcla con el silencio. El K2 aguarda, inmutable.",
    "El viento arrastra los últimos vestigios de la planicie. La montaña te llama.",
    "A tus pies, el mundo se reduce a hielo y voluntad. La cima es una promesa lejana.",
    "El aire es delgado, el silencio, absoluto. Cada respiración es un acto de fe.",
    "La montaña no te ve. No le importas. Y sin embargo, aquí estás.",
    "El glaciar cruje bajo tu peso. Estás solo frente al coloso de roca y hielo.",
    "La luz del amanecer tiñe las crestas de un tono violáceo. Comienza la jornada.",
    "Un frío seco penetra la ropa técnica. Cada paso inicial es para entrar en calor.",
    "La inmensidad vertical te rodea. La civilización queda atrás como un sueño borroso."
]

# Avanzar Normal
ADVANCE_NORMAL = {
    "low": [
        "Avanzas con paso firme. El terreno cede bajo tus botas.",
        "La ascensión continúa. Cada paso es una negociación con la altura.",
        "El crampon muerde el hielo. Un metro más, siempre un metro más.",
        "Tu respiración marca el ritmo. Inhala, pisa, exhala, repite.",
        "Progresas a ritmo constante. El sendero inferior aún es benévolo.",
        "Subes con lentitud pero con técnica. Cada paso firme ahorra valiosa energía.",
        "El piolet se clava en la nieve compacta con un sonido seco.",
        "Ascendés sintiendo el peso de la mochila. El K2 empieza a cobrar su precio.",
        "Pisás con ritmo medido. El piolet marca el compás sobre la nieve firme.",
        "Avanzás por terreno benévolo. Las piernas responden bien al esfuerzo controlado.",
        "Un tramo de nieve compacta deja huellas claras. Buen ritmo de ascenso.",
        "La progresión es fluida. Sentís que podés mantener este paso durante horas.",
    ],
    "mid": [
        "El aire se adelgaza. Cada paso requiere más conciencia que fuerza.",
        "La pendiente no perdona. Avanzas con la precisión de quien sabe que un error cuesta caro.",
        "El viento silba entre las rocas. No te detienes.",
        "Las grietas empiezan a acechar a los lados. La concentración debe ser absoluta.",
        "Un paso tras otro. El K2 impone su ley de paciencia helada.",
        "Tus piernas arden levemente. La altura media empieza a demandar respeto.",
        "El frío se intensifica, pero tu cuerpo mantiene la temperatura con el movimiento constante.",
        "Pisas sobre nieve dura. La tracción es buena, pero la pendiente se agudiza.",
        "La pendiente se endurece. Avanzás midiendo cada apoyo sobre la roca mixta.",
        "Las botas se hunden un poco más en la nieve. El esfuerzo se amplifica.",
        "Un tramo de hielo obliga a ajustar la técnica. Piolet y crampones trabajan en conjunto.",
        "La respiración se acelera. Controlás el paso para no quemar las reservas.",
    ],
    "high": [
        "Cada paso es una batalla contra tu propio cuerpo. La altitud cobra su tributo.",
        "El oxígeno es un recuerdo. Avanzas por inercia y terquedad.",
        "La montaña se siente más cerca, pero tu cuerpo grita que pare.",
        "La cabeza te pulsa rítmicamente por la presión del aire delgado.",
        "Haces una pausa de tres segundos entre cada paso para recuperar el aliento.",
        "Tus botas se sienten de plomo. La fatiga se acumula en las rodillas.",
        "El paisaje es sobrecogedor, pero apenas tenés ojos para mirar dónde pisás.",
        "El viento sopla con fuerza rítmica, intentando retrasar tu progreso.",
        "Avanzás como un autómata. Un pie, piolet, otro pie. La mecánica reemplaza al pensamiento.",
        "El aire entra insuficiente. Solo hay espacio para el siguiente paso en tu mente.",
        "Cada metro ganado es una victoria pírrica. El cuerpo se consume mientras la cima se acerca.",
        "La progresión es un acto de fe ciega. Ponés un pie delante del otro porque no hay alternativa.",
    ],
    "death_zone": [
        "La zona de la muerte no perdona. Cada paso es un acto de rebeldía contra la fisiología.",
        "Tu cuerpo se consume. Avanzas porque detenerte significa morir.",
        "El aire es veneno. Cada respiración quema. Pero la cima está ahí.",
        "Por encima de los 8000 metros, sos un intruso en un mundo que rechaza la vida.",
        "Tus pulmones buscan desesperadamente moléculas de oxígeno en el aire helado.",
        "Te arrastras un metro a la vez. Cada paso adelante requiere toda tu fuerza de voluntad.",
        "El silencio de la altura extrema te envuelve. El mundo de los vivos queda muy abajo.",
        "El tiempo se escurre de prisa aquí. Cada minuto sin cumbre es un riesgo letal.",
        "Cada paso es un universo diminuto de esfuerzo. No hay más allá del pisón siguiente.",
        "Avanzás por terquedad pura. La razón hace rato que abandonó esta ascensión.",
        "El cuerpo se mueve con una lentitud geológica. La cima está ahí, pero el tiempo se agota.",
        "Un paso. Otro paso. La voluntad se ha convertido en mecánica. No hay otra forma de avanzar.",
    ],
}

# Avanzar Agresivo
ADVANCE_AGGRESSIVE = {
    "low": [
        "Te lanzas hacia arriba con determinación. El aire se vuelve más escaso.",
        "La pendiente se acentúa. Tus músculos protestan pero el cuerpo responde.",
        "Aceleras el paso. La montaña parece retroceder ante tu empuje.",
        "Forzás el ritmo en la sección inferior. Querés ganar altitud antes de que empeore el clima.",
        "Un avance rápido y enérgico. Sentís la adrenalina recorrer tus venas.",
        "Empujás tu cuerpo al límite inicial. El terreno lo permite, por ahora.",
        "Pisas con fuerza, devorando metros. Tus crampones muerden el hielo con agresividad.",
        "Ritmo acelerado. La respiración se agita, pero la ganancia de altitud es innegable.",
        "Embistes la pendiente con energía. El terreno cede bajo tu empuje.",
        "Avanzás rápido por la nieve blanda. Las piernas bombean con potencia.",
        "La velocidad es tu cálculo. Querés ganar la mayor altitud antes de que el clima cambie.",
        "Un tramo de roca fácil te permite acelerar. Aprovechás el momento.",
    ],
    "mid": [
        "Forzas el ritmo. El hielo cruje bajo tus pies. Es una apuesta peligrosa.",
        "La adrenalina te empuja hacia arriba. Pero el cuerpo tiene límites.",
        "Cada movimiento es más arriesgado. La fatiga nubla el juicio.",
        "Saltás una pequeña grieta sin dudarlo. La velocidad es tu aliada y tu peligro.",
        "Tu respiración es un jadeo constante. La ambición te obliga a apurar el paso.",
        "Subís a ritmo de ataque. Las pendientes medias requieren un esfuerzo cardíaco brutal.",
        "Ignorás las señales de cansancio de tus piernas y seguís empujando hacia arriba.",
        "Un movimiento rápido para superar una placa de hielo expuesta. Riesgo calculado.",
        "Acelerás sobre la nieve intermedia. Las rodillas protestan pero aguantan.",
        "El ritmo de ataque consume reservas. Sabés que es una apuesta contra el cansancio.",
        "Forzás el paso en una sección mixta. Los crampones chirrían sobre la roca.",
        "Una aceleración arriesgada. El corazón bombea a máxima capacidad en este tramo empinado.",
    ],
    "high": [
        "Te lanzas hacia lo imposible. El cuerpo grita, la mente ordena avanzar.",
        "Es una locura. Lo sabes. Pero detenerte duele más.",
        "La pendiente se vuelve vertical. Cada paso es un acto de fe ciega.",
        "El pecho te estalla por el esfuerzo de avanzar rápido en aire enrarecido.",
        "Superás un tramo empinado con movimientos desesperados. La fatiga es inmensa.",
        "Tus muscles consumen sus últimas reservas de energía en esta embestida.",
        "Te obligás a dar pasos largos y rápidos, ignorando el dolor en las sienes.",
        "Una aceleración arriesgada cerca del hombro del K2. La altura te castiga el doble.",
        "Atacás la pendiente con lo que te queda. No hay ahorro posible, solo velocidad.",
        "Un avance brutal donde cada paso consume el triple de energía. La cima está cerca.",
        "La agresividad tiene un precio en la zona alta. Lo pagarás más tarde.",
        "Subís a golpes de voluntad, tragando aire con desesperación. La cumbre es una obsesión.",
    ],
    "death_zone": [
        "Te arrastras hacia arriba con una furia que no sabías que tenías. La muerte te pisa los talones.",
        "Cada movimiento podría ser el último. Avanzas igual.",
        "La zona de la muerte no distingue entre valientes y necios. Tú eres ambos.",
        "Es un ataque desesperado a la cumbre. O llegás ahora o no lo contarás.",
        "Tus extremidades se sienten entumecidas, pero tu mente ordena avanzar a zancadas.",
        "Corrés una carrera contra el reloj biológico. Cada segundo de esfuerzo agresivo te agota el doble.",
        "Una acometida brutal sobre la última pendiente de hielo azul. Pura locura vertical.",
        "La cima está al alcance del piolet, y empujás tu cuerpo con una violencia suicida.",
        "El último empuje. Cuerpo y mente se rompen simultáneamente mientras avanzás un metro más.",
        "Cada paso agresivo consume minutos de vida. Pero la cima está ahí, intocable y sorda.",
        "Atacás la pendiente con una furia que no tiene nombre. La lógica murió hace horas.",
        "Un zarpazo final al hielo. La progresión es más instinto que técnica a esta altura.",
    ],
}

# Asegurar Ruta — Tiered by altitude
SECURE_ROUTE = {
    "low": [
        "Clavas una estaca en la roca helada. La ruta queda marcada para el retorno.",
        "Asegurás un tramo con soltura. El terreno es firme, las clavijas entran bien.",
        "La cuerda se tensa en un punto sólido. Sentís la seguridad recorrer tus manos.",
        "Instalás un anclaje en la nieve compacta. El piolet entra con un sonido satisfactorio.",
        "Fijás un mosquetón al rápel con facilidad. La progresión está garantizada.",
        "Preparás la cuerda fija en un paso sencillo. Las maniobras de seguridad fluyen natural.",
    ],
    "mid": [
        "Asegurás un tramo. El siguiente paso estará protegido.",
        "La cuerda se tensa contra el viento creciente. Un hilo de seguridad en medio del abismo.",
        "Cada nudo es una promesa: volverás por aquí.",
        "El hielo exige más fuerza para el anclaje. Trabajás con precisión, sin apuro.",
        "Colocás un tornillo de hielo en una sección empinada. La altura exige respeto.",
        "Fijás cuerda en una sección mixta de roca y hielo. La concentración debe ser total.",
    ],
    "high": [
        "El hielo azul no cede fácil. Cada anclaje es una negociación con la montaña.",
        "Trabajás con los mosquetones con dedos entumecidos. La coordinación se complica.",
        "Un anclaje cuestionable en roca descompuesta. Solo el viento no deja que la cuerda flamee.",
        "Fijás el seguro en una laja helada. Dudosamente sólido, pero es lo que hay.",
        "El piolet marca el hielo con más esfuerzo del que recordabas. La fatiga complica la técnica.",
        "Asegurás la cuerda en una cornisa cuestionable. La montaña no ofrece garantías aquí.",
    ],
    "death_zone": [
        "Cada anclaje es una apuesta. A esta altura, el hielo puede mentir.",
        "Tus manos apenas responden. Colocás la estaca por puro instinto de supervivencia.",
        "La cuerda está congelada. Asegurar la ruta toma el triple de tiempo del previsto.",
        "Un anclaje flojo en la zona de muerte. No tenés energía para uno mejor.",
        "Las manos congeladas dificultan cada nudo. La muerte no perdona los errores de técnica.",
        "Clavás la estaca sabiendo que podría arrancarse. Es lo único que tenés.",
    ],
}

# Acampar
CAMP = {
    "clear": [
        "Armas el campamento bajo un cielo despejado. Las estrellas parecen más cercanas aquí.",
        "La tienda resiste el viento. Te permites un respiro mientras la noche pasa.",
        "El cielo estrellado te regala una noche de calma visual. El frío es seco e intenso.",
        "Montás el refugio con relativa facilidad. La montaña te da una tregua hoy.",
        "Bajo una bóveda celeste cristalina, la carpa se convierte en tu pequeño oasis cálido.",
        "El cielo es un diamante negro punteado de luz. Sentís que podrían alcanzarse las estrellas.",
        "La carpa se mantiene firme bajo la bóveda celeste. Una noche casi cálida para los estándares del K2.",
        "Armas la estufa de gas con manos entumecidas pero confiadas. La calma del clima lo permite.",
    ],
    "storm": [
        "La tormenta azota la tienda. Cada ráfaga es un recordatorio de tu fragilidad.",
        "El viento amenaza con arrancar la carpa. Te aferras a la lona como a tu vida.",
        "La nieve se acumula contra la tela. El mundo exterior ha desaparecido.",
        "La ventisca aúlla afuera con furia. Rezas para que las estacas aguanten el embate.",
        "El interior de la carpa tiembla violentamente. La tormenta golpea sin descanso.",
        "La lona azota tus oídos con ruidos ensordecedores. Dormir es imposible en este infierno blanco.",
        "La tormenta araña la lona como si quisiera entrar. Cada ráfaga es un mordisco al refugio.",
        "El viento cambia de dirección sin aviso. La carpa se tensa primero de un lado, luego del otro.",
        "Nieve impulsada a la velocidad de una bala se cuela por la ventilación. No hay rincón seco.",
        "Aferras los tirantes desde adentro, rezando para que la estructura permanezca intacta hasta el alba.",
    ],
    "default": [
        "Armas el campamento entre temblores. El suelo congelado complica todo.",
        "La tienda es tu único refugio contra la inmensidad helada.",
        "Te refugias. El frío se cuela por las costuras, pero estás vivo.",
        "El viento muerde la carpa, pero el refugio te aísla lo suficiente para no congelarte.",
        "Te acurrucás dentro de la tienda, escuchando el crujir constante del hielo exterior.",
        "Montás la carpa a toda prisa con dedos temblorosos. Cualquier refugio es sagrado ahora.",
        "La rutina del campamento se ejecuta mecánicamente. Las horas de oscuridad son largas.",
        "El interior húmedo de la carpa huele a esfuerzo y gasolina. Es el aroma de la supervivencia.",
        "Preparás la bolsa de dormir con dedos que apenas responden. El sueño será breve e inquieto.",
        "La montaña no regala descansos. Pero dentro de la tienda, el viento suena un poco más lejos.",
    ],
}

# Usar Oxígeno — Tiered by altitude
USE_OXYGEN = {
    "low": [
        "Abrís el tanque. El oxígeno fluye y el mundo se vuelve más claro.",
        "Respirás profundamente. La niebla en tu mente se disipa.",
        "El gas silba al salir. Por un momento, recordás cómo se siente respirar sin esfuerzo.",
        "La máscara se empaña. Pero el aire que entra es fresco, casi reconfortante.",
        "Un flujo generoso de oxígeno purifica tus pulmones. Sentís la cabeza despejarse de inmediato.",
        "El regulador entrega el gas con suavidad. Tu respiración encuentra ritmo nuevamente.",
    ],
    "mid": [
        "Un lujo en la montaña. El oxígeno suplementario te devuelve fragmentos de humanidad.",
        "El flujo frío de gas te llena los pulmones. Tu cerebro agradece la carga.",
        "El zumbido del regulador te acompaña mientras el aire puro recupera algo de fuerza.",
        "Inhalás el gas presurizado. Sentís que tu cuerpo recupera compostura térmica y mental.",
        "Las primeras bocanadas de oxígeno alivian la presión en tus sienes. La altitud no perdona.",
        "El suplemento entra como un bálsamo. Sabés que es un parche, no una solución.",
    ],
    "high": [
        "Cada respiración con oxígeno es gas precioso que no se recupera. Pero lo necesitás.",
        "La máscara entrega el aire que la montaña niega. Sentís cómo tu mente se recompone.",
        "El tanque marca menos de lo que quisieras. Pero sin esto, no avanzás.",
        "El regulador ronronea. Es la diferencia entre funcionar y apagarse.",
        "El oxígeno entra a torrente. Tus ojos se despejan y las manos dejan de temblar.",
        "Cada litro de gas vale oro aquí arriba. Ajustás el flujo al mínimo necesario.",
    ],
    "death_zone": [
        "Abrís la válvula con manos que no sentís. El gas es la única razón para seguir.",
        "Jadeás dentro de la máscara. El oxígeno tarda en llegar, pero cuando lo hace, es vida.",
        "El tanque casi vacío. Cada respiración cuesta. Cada segundo con oxígeno es robado a la muerte.",
        "El aire suplementario entra como agua en el desierto. Tu cuerpo lo absorbe con desesperación.",
        "El regulador entrega las últimas moléculas. Sin esto, la inconsciencia llega en minutos.",
        "Bebés el gas como si fuera la última gota de agua del mundo. Quizás lo sea.",
    ],
}

# Comer — Tiered by altitude
EAT = {
    "low": [
        "Una ración tibia. El cuerpo agradece el gesto.",
        "Comés lo mínimo. La supervivencia no permite excesos.",
        "El alimento sabe a algo aquí. Tu cuerpo lo absorbe con gratitud.",
        "Masticás despacio. Cada caloría cuenta, pero al menos el sabor no ha desaparecido.",
        "La comida es un ritual. Un momento de normalidad en medio del esfuerzo.",
        "Ingerís la porción con algo de placer. El estómago recibe el combustible con un rugido satisfecho.",
    ],
    "mid": [
        "El alimento sabe a nada, pero tu cuerpo lo absorbe como un milagro.",
        "Masticás sin entusiasmo. Las calorías son combustible, no placer.",
        "Ingerís alimentos deshidratados. Sabor a metal y supervivencia, pero necesario.",
        "Te obligás a tragar la ración congelada. Tu cuerpo necesita combustible de inmediato.",
        "Cada bocado requiere más masticación de la que recordabas. La altitud entumece hasta el gusto.",
        "La barra energética tiene la consistencia del cartón. La tragás con agua de deshielo.",
    ],
    "high": [
        "La comida se congela antes de llegar a tu boca. La masticás como podés.",
        "El estómago protesta el alimento. Lo obligás a aceptar la ración que sabe a cartón helado.",
        "Tragás algo que solía ser chocolate. A esta altura, todo sabe a nada.",
        "Los músculos necesitan glucosa. Dás vuelta la envoltura con dedos rígidos y mordés lo que podés.",
        "La náusea compite con el hambre. Termina ganando la segunda con pura determinación.",
        "Cada caloría es una batalla contra el estómago cerrado por la altitud. Tragás y seguís.",
    ],
    "death_zone": [
        "El cuerpo apenas digiere. Comés por obligación, no por necesidad que puedas sentir.",
        "La comida se congela en tu mano antes de llegar a la boca. La tragás entera.",
        "El estómago se niega. Forzás la ración hacia abajo como si fuera medicamento.",
        "No sentís hambre. No sentís sabor. Simplemente introducís combustible en una máquina que se apaga.",
        "Cada bocado es un ejercicio de voluntad. Tu organismo rechaza todo alimento a esta altitud.",
        "La barra energética está congelada sólida. La chupetás hasta ablandarla lo suficiente para tragar.",
    ],
}

# Descender — Tiered by altitude
DESCEND = {
    "low": [
        "Desciendes. La presión en tu pecho disminuye con cada metro.",
        "Bajás el ritmo. El valle te recibe con algo de calor residual.",
        "Cada paso hacia abajo es una rendición, pero también una salvación.",
        "La montaña te suelta, metro a metro. El aire se vuelve más amable.",
        "Retrocedés. No es derrota, es estrategia. La montaña estará ahí mañana.",
        "Perdés altitud con decisión. El cuerpo agradece cada metro de descenso.",
    ],
    "mid": [
        "Vas perdiendo altitud. Sentís que recuperás el aliento con cada tramo de bajada.",
        "El descenso requiere rodillas firmes. La gravedad ayuda, pero el cansancio acecha.",
        "Bajás con cuidado por las cuerdas fijas. Dejar atrás la altura extrema alivia tu mente.",
        "Cada metro hacia abajo devuelve algo de lucidez. Los pulmones se expanden un poco más.",
        "Descendés para recuperar. La montaña no va a desaparecer por esperar un día más.",
        "La bajada castiga las rodillas, pero el aire más espeso es un bálsamo inmediato.",
    ],
    "high": [
        "El descenso es urgencia pura. Necesitás bajar, ahora.",
        "Cada metro de bajada es un respiro robado a la altura. No dudás en ceder terreno.",
        "Bajás con movimientos torpes pero veloces. La fatiga convierte el descenso en una ordalía.",
        "Tus rodillas protestan con cada paso hacia abajo, pero la necesidad de aire las impulsa.",
        "Descendés como podés. El cuerpo pide bajar cueste lo que cueste.",
        "El descenso obligado te devuelve algo de oxígeno. Pero la fatiga acumulada es enorme.",
    ],
    "death_zone": [
        "Bajás porque no hay otra opción. Cada metro de descenso es un metro de vida.",
        "El descenso es la única opción racional. La zona de muerte exige evacuación inmediata.",
        "Tus piernas apenas responden, pero la gravedad te ayuda a bajar. Cada metro cuenta.",
        "Descendés con la desesperación de quien sabe que quedarse es morir.",
        "El aire se vuelve un poco menos hostil con cada paso hacia abajo. Seguís bajando.",
        "Abandonás altitud como si tu vida dependiera de ello. Porque depende.",
    ],
}

# Descansar — Tiered by altitude
REST = {
    "low": [
        "Te detenés. Solo un momento, pero el cuerpo lo necesitaba.",
        "Esperás. La inmovilidad pesa, pero el descanso es necesario.",
        "Te sentás sobre la mochila. El viento te recuerda que no podés quedarte mucho tiempo.",
        "Cerrás los ojos un instante. El frío te devuelve a la realidad.",
        "Un respiro. La montaña no espera, pero tu cuerpo sí lo necesita.",
        "La pausa te permite mirar el paisaje. Las cumbres lejanas se recortan contra el cielo.",
    ],
    "mid": [
        "Apoyás la frente sobre el piolet. El pecho sube y baja al ritmo de tu cansancio.",
        "Detenerse a recuperar el pulso. Sentís los latidos retumbar en tus oídos.",
        "Cinco minutos de inmovilidad absoluta. La fatiga retrocede un milímetro.",
        "El descanso es breve pero necesario. La altitud castiga hasta la quietud.",
        "Te apoyás en el piolet, midiendo la respiración. Cada ciclo de aire es oro.",
        "La pausa te permite reevaluar. Controlás pulso, hidratación y determinación.",
    ],
    "high": [
        "Te detenés porque tus piernas se niegan a dar un paso más. El reposo es rendición parcial.",
        "La quietud es engañosa. El frío avanza apenas te detenés. El descanso tiene costo.",
        "Te sentás en la nieve con la espalda contra una roca. El cuerpo agradece, pero el reloj corre.",
        "Descansar a esta altura es un acto de fe. Tenés que volver a moverte antes de que el frío gane.",
        "Tus párpados pesan como piedras. El descanso es una trampa disfrazada de alivio.",
        "La inmovilidad permite que el frío penetre hasta los huesos. No podés quedarte aquí mucho.",
    ],
    "death_zone": [
        "No existe el descanso aquí. Solo pausas en las que te apagás un poco más lento.",
        "Te detenés y el frío te golpea de inmediato. No hay recuperación posible en la zona de muerte.",
        "Sentarte a descansar a 8000 metros es una apuesta. Muchos se sentaron y nunca se levantaron.",
        "La hipoxia te arrulla. Descansar es ceder terreno a la inconsciencia.",
        "Tus piernas ceden. Te apoyás en el piolet sabiendo que levantarte costará lo que no tenés.",
        "El descanso es una mentira a esta altitud. Tu cuerpo se consume igual, solo más lento.",
    ],
}

# Free Heal (Medico) — Tiered by altitude
FREE_HEAL = {
    "low": [
        "Te aplicás un vendaje de emergencia. Las manos tiemblan, pero la técnica es precisa.",
        "Inyectas lo que queda de analgésico. El dolor retrocede, no desaparece.",
        "Primeros auxilios de fortuna. Funciona lo suficiente para seguir.",
        "Tu entrenamiento médico vale más que cualquier equipo aquí arriba.",
        "Limpiás una herida menor con alcohol antiséptico. El ardor te despierta los sentidos.",
        "Tratás los síntomas de congelamiento incipiente con profesionalidad. Las manos responden bien.",
    ],
    "mid": [
        "Administrás medicación básica para la altura. Prevención activa frente al colapso corporal.",
        "Con sutura de emergencia y esparadrapo, te remendás para aguantar unas horas más.",
        "Vendás una zona expuesta con cuidado. El frío no perdona la piel descubierta.",
        "Aplicás un apósito protector. A esta altura, cualquier herida se complica rápido.",
        "Revisás los signos vitales. La presión está alta, pero dentro de lo esperable.",
        "Un torniquete improvisado detiene lo urgente. Lo definitivo queda para el campo base.",
    ],
    "high": [
        "Tus dedos apenas responden. Vendarte es una operación que requiere diez minutos en lugar de dos.",
        "La medicación entra con dificultad. Las jeringas se congelan antes de usar.",
        "Un vendaje apretado sobre la herida. Sin sensibilidad en los dedos, confiás en el tacto memorizado.",
        "Tratás una ampolla que ya no sentís, pero sabés que está ahí por la rojez visible.",
        "La hipoxia complica todo procedimiento. Te costó tres intentos abrir el botiquín.",
        "Aplicás hielo en el lugar equivocado por el temblor. Corregís y seguís.",
    ],
    "death_zone": [
        "Las manos no responden. Te curás más con voluntad que con técnica.",
        "La medicación hace efecto mínimo a esta altitud. La fisiología alterada absorbe poco.",
        "Un vendaje flojo porque tus dedos no pueden hacer fuerza. Es todo lo que podés ofrecer.",
        "Te aplicás tratamiento con manos que no sentís. La destreza es un recuerdo de abajo.",
        "Cada procedimiento médico toma el triple de tiempo. El frío y la hipoxia complican todo.",
        "A 8000 metros, la medicina es un deseo, no una solución. Hacés lo que podés con lo que tenés.",
    ],
}

# Conmutar Oxígeno — Tiered by altitude
TOGGLE_OXYGEN = {
    "low": [
        "Manipulás la válvula del regulador de oxígeno con facilidad.",
        "Ajustás el flujo de oxígeno suplementario en tu máscara como una rutina más.",
        "Girás la perilla del tanque de oxígeno en tu mochila con movimientos naturales.",
        "Revisás y cambiás el estado de la válvula de tu regulador sin inconvenientes.",
        "El clic del regulador confirma que cambiaste el régimen de flujo del tanque.",
        "Ajustás el caudalímetro con guantes gruesos. Operación simple a esta altura.",
    ],
    "mid": [
        "Girás la perilla de paso. El silbido del gas cambia de tono en tu espalda.",
        "Manipulación táctil del tanque. El flujo suplementario se adapta a tu decisión.",
        "Cambiás el régimen de oxígeno deliberadamente. Cada litro cuenta a partir de ahora.",
        "Ajustás el regulador evaluando la respiración. La altitud exige gestión consciente del gas.",
        "La válvula obedece tus manos enguantadas. El zumbido del flujo marca el nuevo ritmo.",
        "Modificás el caudal de oxígeno. La diferencia en la respiración es inmediata pero sutil.",
    ],
    "high": [
        "Ajustás el regulador con manos temblorosas. La precisión importa más que nunca.",
        "La válvula cuesta girar. El hielo la obstaculiza y tus dedos no ayudan.",
        "Cambiás el flujo de oxígeno sabiendo que un error puede costarte la lucidez.",
        "El regulador está semi-congelado. Lo manipulás con cuidado, rezando para que responda.",
        "Tus manos entumecidas forcejean con la perilla. El oxígeno es vida aquí arriba.",
        "Ajustás el caudal al mínimo viable. Cada litro que ahorrás es un litro ganado.",
    ],
    "death_zone": [
        "La válvula está congelada. La golpeás con el piolet hasta que cede.",
        "Tus manos no responden. Manipulás el regulador con los puños, casi a ciegas.",
        "El oxígeno es la línea entre la conciencia y el abismo. Girás la perilla como si tu vida dependiera de ello.",
        "El tanque responde apenas. Ajustás el flujo con lo poco que te queda de destreza.",
        "La máscara se empaña hasta la opacidad. Cambiás el régimen sin ver lo que hacés.",
        "Cada giro de la válvula es una negociación con la muerte. El gas que entra son minutos que ganás.",
    ],
}

# Willpower Despair — Tiered by altitude (3 tiers: low < 6000m, mid 6000-7999m, high >= 8000m)
LOW_WILLPOWER_DESPAIR = {
    "low": [
        "La mente vagabundea. El suelo parece más cercano de lo que debería.",
        "La voluntad se erosiona. Cada paso es una duda.",
        "Pensás en rendirte. No es un pensamiento nuevo, pero hoy pesa más.",
        "Las sombras se alargan. No sabés si es el cansancio o algo más.",
        "Tu reflejo en el hielo te devuelve una mirada que no reconoces.",
        "El silencio te habla. Dice cosas que no querés escuchar.",
    ],
    "mid": [
        "¿Qué sentido tiene todo esto? El vacío de la montaña se traslada a tu interior.",
        "La nieve parece un lecho cómodo para acostarse y no despertar.",
        "Tu nombre carece de significado aquí arriba. Sos solo un cuerpo que se apaga.",
        "La voluntad está rota. Te movés por pura inercia biológica, sin rumbo mental.",
        "La altitud aplasta tus pensamientos. Solo existe el siguiente paso, y ni siquiera estás seguro de querer darlo.",
        "El hielo te llama. La montaña te ofrece silencio eterno.",
    ],
    "high": [
        "La muerte es una compañera tangible aquí. La sentís respirar junto a vos.",
        "Tu mente se fragmenta. Los pensamientos se deshacen como cristal bajo una bota.",
        "Ya no hay voluntad. Solo un cuerpo que se niega a detenerse por pura terquedad celular.",
        "La hipoxia disuelve tu identidad. No sabés quién sos ni por qué estás aquí.",
        "El vacío no está afuera. Está adentro, y crece con cada respiración insuficiente.",
        "Cerrás los ojos y la montaña te susurra: quedate. Mirás las nubes y pensás en descansar para siempre.",
    ],
}

# Willpower Doubt — Tiered by altitude (3 tiers: low < 6000m, mid 6000-7999m, high >= 8000m)
LOW_WILLPOWER_DOUBT = {
    "low": [
        "¿Por qué estoy aquí? La pregunta no tiene respuesta, solo eco.",
        "La cima ya no parece una meta. Parece una excusa.",
        "Mirás hacia arriba y no sabés si es ambición o estupidez.",
        "El cuerpo sigue, pero la mente empieza a negociar.",
        "Recordás por qué viniste. El recuerdo se siente de otra persona.",
        "Cada paso es una pregunta sin respuesta.",
    ],
    "mid": [
        "La cumbre prometida no vale el dolor de cada respiración.",
        "Te cuestionás cada sacrificio que te trajo a esta pared de hielo.",
        "Pensás en los que se quedaron abajo. En el calor. En la vida normal.",
        "La montaña te parece un monumento a la soberbia humana hoy.",
        "Dudás de cada decisión. El camino arriba se ve insensato desde esta perspectiva.",
        "La fatiga mental iguala a la física. Ya no distinguís cansancio del cuerpo del del alma.",
    ],
    "high": [
        "La duda se convierte en certeza: esto es un error. Pero no podés dar marcha atrás.",
        "La hipoxia te pregunta si todo valió la pena. No tenés respuesta.",
        "Cada paso arriba es una pregunta que la montaña no contesta. Solo espera.",
        "Tu voluntad es una correa desgastada a punto de romperse. Cada metro la tensa más.",
        "La cumbre ya no importa. Lo único que querés es que termine, de una forma u otra.",
        "Dudás de todo: de la ruta, del equipo, de tu cordura. A 8000 metros la certeza no existe.",
    ],
}

# Zona de la muerte
DEATH_ZONE = [
    "La zona de la muerte no perdona. El cuerpo consume sus propias reservas.",
    "Pasas los 8000 metros. El oxígeno es un lujo y el tiempo se agota.",
    "Cada célula de tu cuerpo grita que bajes. Pero la cima está tan cerca.",
    "El aire es tan delgado que respirar duele. Sigues adelante.",
    "La montaña te ha absorbido. Ya no eres un escalador, eres parte del hielo.",
    "Los cuerpos de otros escaladores marcan el camino. Ninguno llegó a la cima.",
    "A 8000 metros la muerte es pasiva. Si te quedás quieto demasiado tiempo, te apagas.",
    "La hipoxia va apagando tu raciocinio. Sentís una somnolencia peligrosa y dulce.",
    "Cada minuto en la zona de la muerte erosiona tus órganos internos. El reloj corre.",
    "El viento silba con una frecuencia que parece llamarte al descanso eterno.",
    "El aire no es aire. Es una mentira delgada que apenas engaña a tus pulmones.",
    "Pisás el reino de la muerte. Cada metro por encima de los 8000 es territorio prestado.",
    "Tus piernas responden con un retraso de segundos. La hipoxia convierte los reflejos en eco.",
    "La zona de la muerte te absorbe. El tiempo se distorsiona y el frío borra la frontera entre vivo y muerto.",
    "Cada respiración aquí es un contrato roto con la biología. No deberías estar consciente.",
    "Caminás sobre los restos de otros que creyeron que podían hacerlo. La montaña no distingue.",
]

# Tormenta
STORM = [
    "La tormenta te envuelve. Visibilidad cero.",
    "El viento aúlla. La nieve golpea tu rostro sin piedad.",
    "No ves nada más allá de tu nariz. El mundo se reduce a blanco y dolor.",
    "La tormenta no distingue entre preparados y desprevenidos. Todos sufren igual.",
    "El frío penetra hasta los huesos. La tormenta no tiene piedad.",
    "La ventisca te desorienta. Perdés la noción de dónde está la pendiente.",
    "El viento sopla a más de cien kilómetros por hora, amenazando con arrancarte de la pared.",
    "La nieve acumulada te llega a las rodillas. Cada paso requiere levantar las piernas con un esfuerzo titánico.",
    "Los cristales de hielo te golpean la cara con la fuerza de perdigones.",
    "La tormenta ruge como una bestia herida. No hay dirección posible en este caos.",
    "El viento te empuja hacia un lado y luego hacia el otro. No podés anticipar la siguiente ráfaga.",
    "La nieve acumulada te inmoviliza las piernas. Cada paso es una excavación antes de un avance.",
    "La temperatura cae en picada. Sentís el frío filtrándose por donde no creías que existían costuras.",
    "Una ráfaga te hace perder el equilibrio. Te aferrás al piolet con la desesperación de quien no quiere caer.",
]

# Sufijos Contextuales
SUFFIXES = {
    "general": [
        "El K2 no perdona.",
        "La montaña exige.",
        "Cada turno cuenta.",
        "El tiempo corre contra ti.",
        "La cima es una promesa, no una garantía.",
        "La gravedad es tu constante enemiga aquí.",
        "La montaña dicta las reglas; vos solo intentás sobrevivir.",
        "El silencio de la altura es absoluto e indiferente."
    ],
    "desperation": [
        "¿Cuánto más puedes aguantar?",
        "El cuerpo tiene límites. La mente, también.",
        "Cada paso podría ser el último.",
        "La montaña no te extrañará si te quedas aquí.",
        "La muerte acecha en cada centímetro de hielo azul.",
        "Tu energía se drena como agua entre los dedos.",
        "Apenas sentís las manos. El frío está ganando la batalla.",
        "Te preguntás cuánto tempo pasará antes de que te conviertas en otra marca del camino."
    ],
    "hope": [
        "La cima está más cerca de lo que parece.",
        "Un paso más. Siempre un paso más.",
        "El sol sale para todos, incluso aquí arriba.",
        "La montaña te prueba, pero no te ha vencido.",
        "Sentís una extraña paz en medio del esfuerzo.",
        "El K2 parece darte permiso para seguir subiendo.",
        "Tu cuerpo responde con la memoria del entrenamiento.",
        "La determinación le gana al cansancio por este turno."
    ],
}

# Epitafios
EPITAPHS = {
    "DEAD_EXHAUSTION": [
        "Tu cuerpo se rindió antes que tu voluntad. La montaña respetó tu esfuerzo.",
        "El agotamiento te alcanzó. No fue falta de coraje, fue falta de aire.",
        "Caminaste hasta que tus piernas dejaron de obedecer. La montaña recuerda tu nombre.",
        "Tus últimas calorías se gastaron en un paso más que nunca llegó. La montaña no necesita razón.",
        "El agotamiento fue un peso que no pudiste soltar. Te acostaste en la nieve y la nieve te recibió.",
        "Tu cuerpo dijo basta. Tu espíritu ya había dicho basta horas antes. Solo la terquedad te mantuvo en pie.",
    ],
    "DEAD_COLD": [
        "El frío te reclamó. Tu cuerpo se convirtió en parte del glaciar.",
        "La hipotermia fue silenciosa. Te dormiste en la nieve y no despertaste.",
        "El hielo te abrazó. Ahora eres parte eterna de la montaña.",
        "El frío no fue violento. Fue una promesa de silencio que tu cuerpo aceptó sin protestar.",
        "Te quedaste sin calor como se gasta una vela. La última llama se apagó en la oscuridad del K2.",
        "La hipotermia te entregó al sueño blanco. Tus últimos pasos fueron los de alguien que ya soñaba.",
    ],
    "DEAD_FALL": [
        "La gravedad fue más rápida que tu reflejo. El abismo te recibió sin preguntas.",
        "Un paso en falso. Eso fue todo. La montaña no perdona distracciones.",
        "Caíste. El eco de tu grito se perdió en el viento.",
        "El vacío te recibió en silencio. La gravedad fue la última ley que tu cuerpo obedeció.",
        "Un instante de duda, un pie que no encontró sostén. El abismo no da segundas oportunidades.",
        "Caíste como cae la nieve de una cornisa: sin ruido, sin aviso, sin retorno.",
    ],
    "DEAD_STORM": [
        "La tormenta fue más fuerte que tu voluntad. El viento te arrancó de la montaña.",
        "No viste venir la ráfaga. La montaña te devolvió al valle en un instante.",
        "La ventisca te tragó. Ni tus huellas quedaron.",
        "La tormenta te devoró. El K2 reclamó lo que siempre fue suyo.",
        "El viento te arrancó del hielo como una hoja seca. En segundos, la montaña te hizo invisible.",
        "La nevada cubrió tu último refugio. La tormenta fue el verdugo y la tumba.",
    ],
    "DEAD_EDEMA": [
        "Tus pulmones se llenaron de líquido. La altitud te traicionó desde dentro.",
        "El edema pulmonar fue implacable. Cada respiración era un suplicio.",
        "Tu cuerpo no pudo con la altura. El aire se volvió tu enemigo.",
        "Tus pulmones se ahogaron en el aire más delgado del mundo. La ironía fue tu último pensamiento.",
        "El edema te inundó desde adentro. Cada respiración fue un grito ahogado en silencio.",
        "El líquido llenó lo que el aire abandonó. Moriste ahogado a 8000 metros, rodeado de vacío.",
    ],
    "default": [
        "La montaña te reclamó. Tu nombre se pierde en el viento.",
        "Ma mardina (म मर्दिन) — No moriré en esta montaña.",
        "El K2 me ha reclamado, pero no me ha vencido.",
        "La montaña te reclamó en silencio. Solo el viento recuerda tu nombre.",
        "El K2 no fue personal. La montaña simplemente siguió siendo lo que siempre fue.",
        "Tu historia se une a las muchas que el hielo del K2 guarda sin contar.",
    ],
}

# Citas de Alpinismo
MOUNTAINEERING_QUOTES = [
    '"Las grandes montañas no son justas o injustas, simplemente son peligrosas." — Reinhold Messner',
    '"La aventura es vivir y no perder la vida; el arte del alpinismo es no morir." — Reinhold Messner',
    '"El mundo vertical no termina nunca. Dura. Espera." — Jerzy Kukuczka',
    '"Tuve la sensación de que, al entrar en ese mundo helado, cruzaba una frontera más allá de la cual no pertenecía al mundo humano." — Jerzy Kukuczka',
    '"La montaña no es como los humanos. La montaña es sincera." — Walter Bonatti',
    '"No me ha quedado el horror de caer, sino la alegría de volar." — Walter Bonatti',
    '"Voy a la montaña solo. Si no regreso, solo me pierdo yo." — Buntaro Kato',
    '"Las montañas no son estadios donde satisfago mi ambición, son las catedrales donde practico mi religión." — Anatoli Boukreev',
    '"El alpinista es un hombre que conduce su cuerpo allá donde un día sus ojos lo soñaron." — Gaston Rébuffat',
    '"Llegar a la cima es opcional, regresar al campo base es obligatorio." — Ed Viesturs',
    '"Porque está ahí." — George Mallory',
    '"No es la montaña lo que conquistamos, sino a nosotros mismos." — Edmund Hillary',
    '"A la montaña hay que llevar el miedo, para que nos mantenga vivos." — Ueli Steck',
    '"No busco la muerte, pero no me importa morir en las montañas." — Wanda Rutkiewicz',
    '"El alpinismo es un juego en el que el castigo por cometer un error es la muerte." — Mark Twight',
    '"El precio de la vida es la vida misma." — Reinhold Messner',
]

# Palabras Nepaleses
NEPALI_PHRASES = [
    "Ma mardina (म मर्दिन) — No moriré.",
    "Bistarai bistarai (बिस्तारै बिस्तारै) — Despacio, despacio.",
    "Eklai (एक्लै) — Solo. En soledad.",
    "Paila (पाइला) — Un solo paso.",
    "Sahasa (साहस) — Coraje. Voluntad pura.",
    "Agadi badha (अगाडि बढ) — Avanza hacia adelante.",
    "Man mardaina (मन मर्दैन) — La mente no muere.",
    "Shunyata (शून्यता) — El vacío absoluto. Silencio de la cumbre.",
    "Himalaya (हिमालय) — La morada de la nieve.",
    "Gari-gara (गरि-गर) — Último esfuerzo.",
    "Mero antim sasa (मेरो अन्तिम श्वास) — Mi último respiro.",
    "Dherai mathi (धेरै maथि) — Demasiado alto.",
]

# Continuidad tras evento
POST_EVENT_OVERRIDES = {
    "DISTANT_AVALANCHE": [
        "Aún con el rugido de la avalancha resonando en tus oídos, intentás concentrarte.",
        "El trueno de nieve del turno anterior te dejó alerta. Mirás hacia arriba constantemente.",
        "Con el polvo de la avalancha lejana todavía asentándose, continuás.",
        "El eco del deslizamiento no se apaga. Mirás las laderas con desconfianza renovada.",
        "La montaña te recordó su poder. Cada sombra de nube ahora parece una avalancha potencial.",
    ],
    "HALLUCINATION": [
        "Las sombras que viste antes parecen retirarse, pero sabés que siguen ahí.",
        "Sacudís la cabeza para espantar los ecos de las voces que creíste oír.",
        "La mente aún lucha por distinguir el hielo real de las visiones de la hipoxia.",
        "Parpadeás con fuerza. Lo que viste no estaba ahí, pero tus ojos no están seguros.",
        "El cerebro juega trucos a esta altura. Costó separar lo real de la alucinación.",
    ],
    "WIND_GUST": [
        "Recuperando la compostura tras el empuje del viento, volvés a erguirte.",
        "Con el cuerpo tenso tras la última ráfaga violenta, reanudás el movimiento.",
        "Aún sintiendo el impacto del viento en el pecho, te aferrás al hielo.",
        "El aire alrededor sigue turbulento. La ráfaga dejó tus oídos zumbando.",
        "Te reincorporás lentamente. El viento recuerda que no sos más que un obstáculo en su camino.",
    ],
    "O2_REGULATOR_FAIL": [
        "Buscando desesperadamente recuperar el ritmo respiratorio tras el fallo del regulador...",
        "Aún mareado por el súbito corte de oxígeno, intentás reaccionar.",
        "El regulador emitió un silbido extraño antes de fallar. Ahora respirás con precaución.",
        "La falta de oxígeno te dejó un vacío en el pecho. Restablecés el flujo con manos temblorosas.",
        "El fallo del regulador fue un aviso. Revisás las conexiones dos veces antes de seguir.",
    ],
    "FROSTBITE": [
        "El dolor sordo y helado en tus extremidades congeladas te acompaña en cada movimiento.",
        "Con los dedos rígidos por el principio de congelamiento, cada manipulación es un calvario.",
        "El recuerdo del frío mordiendo tu carne te empuja a no detenerte.",
        "La piel ennegrecida en las puntas de los dedos te recuerda que el reloj avanza.",
        "Cada movimiento de las manos envía punzadas de dolor. La congelación no es una advertencia, es una sentencia.",
    ],
    "PULMONARY_EDEMA": [
        "Cada respiración sigue siendo un gorgoteo húmedo y doloroso. El edema no da tregua.",
        "El pecho te arde. Sabés que tus pulmones están al límite, pero seguís.",
        "El líquido en los pulmones complica cada inhalación. Tosís algo que no querés mirar.",
        "La presión en el pecho no cede. Respirás con la dificultad de quien tiene agua en el cofre.",
        "Los estertores del edema acompañan cada paso. Tu cuerpo es un fuelle roto que se niega a apagarse.",
    ],
    "TENT_COLLAPSE": [
        "Sin el refugio seguro de la carpa tras su colapso, el K2 se siente infinitamente más hostil.",
        "Aún con la nieve de la carpa derretida pegada al cuerpo, seguís expuesto.",
        "Recogés los restos del refugio destruido. Sin paredes, el frío entra sin pedir permiso.",
        "La carpa yace como un animal muerto sobre la nieve. Estás completamente a la intemperie.",
        "Improvisás lo que podés con los restos rotos. El viento se cuela por donde antes había protección.",
    ],
    "PARTNER_VISION": [
        "La figura inexistente que creíste ver sigue grabada en tu memoria.",
        "Mirás de reojo, esperando que el alpinista fantasma vuelva a aparecer.",
        "La hipoxia fabricó una compañía que nunca existió. La soledad real pesa más ahora.",
        "La silueta que viste junto a vos se desvaneció, pero su recuerdo es más real que el hielo.",
        "Mirás al vacío donde estabas seguro de que alguien caminaba. Solo hay nieve y viento.",
    ],
    "EQUIPMENT_DROP": [
        "La pérdida del equipo del turno anterior pesa en tu mochila y en tu mente.",
        "Con menos recursos de seguridad a tu disposición, el abismo se siente más cerca.",
        "Extrañás el equipo perdido. Cada capa de seguridad que no tenés hace la montaña más grande.",
        "El espacio vacío en el arnés te recuerda lo que perdiste. Avanzás con menos márgenes.",
        "Sin aquel equipo, cada paso es un poco más expuesto. La montaña castiga la falta de preparación.",
    ],
    "SECOND_WIND": [
        "Aprovechando el último impulso de energía del segundo aliento, forzás el paso.",
        "El alivio del segundo aire aún te sostiene, pero sabés que es temporal.",
        "La oleada de energía recorre tus músculos como un regalo inesperado.",
        "El segundo aliento inyecta urgencia en tus movimientos. Hay que aprovechar antes de que se evapore.",
        "Sentís la fuerza volver como un arroyo seco que recibe lluvia. Sabés que no dura.",
    ],
}

# Frases nocturnas
NIGHT_FLAVOR = [
    "La oscuridad de la noche lo envuelve todo, volviendo cada grieta invisible.",
    "La luna proyecta sombras largas y espectrales sobre la pared de hielo.",
    "El frío nocturno congela las lágrimas antes de que caigan.",
    "De noche, la inmensidad del K2 se siente como un vacío absoluto.",
    "Tu linterna frontal apenas corta la negrura de la noche montañesa.",
    "El aire nocturno corta la garganta como vidrio molido.",
    "Las estrellas parecen frías e indiferentes. El cosmos no se conmueve por tu pequeña lucha.",
    "El silencio nocturno es más profundo que cualquier otro. Solo interrumpido por el crujido del hielo.",
    "La oscuridad transforma cada sombra en una grieta posible. Caminás con los sentidos alerta.",
    "Las horas de la noche se estiran como el hielo. El amanecer parece una promesa lejana.",
    "Bajo el manto nocturno, el K2 es una silueta que se pierde en un cielo violáceo.",
    "El frío nocturno tiene una cualidad diferente: es un frío que se infiltra, que espera, que nunca se va.",
]

# Condiciones de Cumbre
SUMMIT_CONDITIONS = {
    "legendary": "Llegaste como si la montaña te hubiera esperado. El K2 se rindió ante tu preparación y voluntad impecable.",
    "strong": "Llegaste con recursos y energía. La montaña te respetó.",
    "barely": "Llegaste en los huesos. Cada paso fue una agonía. Pero llegaste.",
    "exhausted": "Llegaste arrastrándote. Cada músculo gritaba que no, pero la cima te escupió al final.",
    "miracle": "No deberías haber llegado. Y sin embargo, aquí estás.",
}