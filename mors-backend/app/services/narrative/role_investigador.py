# Voice and narrative templates for the Investigador role (Altitude-Granular)

PREFIXES = {
    "low": [
        "",
        "Calibración de instrumentos y barómetros de base completada. ",
        "El microclima inicial del glaciar muestra condiciones estándar. ",
        "Recopilando datos de temperatura del aire y humedad relativa. ",
        "El registro de la presión atmosférica es de suma importancia. ",
        "Los sensores de viento registran parámetros dentro del rango esperado. ",
        "Muestras de nieve superficiales tomadas para análisis de densidad. ",
        "Lecturas de radiación solar en niveles aceptables para la latitud. ",
        "La estratosfera se comporta según los modelos predictivos iniciales. ",
    ],
    "mid": [
        "",
        "Presión barométrica inestable detectada a 6000 metros. ",
        "El gradiente térmico de la chimenea House indica inestabilidad. ",
        "Monitoreando la disminución lineal de la densidad del aire. ",
        "Los sensores registran ráfagas de viento ascendentes y frías. ",
        "El delta térmico sugiere un cambio de masa de aire en las próximas horas. ",
        "La visibilidad se reduce según la ley de Beer-Lambert aplicada a la niebla. ",
        "Anoto las desviaciones del modelo. Los datos nunca mienten. ",
        "La humedad relativa cae. El aire se vuelve hostil para la combustión metabólica. ",
    ],
    "high": [
        "",
        "Presión parcial de oxígeno cayendo drásticamente a 7000 metros. ",
        "La evaporación latente del hielo azul es anormal hoy. ",
        "La acumulación de errores de cálculo en la libreta de notas preocupa. ",
        "El K2 se comporta como un sistema caótico altamente dinámico. ",
        "Las variables se desacoplan. El modelo lineal ya no predice nada. ",
        "Mi frecuencia cardíaca no corresponde a la ecuación esperada. Datos anómalos. ",
        "El viento Katabatic cambió de régimen. Las ecuaciones de Navier-Stokes dan resultados divergentes. ",
        "La incertidumbre en las mediciones crece exponencialmente con la altitud. ",
    ],
    "death_zone": [
        "",
        "A 8000 metros la entropía corporal supera los niveles de control. ",
        "Delirio de datos: el barómetro registra un vacío casi absoluto... ",
        "La hipoxia cerebral altera la interpretación de las variables físicas. ",
        "Las matemáticas de la supervivencia fallan por congelación de sensores. ",
        "La termodinámica dicta que mi cuerpo es un sistema abierto perdiendo energía sin retorno. ",
        "El número pi se desvanece de mi memoria. ¿Era tres coma... algo? ",
        "La segunda ley de la termodinámica se cumple. Mi entropía se maximiza. ",
        "Las constantes universales se burlan de mis cálculos temblorosos. ",
    ]
}

SUFFIXES = {
    "low": [
        "",
        " Los datos empíricos avalan nuestra planificación de ruta.",
        " Temperatura ambiental dentro de los parámetros de seguridad.",
        " Tomo notas del viento para contrastar con los modelos teóricos.",
        " La presión atmosférica coincide con los mapas meteorológicos disponibles.",
        " Registramos valores normales. El experimento avanza sin desviaciones.",
        " Cada lectura confirma la hipótesis inicial de ascenso seguro.",
        " Variables controladas. Los instrumentos calibrados responden con precisión.",
    ],
    "mid": [
        "",
        " Anoto mentalmente las desviaciones del forecast climático.",
        " La resistencia aerodinámica de la mochila aumenta con el viento.",
        " La altitud media ofrece el laboratorio perfecto para estudiar la aclimatación.",
        " La presión parcial de O2 baja. La curva de disociación se desplaza.",
        " El gradiente adiabático se manifiesta con claridad en la roca helada.",
        " Anotación: la cohesión de la nieve disminuye con la pendiente. Cuidado.",
        " La termorregulación se mantiene gracias a la vasoconstricción periférica.",
        " Los datos de viento empiezan a mostrar patrones anómalos. Registro todo.",
    ],
    "high": [
        "",
        " Ley de Charles y ley de Boyle-Mariotte confirmadas en mi pecho.",
        " La memoria RAM del ordenador portátil sufre por el frío extremo.",
        " El análisis térmico predice un enfriamiento conductivo acelerado.",
        " Los datos divergen del modelo. Necesito recalcular todo en la libreta.",
        " La hipoxia introduce ruido cognitivo. Filtrar las observaciones se vuelve difícil.",
        " Cada medición requiere más intentos. Los tiempos de reacción se degradan.",
        " El gradiente térmico entre mi cuerpo y el aire alcanza niveles preocupantes.",
    ],
    "death_zone": [
        "",
        " Mis sienes pulsan a la frecuencia de una onda senoidal disonante.",
        " El aire aquí arriba no es respirable, es solo una ecuación incompleta.",
        " Las constantes termodinámicas indican que el calor interno se disipa sin retorno.",
        " Un paso más... la cima es la singularidad matemática de este viaje.",
        " La entropía se maximiza. El sistema tiende al desorden. Yo soy el sistema.",
        " El gradiente térmico entre mi cuerpo y el aire es letal. Los datos lo confirman.",
        " Las ecuaciones se desmoronan como mi escritura en la libreta congelada.",
        " La última variable que no puedo medir es si salgo de aquí con vida.",
    ]
}

EPITAPH_SUFFIXES = [
    "Los datos no pudieron predecir el comportamiento caótico del K2. La montaña es infinitamente compleja.",
    "Tu última observación científica: la altitud gana siempre a la fisiología humana. Eventualmente.",
    "La hipótesis era incorrecta. La montaña no se puede modelar con fórmulas, solo respetar con silencio.",
    "El científico de altura que anotó su propia degradación barométrica hasta que la pluma se congeló.",
    "El sensor de tu voluntad se apagó a gran altitud, dejando tus observaciones científicas incompletas en la nieve.",
    "La segunda ley se cumplió. Tu entropía alcanzó su máximo en el hielo del Karakórum, y los datos quedaron ahí.",
    "La última anotación en la libreta es ilegible. La hipoxia te arrebató la sintaxis antes que la vida.",
    "Modelaste la montaña como un sistema. El K2 demostró que la complejidad real no cabe en una hoja de cálculo.",
]

SUMMIT_NARRATIVES = [
    "La cima. 8611 metros. La presión atmosférica registra el valor mínimo teórico. Has resuelto la gran ecuación del K2.",
    "Llegaste al punto geodésico más alto del Karakórum. Los datos confirman lo que la terquedad científica buscaba demostrar.",
    "8611 metros. Temperatura extrema, viento racheado, pero los datos de la cumbre están a salvo contigo.",
    "La cima como resultado experimental. Presión mínima, temperatura letal, oxígeno insuficiente. Y aun así, los datos se recopilaron.",
    "8611 metros. Los sensores marcan valores que desafían la fisiología humana. Pero las lecturas son reales y están en tu libreta.",
    "El experimento concluye con éxito. Los datos de la cumbre existen porque exististe para registrarlos. Eso es ciencia pura.",
]