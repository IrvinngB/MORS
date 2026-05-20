import random
from app.core.config import settings


# ═══════════════════════════════════════════════════════════════
# ROLE VOICE MODIFIERS
# Each role has a distinct narrative voice — not rewritten text,
# but tone modifiers (prefix/suffix) that alter how the same
# action feels from that role's perspective.
# ═══════════════════════════════════════════════════════════════

ROLE_VOICE: dict[str, dict] = {
    "sherpa": {
        "prefixes": [
            "",  # 40% no prefix — not every line needs it
            "",
            "",
            "El hielo cede. ",
            "Buen paso. ",
            "La montaña nos habla. ",
        ],
        "suffixes": [
            "",
            "",
            " El camino es claro.",
            " Mis pies conocen este hielo.",
            " Otro paso, otro respiro.",
        ],
    },
    "clasico": {
        "prefixes": [
            "",
            "",
            "",
            "Sin ayuda. ",
            "Como debe ser. ",
            "Solo con mi voluntad. ",
        ],
        "suffixes": [
            "",
            "",
            " Sin atajos.",
            " El purismo tiene su precio.",
            " La montaña no regala nada.",
        ],
    },
    "investigador": {
        "prefixes": [
            "",
            "",
            "",
            "Observo: ",
            "Datos: ",
            "La ciencia dice: ",
        ],
        "suffixes": [
            "",
            "",
            " La evidencia confirma mis hipótesis.",
            " Condiciones dentro de los parámetros esperados.",
            " Anoto mentalmente cada detalle.",
        ],
    },
    "tecnico": {
        "prefixes": [
            "",
            "",
            "",
            "Ángulo de placa: manejable. ",
            "La técnica importa. ",
            "Equipo revisado. ",
        ],
        "suffixes": [
            "",
            "",
            " La cuerda aguanta.",
            " Cada nudo, una promesa.",
            " El equipo no falla si lo cuidas.",
        ],
    },
    "medico": {
        "prefixes": [
            "",
            "",
            "",
            "Diagnóstico: ",
            "Noto en mi cuerpo: ",
            "Signos vitales estables. ",
        ],
        "suffixes": [
            "",
            "",
            " El cuerpo aguanta, por ahora.",
            " Monitoreo cada síntoma.",
            " La medicina no sirve de mucho aquí, pero la disciplina sí.",
        ],
    },
}

# ═══════════════════════════════════════════════════════════════
# MEMORIA DE EVENTOS ANTERIORES (POST-EVENT CONTINUITY)
# ═══════════════════════════════════════════════════════════════

POST_EVENT_OVERRIDES = {
    "DISTANT_AVALANCHE": [
        "Aún con el rugido de la avalancha resonando en tus oídos, intentás concentrarte.",
        "El trueno de nieve del turno anterior te dejó alerta. Mirás hacia arriba constantemente.",
        "Con el polvo de la avalancha lejana todavía asentándose, continuás.",
    ],
    "HALLUCINATION": [
        "Las sombras que viste antes parecen retirarse, pero sabés que siguen ahí.",
        "Sacudís la cabeza para espantar los ecos de las voces que creíste oír.",
        "La mente aún lucha por distinguir el hielo real de las visiones de la hipoxia.",
    ],
    "WIND_GUST": [
        "Recuperando la compostura tras el empuje del viento, volvés a erguirte.",
        "Con el cuerpo tenso tras la última ráfaga violenta, reanudas el movimiento.",
        "Aún sintiendo el impacto del viento en el pecho, te aferrás al hielo.",
    ],
    "O2_REGULATOR_FAIL": [
        "Buscando desesperadamente recuperar el ritmo respiratorio tras el fallo del regulador...",
        "Aún mareado por el súbito corte de oxígeno, intentás reaccionar.",
    ],
    "FROSTBITE": [
        "El dolor sordo y helado en tus extremidades congeladas te acompaña en cada movimiento.",
        "Con los dedos rígidos por el principio de congelamiento, cada manipulación es un calvario.",
        "El recuerdo del frío mordiendo tu carne te empuja a no detenerte.",
    ],
    "PULMONARY_EDEMA": [
        "Cada respiración sigue siendo un gorgoteo húmedo y doloroso. El edema no da tregua.",
        "El pecho te arde. Sabés que tus pulmones están al límite, pero seguís.",
    ],
    "TENT_COLLAPSE": [
        "Sin el refugio seguro de la carpa tras su colapso, el K2 se siente infinitamente más hostil.",
        "Aún con la nieve de la carpa derretida pegada al cuerpo, seguís expuesto.",
    ],
    "PARTNER_VISION": [
        "La figura inexistente que creíste ver sigue grabada en tu memoria.",
        "Miras de reojo, esperando que el alpinista fantasma vuelva a aparecer.",
    ],
    "EQUIPMENT_DROP": [
        "La pérdida del equipo del turno anterior pesa en tu mochila y en tu mente.",
        "Con menos recursos de seguridad a tu disposición, el abismo se siente más cerca.",
    ],
    "SECOND_WIND": [
        "Aprovechando el último impulso de energía del segundo aliento, forzás el paso.",
        "El alivio del segundo aire aún te sostiene, pero sabés que es temporal.",
    ],
}

# ═══════════════════════════════════════════════════════════════
# FRASES NOCTURNAS (NIGHT FLAVOR)
# ═══════════════════════════════════════════════════════════════

NIGHT_FLAVOR = [
    "La oscuridad de la noche lo envuelve todo, volviendo cada grieta invisible.",
    "La luna proyecta sombras largas y espectrales sobre la pared de hielo.",
    "El frío nocturno congela las lágrimas antes de que caigan.",
    "De noche, la inmensidad del K2 se siente como un vacío absoluto.",
    "Tu linterna frontal apenas corta la negrura de la noche montañesa.",
    "El aire nocturno corta la garganta como vidrio molido.",
]



# ═══════════════════════════════════════════════════════════════
# MOUNTAINEERING QUOTES
# Real quotes from real climbers. These appear at the end of
# epitaphs and summit narratives for authenticity.
# ═══════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════
# NEPALI PHRASES
# Words of the Himalayas. Mixed into epitaphs and summit narratives
# alongside mountaineering quotes for cultural authenticity.
# ═══════════════════════════════════════════════════════════════

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
    "Dherai mathi (धेरै माथि) — Demasiado alto.",
]


# ═══════════════════════════════════════════════════════════════
# INTRODUCCIÓN
# ═══════════════════════════════════════════════════════════════

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

# ── Avanzar Normal ──────────────────────────────────────────────
ADVANCE_NORMAL = {
    "low": [
        "Avanzas con paso firme. El terreno cede bajo tus botas.",
        "La ascensión continúa. Cada paso es una negociación con la altura.",
        "El crampon muerde el hielo. Un metro más, siempre un metro más.",
        "Tu respiración marca el ritmo. Inhala, pisa, exhala, repite.",
        "Progresas a ritmo constante. El sendero inferior aún es benévolo.",
        "Subes con lentitud pero con técnica. Cada paso firme ahorra valiosa energía.",
        "El piolet se clava en la nieve compacta con un sonido seco.",
        "Ascendés sintiendo el peso de la mochila. El K2 empieza a cobrar su precio."
    ],
    "mid": [
        "El aire se adelgaza. Cada paso requiere más conciencia que fuerza.",
        "La pendiente no perdona. Avanzas con la precisión de quien sabe que un error cuesta caro.",
        "El viento silba entre las rocas. No te detienes.",
        "Las grietas empiezan a acechar a los lados. La concentración debe ser absoluta.",
        "Un paso tras otro. El K2 impone su ley de paciencia helada.",
        "Tus piernas arden levemente. La altura media empieza a demandar respeto.",
        "El frío se intensifica, pero tu cuerpo mantiene la temperatura con el movimiento constante.",
        "Pisas sobre nieve dura. La tracción es buena, pero la pendiente se agudiza."
    ],
    "high": [
        "Cada paso es una batalla contra tu propio cuerpo. La altitud cobra su tributo.",
        "El oxígeno es un recuerdo. Avanzas por inercia y terquedad.",
        "La montaña se siente más cerca, pero tu cuerpo grita que pare.",
        "La cabeza te pulsa rítmicamente por la presión del aire delgado.",
        "Haces una pausa de tres segundos entre cada paso para recuperar el aliento.",
        "Tus botas se sienten de plomo. La fatiga se acumula en las rodillas.",
        "El paisaje es sobrecogedor, pero apenas tenés ojos para mirar dónde pisás.",
        "El viento sopla con fuerza rítmica, intentando retrasar tu progreso."
    ],
    "death_zone": [
        "La zona de la muerte no perdona. Cada paso es un acto de rebeldía contra la fisiología.",
        "Tu cuerpo se consume. Avanzas porque detenerte significa morir.",
        "El aire es veneno. Cada respiración quema. Pero la cima está ahí.",
        "Por encima de los 8000 metros, sos un intruso en un mundo que rechaza la vida.",
        "Tus pulmones buscan desesperadamente moléculas de oxígeno en el aire helado.",
        "Te arrastras un metro a la vez. Cada paso adelante requiere toda tu fuerza de voluntad.",
        "El silencio de la altura extrema te envuelve. El mundo de los vivos queda muy abajo.",
        "El tiempo se escurre de prisa aquí. Cada minuto sin cumbre es un riesgo letal."
    ],
}

# ── Avanzar Agresivo ────────────────────────────────────────────
ADVANCE_AGGRESSIVE = {
    "low": [
        "Te lanzas hacia arriba con determinación. El aire se vuelve más escaso.",
        "La pendiente se acentúa. Tus músculos protestan pero el cuerpo responde.",
        "Aceleras el paso. La montaña parece retroceder ante tu empuje.",
        "Forzás el ritmo en la sección inferior. Querés ganar altitud antes de que empeore el clima.",
        "Un avance rápido y enérgico. Sentís la adrenalina recorrer tus venas.",
        "Empujás tu cuerpo al límite inicial. El terreno lo permite, por ahora.",
        "Pisas con fuerza, devorando metros. Tus crampones muerden el hielo con agresividad.",
        "Ritmo acelerado. La respiración se agita, pero la ganancia de altitud es innegable."
    ],
    "mid": [
        "Forzas el ritmo. El hielo cruje bajo tus pies. Es una apuesta peligrosa.",
        "La adrenalina te empuja hacia arriba. Pero el cuerpo tiene límites.",
        "Cada movimiento es más arriesgado. La fatiga nubla el juicio.",
        "Saltás una pequeña grieta sin dudarlo. La velocidad es tu aliada y tu peligro.",
        "Tu respiración es un jadeo constante. La ambición te obliga a apurar el paso.",
        "Subís a ritmo de ataque. Las pendientes medias requieren un esfuerzo cardíaco brutal.",
        "Ignorás las señales de cansancio de tus piernas y seguís empujando hacia arriba.",
        "Un movimiento rápido para superar una placa de hielo expuesta. Riesgo calculado."
    ],
    "high": [
        "Te lanzas hacia lo imposible. El cuerpo grita, la mente ordena avanzar.",
        "Es una locura. Lo sabes. Pero detenerte duele más.",
        "La pendiente se vuelve vertical. Cada paso es un acto de fe ciega.",
        "El pecho te estalla por el esfuerzo de avanzar rápido en aire enrarecido.",
        "Superás un tramo empinado con movimientos desesperados. La fatiga es inmensa.",
        "Tus muscles consumen sus últimas reservas de energía en esta embestida.",
        "Te obligás a dar pasos largos y rápidos, ignorando el dolor en las sienes.",
        "Una aceleración arriesgada cerca del hombro del K2. La altura te castiga el doble."
    ],
    "death_zone": [
        "Te arrastras hacia arriba con una furia que no sabías que tenías. La muerte te pisa los talones.",
        "Cada movimiento podría ser el último. Avanzas igual.",
        "La zona de la muerte no distingue entre valientes y necios. Tú eres ambos.",
        "Es un ataque desesperado a la cumbre. O llegás ahora o no lo contarás.",
        "Tus extremidades se sienten entumecidas, pero tu mente ordena avanzar a zancadas.",
        "Corrés una carrera contra el reloj biológico. Cada segundo de esfuerzo agresivo te agota el doble.",
        "Una acometida brutal sobre la última pendiente de hielo azul. Pura locura vertical.",
        "La cima está al alcance del piolet, y empujás tu cuerpo con una violencia suicida."
    ],
}

# ── Asegurar Ruta ───────────────────────────────────────────────
SECURE_ROUTE = [
    "Clavas una estaca en la roca helada. La ruta queda marcada para el retorno.",
    "Aseguras un tramo. El siguiente paso estará protegido.",
    "La cuerda tensa contra el viento. Un hilo de seguridad en medio del abismo.",
    "Cada nudo es una promesa: volverás por aquí.",
    "El hielo cede ante el piolet. Aseguras el camino para quien venga después.",
    "Instalás un anclaje firme en la pared de hielo azul. La cuerda fija te da tranquilidad.",
    "Fijás un tramo de cuerda en una sección expuesta. El descenso será más seguro gracias a esto.",
    "Trabajás con los mosquetones con dedos entumecidos, asegurando la línea de vida."
]

# ── Acampar ─────────────────────────────────────────────────────
CAMP = {
    "clear": [
        "Armas el campamento bajo un cielo despejado. Las estrellas parecen más cercanas aquí.",
        "La tienda resiste el viento. Te permites un respiro mientras la noche pasa.",
        "El cielo estrellado te regala una noche de calma visual. El frío es seco e intenso.",
        "Montás el refugio con relativa facilidad. La montaña te da una tregua hoy.",
        "Bajo una bóveda celeste cristalina, la carpa se convierte en tu pequeño oasis cálido."
    ],
    "storm": [
        "La tormenta azota la tienda. Cada ráfaga es un recordatorio de tu fragilidad.",
        "El viento amenaza con arrancar la carpa. Te aferras a la lona como a tu vida.",
        "La nieve se acumula contra la tela. El mundo exterior ha desaparecido.",
        "La ventisca aúlla afuera con furia. Rezas para que las estacas aguanten el embate.",
        "El interior de la carpa tiembla violentamente. La tormenta golpea sin descanso.",
        "La lona azota tus oídos con ruidos ensordecedores. Dormir es imposible en este infierno blanco."
    ],
    "default": [
        "Armas el campamento entre temblores. El suelo congelado complica todo.",
        "La tienda es tu único refugio contra la inmensidad helada.",
        "Te refugias. El frío se cuela por las costuras, pero estás vivo.",
        "El viento muerde la carpa, pero el refugio te aísla lo suficiente para no congelarte.",
        "Te acurrucás dentro de la tienda, escuchando el crujir constante del hielo exterior.",
        "Montás la carpa a toda prisa con dedos temblorosos. Cualquier refugio es sagrado ahora."
    ],
}

# ── Usar Oxígeno ────────────────────────────────────────────────
USE_OXYGEN = [
    "Abres el tanque. El oxígeno fluye y el mundo se vuelve más claro.",
    "Respiras profundamente. La niebla en tu mente se disipa.",
    "El gas silba al salir. Por un momento, recuerdas cómo se siente respirar sin esfuerzo.",
    "La máscara se empaña. Pero el aire que entra es dulce, casi olvidado.",
    "Un lujo en la montaña. El oxígeno suplementario te devuelve fragmentos de humanidad.",
    "El flujo frío de gas te llena los pulmones. Tu cerebro agradece el torrente de energía.",
    "El zumbido del regulador te acompaña mientras el aire puro te devuelve la fuerza muscular.",
    "Inhalás el gas presurizado. Sentís que tu cuerpo recupera la compostura térmica y mental."
]

# ── Comer ───────────────────────────────────────────────────────
EAT = [
    "Una ración tibia. El cuerpo agradece el gesto.",
    "Comes lo mínimo. La supervivencia no permite excesos.",
    "El alimento sabe a nada, pero tu cuerpo lo absorbe como un milagro.",
    "Masticas despacio. Cada caloría cuenta aquí arriba.",
    "La comida es un ritual. Un momento de normalidad en medio del caos.",
    "Ingerís alimentos deshidratados. Sabor a metal y supervivencia, pero necesario.",
    "Te obligás a tragar la ración congelada. Tu cuerpo necesita combustible de inmediato.",
    "Cada bocado es digerido con lentitud. Las calorías te devolverán algo de calor interno."
]

# ── Descender ───────────────────────────────────────────────────
DESCEND = [
    "Desciendes. La presión en tu pecho disminuye con cada metro.",
    "Bajas el ritmo. El valle te recibe con algo de calor residual.",
    "Cada paso hacia abajo es una rendición, pero también una salvación.",
    "La montaña te suelta, metro a metro. El aire se vuelve más amable.",
    "Retrocedes. No es derrota, es estrategia. La montaña estará ahí mañana.",
    "Vas perdiendo altitud. Sentís que recuperás el aliento con cada tramo de bajada.",
    "El descenso requiere rodillas firmes. La gravedad ayuda, pero el cansancio acecha.",
    "Bajás con cuidado por las cuerdas fijas. Dejar atrás la altura extrema alivia tu mente."
]

# ── Descansar ───────────────────────────────────────────────────
REST = [
    "Te detienes. Solo un momento, pero el cuerpo lo necesitaba.",
    "Esperas. La inmovilidad pesa, pero el descanso es necesario.",
    "Te sientas sobre la mochila. El viento te recuerda que no puedes quedarte aquí mucho tiempo.",
    "Cierras los ojos un instante. El frío te devuelve a la realidad.",
    "Un respiro. La montaña no espera, pero tu cuerpo sí lo necesita.",
    "Apoyás la frente sobre el piolet. El pecho sube y baja al ritmo de tu cansancio.",
    "Detenerse a recuperar el pulso. Sentís los latidos retumbar en tus oídos.",
    "Cinco minutos de inmovilidad absoluta. La fatiga retrocede un milímetro."
]

# ── Free Heal (Medico) ──────────────────────────────────────────
FREE_HEAL = [
    "Te aplicas un vendaje de emergencia. Las manos tiemblan, pero la técnica es precisa.",
    "Inyectas lo que queda de analgésico. El dolor retrocede, no desaparece.",
    "Primeros auxilios de fortuna. Funciona lo suficiente para seguir.",
    "Tu entrenamiento médico vale más que cualquier equipo aquí arriba.",
    "Limpiás una herida menor con alcohol antiséptico. El ardor te despierta los sentidos.",
    "Tratás los síntomas de congelamiento incipiente. Técnica médica en condiciones extremas.",
    "Administrás medicación básica para la altura. Prevención activa frente al colapso corporal.",
    "Con sutura de emergencia y esparadrapo, te remendás para aguantar unas horas más."
]

# ── Conmutar Oxígeno ─────────────────────────────────────────────
TOGGLE_OXYGEN = [
    "Manipulas la válvula del regulador de oxígeno.",
    "Ajustas el flujo de oxígeno suplementario en tu máscara.",
    "Giras la perilla del tanque de oxígeno en tu mochila.",
    "Revisas y cambias el estado de la válvula de tu regulador.",
    "El clic del regulador confirma que has cambiado el régimen de flujo del tanque.",
    "Ajustás el caudalímetro con guantes gruesos. Operación delicada.",
    "Giras la perilla de paso. El silbido del gas cambia de tono en tu espalda.",
    "Manipulación táctil del tanque. El flujo suplementario se adapta a tu decisión."
]


# ═══════════════════════════════════════════════════════════════
# WILLPOWER TIERS (4 levels now, was 3)
# ═══════════════════════════════════════════════════════════════

# DESPAIR (< 15): fragmented, broken
LOW_WILLPOWER_DESPAIR = [
    "La mente vagabundea. El suelo parece más cercano de lo que debería.",
    "La voluntad se erosiona. Cada paso es una duda.",
    "Piensas en rendirte. No es un pensamiento nuevo, pero hoy pesa más.",
    "Las sombras se alargan. No sabes si es el cansancio o algo más.",
    "Tu reflejo en el hielo te devuelve una mirada que no reconoces.",
    "El silencio te habla. Dice cosas que no quieres escuchar.",
    "¿Qué sentido tiene todo esto? El vacío de la montaña se traslada a tu interior.",
    "La nieve parece un lecho cómodo para acostarse y no despertar.",
    "Tu nombre carece de significado aquí arriba. Eres solo un cuerpo que se apaga.",
    "La voluntad está rota. Te movés por pura inercia biológica, sin rumbo mental."
]

# PURPOSE DOUBT (15–50): questioning why, not whether
LOW_WILLPOWER_DOUBT = [
    "¿Por qué estoy aquí? La pregunta no tiene respuesta, solo eco.",
    "La cima ya no parece una meta. Parece una excusa.",
    "Miras hacia arriba y no sabes si es ambición o estupidez.",
    "El cuerpo sigue, pero la mente empieza a negociar.",
    "Recuerdas por qué viniste. El recuerdo se siente de otra persona.",
    "Cada paso es una pregunta sin respuesta.",
    "La cumbre prometida no vale el dolor de cada respiración.",
    "Te cuestionás cada sacrificio que te trajo a esta pared de hielo.",
    "Pensás en los que se quedaron abajo. En el calor. En la vida normal.",
    "La montaña te parece un monumento a la soberbia humana hoy."
]

# Normal (>= 50): no override needed


# ═══════════════════════════════════════════════════════════════
# SUMMIT NARRATIVE (victory)
# ═══════════════════════════════════════════════════════════════

SUMMIT_NARRATIVE = {
    "default": [
        "La cima. 8611 metros. El mundo entero bajo tus pies.",
        "Llegaste. El K2, el asesino, el salvaje — rendido ante tu voluntad.",
        "8611 metros. Cada paso del camino te trajo aquí. Ahora el cielo es tu techo.",
        "La cima del K2. Donde otros murieron, tú llegaste.",
    ],
    "sherpa": [
        "La cima. 8611 metros. La montaña que guiaste con pasos conocidos.",
        "Llegaste. El K2 no es un enemigo para quien lo conoce. Es un camino.",
        "8611 metros. Tus pies saben lo que otros solo sueñan.",
    ],
    "clasico": [
        "La cima. 8611 metros. Sin oxígeno, sin atajos, sin ayuda. Solo tú.",
        "Llegaste. El purismo tiene su recompensa: la cima del K2, sin trampas.",
        "8611 metros. Cada metro fue tuyo. Nadie te lo regaló.",
    ],
    "investigador": [
        "La cima. 8611 metros. Los datos confirman lo que la intuición sabía.",
        "Llegaste. La montaña, analizada, comprendida, conquistada con conocimiento.",
        "8611 metros. La hipótesis era correcta: se puede.",
    ],
    "tecnico": [
        "La cima. 8611 metros. La técnica venció donde la fuerza sola no alcanza.",
        "Llegaste. Cada nudo, cada crampon, cada decisión técnica — perfecta.",
        "8611 metros. El equipo no falló. La técnica fue tu salvación.",
    ],
    "medico": [
        "La cima. 8611 metros. Tu cuerpo resistió. Tu mente, también.",
        "Llegaste. El médico que se curó a sí mismo para alcanzar la cima.",
        "8611 metros. Signos vitales: vivos. Diagnóstico: victoria.",
    ],
}

SUMMIT_CONDITIONS = {
    "strong": "Llegaste con recursos y energía. La montaña te respetó.",
    "barely": "Llegaste en los huesos. Cada paso fue una agonía. Pero llegaste.",
    "miracle": "No deberías haber llegado. Y sin embargo, aquí estás.",
}


# ═══════════════════════════════════════════════════════════════
# ZONA DE LA MUERTE
# ═══════════════════════════════════════════════════════════════

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
    "El viento silba con una frecuencia que parece llamarte al descanso eterno."
]

# ── Tormenta ────────────────────────────────────────────────────
STORM = [
    "La tormenta te envuelve. Visibilidad cero.",
    "El viento aúlla. La nieve golpea tu rostro sin piedad.",
    "No ves nada más allá de tu nariz. El mundo se reduce a blanco y dolor.",
    "La tormenta no distingue entre preparados y desprevenidos. Todos sufren igual.",
    "El frío penetra hasta los huesos. La tormenta no tiene piedad.",
    "La ventisca te desorienta. Perdés la noción de dónde está la pendiente.",
    "El viento sopla a más de cien kilómetros por hora, amenazando con arrancarte de la pared.",
    "La nieve acumulada te llega a las rodillas. Cada paso requiere levantar las piernas con un esfuerzo titánico."
]

# ── Suffixes contextuales ───────────────────────────────────────
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
        "Te preguntás cuánto tiempo pasará antes de que te conviertas en otra marca del camino."
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
# ═══════════════════════════════════════════════════════════════
# EPITAFIOS
# ═══════════════════════════════════════════════════════════════

EPITAPHS = {
    "DEAD_EXHAUSTION": [
        "Tu cuerpo se rindió antes que tu voluntad. La montaña respetó tu esfuerzo.",
        "El agotamiento te alcanzó. No fue falta de coraje, fue falta de aire.",
        "Caminaste hasta que tus piernas dejaron de obedecer. La montaña recuerda tu nombre.",
    ],
    "DEAD_COLD": [
        "El frío te reclamó. Tu cuerpo se convirtió en parte del glaciar.",
        "La hipotermia fue silenciosa. Te dormiste en la nieve y no despertaste.",
        "El hielo te abrazó. Ahora eres parte eterna de la montaña.",
    ],
    "DEAD_FALL": [
        "La gravedad fue más rápida que tu reflejo. El abismo te recibió sin preguntas.",
        "Un paso en falso. Eso fue todo. La montaña no perdona distracciones.",
        "Caíste. El eco de tu grito se perdió en el viento.",
    ],
    "DEAD_STORM": [
        "La tormenta fue más fuerte que tu voluntad. El viento te arrancó de la montaña.",
        "No viste venir la ráfaga. La montaña te devolvió al valle en un instante.",
        "La ventisca te tragó. Ni tus huellas quedaron.",
    ],
    "DEAD_EDEMA": [
        "Tus pulmones se llenaron de líquido. La altitud te traicionó desde dentro.",
        "El edema pulmonar fue implacable. Cada respiración era un suplicio.",
        "Tu cuerpo no pudo con la altura. El aire se volvió tu enemigo.",
    ],
    "default": [
        "La montaña te reclamó. Tu nombre se pierde en el viento.",
        "Ma mardina (म मर्दिन) — No moriré en esta montaña.",
        "El K2 me ha reclamado, pero no me ha vencido.",
    ],
}

# Role-specific epitaph additions (appended after the base epitaph)
ROLE_EPITAPH_SUFFIX: dict[str, list[str]] = {
    "sherpa": [
        "El guía que conocía el camino pero no pudo completarlo.",
        "La montaña que guiaste tantas veces — esta vez no te dejó pasar.",
        "Tus pasos se pierden en la nieve, pero el camino queda marcado.",
    ],
    "clasico": [
        "Sin oxígeno, sin atajos, sin ayuda. Como elegiste vivir, elegiste morir.",
        "El purismo tiene su precio. Lo pagaste con dignidad.",
        "No buscaste ayuda. No la encontraste. Pero no te arrepentiste.",
    ],
    "investigador": [
        "Los datos no pudieron predecir esto. La montaña es impredecible.",
        "Tu última observación: la altitud gana siempre. Eventualmente.",
        "La hipótesis era incorrecta. La montaña no se puede analizar, solo respetar.",
    ],
    "tecnico": [
        "El equipo no falló. La técnica fue perfecta. La montaña, simplemente, es más fuerte.",
        "Cada nudo estaba bien hecho. Cada crampon, bien clavado. No fue suficiente.",
        "La técnica te llevó lejos. Pero hay límites que ningún equipo cruza.",
    ],
    "medico": [
        "El médico que no pudo curarse a sí mismo.",
        "Sabías exactamente qué estaba pasando en tu cuerpo. Eso no lo hizo más fácil.",
        "Tu último diagnóstico: la montaña gana. Siempre gana.",
    ],
}


def _select_from_list(lst: list[str], seed: int | None = None) -> str:
    """Select a random item from a list, optionally seeded for reproducibility."""
    if seed is not None:
        random.seed(seed)
    return random.choice(lst)


def _get_altitude_tier(altitude: float) -> str:
    """Return altitude tier: low, mid, high, death_zone."""
    if altitude >= 8000:
        return "death_zone"
    elif altitude >= 7000:
        return "high"
    elif altitude >= 6000:
        return "mid"
    return "low"


def _get_weather_category(weather: str) -> str:
    """Return weather category for narrative selection."""
    if weather in ("STORM", "WHITEOUT"):
        return "storm"
    elif weather == "CLEAR":
        return "clear"
    return "default"


def _apply_willpower_voice(text: str, willpower: float) -> str:
    """Degrade narrative prose quality based on willpower level."""
    if willpower >= 50:
        return text  # Normal: no degradation
    if willpower >= 30:
        # PURPOSE DOUBT: adds a questioning undertone
        if random.random() < 0.3:
            return text + " ¿Para qué?"
        return text
    if willpower >= 15:
        # DOUBT: shortens and adds uncertainty
        sentences = text.split(". ")
        if len(sentences) > 1:
            return sentences[0] + "."
        return text + " Tal vez."
    # DESPAIR: fragments the sentence, adds ellipsis and repetition
    words = text.split()
    if len(words) > 8:
        truncated = " ".join(words[:6])
        return f"{truncated}... no importa."
    return f"{text}..."


def _apply_role_voice(text: str, role: str, willpower: float) -> str:
    """Apply role-specific voice modifier (prefix/suffix) to narrative text.
    
    This is NOT a rewrite — it's a tone overlay. The same action feels different
    depending on who's experiencing it.
    """
    if not role or role not in ROLE_VOICE:
        return text

    voice = ROLE_VOICE[role]

    # Low willpower reduces the chance of voice modifiers (mind is too broken for persona)
    if willpower < 15:
        if random.random() < 0.7:  # 70% chance to skip voice at despair
            return text

    prefix = _select_from_list(voice["prefixes"])
    suffix = _select_from_list(voice["suffixes"])

    return f"{prefix}{text}{suffix}"


def generate_narrative(
    action: str,
    deltas: dict,
    event: dict | None,
    willpower: float,
    altitude: float,
    weather: str,
    role: str = "",
    last_event_type: str | None = None,
    turn: int = 0,
) -> str:
    """Generate composed contextual narrative for a turn.
    
    Narrative structure:
    [role voice prefix] + [action narrative] + optional [delta context] + optional [suffix]
    These are composed into a single paragraph. Event narrative is a separate paragraph.
    """
    altitude_tier = _get_altitude_tier(altitude)
    weather_cat = _get_weather_category(weather)

    # --- Action narrative ---
    if willpower < 15:
        # DESPAIR: override with low willpower fragments
        action_text = _select_from_list(LOW_WILLPOWER_DESPAIR)
    elif willpower < 50:
        # PURPOSE DOUBT: questioning tone
        action_text = _select_from_list(LOW_WILLPOWER_DOUBT)
    elif altitude_tier == "death_zone":
        action_text = _select_from_list(DEATH_ZONE)
    elif weather_cat == "storm" and action not in ("CAMP", "EAT", "USE_OXYGEN", "USE_FREE_HEAL"):
        action_text = _select_from_list(STORM)
    else:
        action_templates = {
            "ADVANCE_NORMAL": ADVANCE_NORMAL.get(altitude_tier, ADVANCE_NORMAL["low"]),
            "ADVANCE_AGGRESSIVE": ADVANCE_AGGRESSIVE.get(altitude_tier, ADVANCE_AGGRESSIVE["low"]),
            "SECURE_ROUTE": SECURE_ROUTE,
            "CAMP": CAMP.get(weather_cat, CAMP["default"]),
            "USE_OXYGEN": USE_OXYGEN,
            "EAT": EAT,
            "DESCEND": DESCEND,
            "REST": REST,
            "USE_FREE_HEAL": FREE_HEAL,
            "intro": INTRO_TEMPLATES,
        }
        templates = action_templates.get(action, ADVANCE_NORMAL["low"])
        action_text = _select_from_list(templates)

    # --- Night flavor injection ---
    # turn % 24 >= 12 means night. Injected with 35% chance to build night atmosphere.
    if turn % 24 >= 12 and random.random() < 0.35:
        night_text = _select_from_list(NIGHT_FLAVOR)
        action_text = f"{action_text} {night_text}"

    # --- Narrative Memory: continuity from previous turn's event ---
    if last_event_type and last_event_type in POST_EVENT_OVERRIDES:
        if random.random() < 0.65:
            post_event_text = _select_from_list(POST_EVENT_OVERRIDES[last_event_type])
            # Prepend continuity text to action text
            action_text = f"{post_event_text} {action_text}"

    # Apply willpower voice degradation
    action_text = _apply_willpower_voice(action_text, willpower)

    # Apply role voice modifier
    action_text = _apply_role_voice(action_text, role, willpower)

    # --- Delta context (only meaningful changes) ---
    delta_parts = []
    if deltas.get("stamina_delta", 0) < -25:
        delta_parts.append("El agotamiento se acumula.")
    if deltas.get("temp_delta", 0) < -2.5:
        delta_parts.append("El frío penetra hasta los huesos.")
    if deltas.get("willpower_delta", 0) < -12:
        delta_parts.append("La mente se nubla.")
    if deltas.get("altitude_delta", 0) > 250:
        delta_parts.append("La cima se siente más cerca.")
    if deltas.get("altitude_delta", 0) < -150:
        delta_parts.append("Bajar duele más que subir.")

    if delta_parts and random.random() < 0.6:
        delta_text = _apply_willpower_voice(" ".join(delta_parts), willpower)
        action_text = action_text + " " + delta_text

    # --- Contextual suffix ---
    if willpower < 20:
        suffix_pool = SUFFIXES["desperation"]
        suffix_chance = 0.55
    elif willpower > 70:
        suffix_pool = SUFFIXES["hope"]
        suffix_chance = 0.35
    else:
        suffix_pool = SUFFIXES["general"]
        suffix_chance = 0.30

    if random.random() < suffix_chance:
        suffix = _select_from_list(suffix_pool)
        suffix = _apply_willpower_voice(suffix, willpower)
        action_text = action_text + " " + suffix

    parts = [action_text]

    # --- Event narrative (separate paragraph, if any) ---
    if event:
        event_text = event.get("narrative", "")
        if event_text:
            parts.append(event_text)

    return "\n\n".join(parts)


def generate_summit_narrative(role: str = "", stamina: float = 100.0, hp: float = 100.0) -> str:
    """Generate narrative for reaching the summit. Varies by role and condition."""
    role_texts = SUMMIT_NARRATIVE.get(role, SUMMIT_NARRATIVE["default"])
    base = _select_from_list(role_texts)

    # Condition suffix
    condition_score = (stamina + hp) / 2
    if condition_score > 60:
        condition = SUMMIT_CONDITIONS["strong"]
    elif condition_score > 25:
        condition = SUMMIT_CONDITIONS["barely"]
    else:
        condition = SUMMIT_CONDITIONS["miracle"]

    # Pick from both mountaineering quotes and Nepali phrases
    all_quotes = MOUNTAINEERING_QUOTES + NEPALI_PHRASES
    quote = _select_from_list(all_quotes)

    return f"{base} {condition}\n\n{quote}"


def generate_epitaph(
    death_cause: str,
    max_altitude: float,
    turn: int,
    worst_moment: str = "",
    role: str = "",
) -> str:
    """Generate a poetic epitaph for the fallen climber. Varies by role."""
    cause_epitaphs = EPITAPHS.get(death_cause, EPITAPHS["default"])
    base = _select_from_list(cause_epitaphs)

    parts = [base]

    # Role-specific epitaph addition
    if role and role in ROLE_EPITAPH_SUFFIX:
        role_suffix = _select_from_list(ROLE_EPITAPH_SUFFIX[role])
        parts.append(role_suffix)

    if max_altitude >= 8000:
        parts.append(f"Llegaste a la zona de la muerte ({max_altitude:.0f}m).")
    elif max_altitude >= 7000:
        parts.append(f"Alcanzaste los {max_altitude:.0f}m antes de caer.")
    else:
        parts.append(f"Tu expedición terminó a los {max_altitude:.0f}m.")

    parts.append(f"Sobreviviste {turn} {'hora' if turn == 1 else 'horas'} en la montaña.")

    if worst_moment:
        parts.append(worst_moment)

    # Pick from both mountaineering quotes and Nepali phrases
    all_quotes = MOUNTAINEERING_QUOTES + NEPALI_PHRASES
    quote = _select_from_list(all_quotes)
    parts.append(quote)

    return " ".join(parts)
