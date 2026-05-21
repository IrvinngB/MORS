# Voice and narrative templates for the Médico role (Altitude-Granular)

PREFIXES = {
    "low": [
        "",
        "Signos vitales estables en el campamento base. Frecuencia cardíaca normal. ",
        "Evaluación de la saturación de oxígeno inicial completa. ",
        "El metabolismo responde bien al esfuerzo inicial de aclimatación. ",
        "Chequeo de botiquín de emergencia y ampollas de dexametasona. ",
        "Pulsioxímetro en rango saludable. El cuerpo responde con eficacia. ",
        "Presión arterial estable. La aclimatación inicial progresa sin incidentes. ",
        "La respuesta fisiológica al esfuerzo es predecible y dentro de parámetros. ",
        "Auscultación pulmonar clara. Sin estertores ni signos de edema temprano. ",
    ],
    "mid": [
        "",
        "Primeros síntomas de hipoxia leve a 6000 metros. Cefalea tolerable. ",
        "Noto vasoconstricción periférica para proteger los órganos vitales. ",
        "Frecuencia respiratoria aumentada para compensar la baja presión parcial de O2. ",
        "El esfuerzo cardíaco en la chimenea House es severo. ",
        "La diuresis por altitud aumenta. Hay que mantener hidratación constante. ",
        "Los capilares retinianos comienzan a dilatarse. Monitoreo ocular en curso. ",
        "El hematocrito sube. La sangre se vuelve hiperviscosa progresivamente. ",
        "Eritropoyetina elevada. El riñón compensa la hipoxia como debe. ",
    ],
    "high": [
        "",
        "Acidosis respiratoria compensada por hiperventilación a 7000 metros. ",
        "Ligera descoordinación motora. Debo vigilar signos de ataxia. ",
        "La saturación de O2 en sangre cae por debajo del 70 por ciento. ",
        "El frío extremo acelera la necrosis tisular en los dedos del pie. ",
        "La memoria a corto plazo fluctúa. Posible inicio de HACE leve. ",
        "Taquicardia de reposo. El miocardio trabaja al límite de la compensación. ",
        "La perfusión cerebral disminuye. El juicio clínico empieza a comprometerse. ",
    ],
    "death_zone": [
        "",
        "Saturación de oxígeno crítica. Hipoxia cerebral severa. ",
        "Gorgoteo sutil al respirar. Alerta roja de edema pulmonar inminente. ",
        "La homeostasia celular se colapsa a 8000 metros de altitud. ",
        "Delirio clínico: auto-prescribiendo fármacos con dedos de hielo... ",
        "Edema cerebral causando presión endocraneana. Papiledema probable. ",
        "La cascada de coagulación intravascular diseminada es inminente. ",
        "Hemoglobina sin oxígeno funcional. Cianosis periférica generalizada. ",
        "La ATPasa celular deja de sintetizar. El colapso energético es total. ",
    ]
}

SUFFIXES = {
    "low": [
        "",
        " El metabolismo se adapta correctamente a las primeras pendientes.",
        " Hidratación y glucosa celular en niveles óptimos.",
        " Monitoreando la respuesta pulmonar al aire de la base.",
        " Los signos vitales son los esperados para un ascenso controlado.",
        " La frecuencia cardíaca de reposo vuelve a rangos de aclimatación adecuados.",
        " Buena perfusión periférica. Los capilares responden con normalidad.",
        " El hemograma basal confirma condiciones favorables para el ascenso.",
    ],
    "mid": [
        "",
        " Dolor de cabeza occipital, primer aviso de mal de montaña.",
        " La alcalosis respiratoria compensatoria mantiene el pH sanguíneo estable.",
        " Las extremidades responden bien al estímulo nervioso, por ahora.",
        " La función renal compensa, pero la deshidratación es un riesgo latente.",
        " La curva de disociación de la hemoglobina se desplaza a la derecha. Mecanismo de supervivencia.",
        " El edema periférico es leve. Monitoreo sin intervención todavía.",
        " La respuesta compensatoria del organismo es notable, pero tiene un límite.",
    ],
    "high": [
        "",
        " Necesito hidratarme para evitar la hiperviscosidad sanguínea y trombos.",
        " Pérdida leve de agudeza visual por hipoxia retiniana.",
        " El cerebro lucha por mantener las funciones ejecutivas lógicas.",
        " La microcirculación periférica comprometida. Riesgo de congelación inminente.",
        " Ataxia creciente. El cerebelo sufre por falta de oxigenación.",
        " La diuresis osmótica me deshidrata más rápido de lo que puedo compensar.",
        " Los reflejos tendinosos están disminuidos. Signo preocupante de compromiso neurológico.",
    ],
    "death_zone": [
        "",
        " Cada respiro es un intercambio gaseoso agónico y casi nulo.",
        " Necrosis celular activa en mis extremidades entumecidas.",
        " Edema cerebral inminente si no inicio el descenso inmediato.",
        " Diagnóstico final: la vida se apaga a nivel mitocondrial.",
        " La presión intracraneana aumenta sin freno. Riesgo inminente de herniación cerebral.",
        " Falla multiorgánica silenciosa. Los sistemas compensatorios colapsan uno a uno.",
        " Hipoxia tisular generalizada. El diagnóstico es irreversible.",
        " El ECG mental muestra arritmias del juicio. No puedo confiar en mis propias decisiones.",
    ]
}

EPITAPH_SUFFIXES = [
    "El médico de expedición que conocía cada síntoma del colapso corporal, pero no pudo evitar su propio diagnóstico fatal.",
    "Sabías con precisión científica qué estaba ocurriendo en tus células. Saberlo no hizo que el frío fuera más fácil.",
    "Tu último diagnóstico clínico: la altitud del K2 es incompatible con la vida humana a largo plazo.",
    "Trataste a otros, pero la montaña te aisló de tus propios remedios en el tramo final.",
    "Fallo multiorgánico silencioso inducido por la hipoxia extrema. La montaña te anestesió con frío eterno.",
    "El médico que diagnosticó su propio edema cerebral y no pudo prescribir el único tratamiento: descender.",
    "Conocías la farmacología de la hipoxia de memoria. La montaña no necesitaba recetas, solo tiempo y altitud.",
    "Autodiagnóstico preciso, tratamiento imposible. La medicina se rinde donde la fisiología encuentra su límite.",
]

SUMMIT_NARRATIVES = [
    "La cima. 8611 metros. A pesar del colapso celular y la hipoxia crítica, tu voluntad homeostática te mantuvo de pie.",
    "Llegaste al punto más alto. Un milagro de la fisiología humana y la disciplina médica en la zona de la muerte.",
    "8611 metros. Signos vitales débiles pero estables. Diagnóstico de cumbre completado con éxito.",
    "La cima desafiando toda predicción clínica. La homeostasis al borde del colapso se sostuvo por pura terquedad fisiológica.",
    "8611 metros. Saturación crítica, taquicardia severa, pero de pie. El cuerpo humano no debería estar aquí, y sin embargo lo está.",
    "Diagnóstico final: cumbre alcanzada. Pronóstico: reservado. La medicina diría que es imposible. Tus piernas dicen lo contrario.",
]