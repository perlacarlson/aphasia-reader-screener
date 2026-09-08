"""
src/stories/last_leaf.py
BNAR adaptation of O. Henry's 'The Last Leaf' (1907).
"""

LAST_LEAF_DATA = {
    "title": "The Last Leaf — O. Henry",
    "tier_1": {
        "en": [
            [
                "Two artists <strong>lived</strong> here.",
                "Sue and Johnsy <strong>painted</strong>.",
                "The studio was <strong>small</strong>.",
                "November brought <strong>cold</strong>."
            ]
        ],
        "es": [
            [
                "Dos artistas <strong>vivían</strong> aquí.",
                "Sue y Johnsy <strong>pintaban</strong>.",
                "El estudio era <strong>pequeño</strong>.",
                "Noviembre trajo el <strong>frío</strong>."
            ]
        ],
        "anchors": [
            {"tag": "Tier 1 • Scene 1", "icon_key": "art_palette", "fallback": "🎨", "concept": "The Studio / El estudio", "alert": None}
        ]
    },
    "tier_2": {
        "en": [
            [
                "Two young artists <strong>lived in New York</strong>.",
                "Sue and Johnsy shared a <strong>top studio</strong>.",
                "The two women loved <strong>art and painting</strong>.",
                "In November, a <strong>cold sickness struck</strong>.",
                "Doctors called this illness <strong>pneumonia</strong>."
            ]
        ],
        "es": [
            [
                "Dos jóvenes artistas <strong>vivían en Nueva York</strong>.",
                "Sue y Johnsy compartían un <strong>estudio alto</strong>.",
                "Las dos mujeres amaban el <strong>arte y la pintura</strong>.",
                "En noviembre, una <strong>enfermedad fría atacó</strong>.",
                "Los médicos llamaban a este mal <strong>pulmonía</strong>."
            ]
        ],
        "anchors": [
            {
                "tag": "Tier 2 • Scene 1",
                "icon_key": "pneumonia_illness",
                "fallback": "🩺",
                "concept": "The Sickness in Greenwich / La enfermedad en el barrio",
                "alert": "⚠️ Metaphor Unpacked: Abstract disease personification replaced with direct medical referents"
            }
        ]
    },
    "tier_3": {
        "en": [
            [
                "In Greenwich Village, narrow streets curved between old brick buildings.",
                "At the top of a three-story house, two young artists named Sue and Johnsy shared a painting studio.",
                "They had met at a restaurant on Eighth Street, discovered they loved the same art, and decided to live together.",
                "All through the autumn, their life was happy and filled with color.",
                "But in cold November, an unseen sickness crept into the neighborhood.",
                "The doctors called this cold visitor Pneumonia, and it struck people across the city with icy fingers."
            ]
        ],
        "es": [
            [
                "En Greenwich Village, las calles estrechas cruzaban entre viejos edificios de ladrillo.",
                "En el último piso de una casa de tres pisos, dos jóvenes artistas llamadas Sue y Johnsy compartían un estudio de pintura.",
                "Se habían conocido en un restaurante de la calle Ocho, descubrieron que amaban el mismo arte y decidieron vivir juntas.",
                "Durante todo el otoño, su vida fue tranquila y llena de color.",
                "Pero en el frío noviembre, una enfermedad invisible entró al vecindario.",
                "Los médicos llamaban a este visitante frío pulmonía, y atacaba a la gente por toda la ciudad con dedos helados."
            ]
        ],
        "anchors": [
            {"tag": "Tier 3 • Chapter 1", "icon_key": None, "fallback": "🎨", "concept": "Greenwich Village & The Cold Visitor", "alert": None}
        ],
        "recaps": [
            {
                "en": [
                    "<strong>Setting:</strong> Greenwich Village art studio in late autumn (November).",
                    "<strong>Characters:</strong> Sue and Johnsy, two young painters sharing an apartment.",
                    "<strong>Primary Threat:</strong> A dangerous respiratory illness (pneumonia) enters the district."
                ],
                "es": [
                    "<strong>Lugar:</strong> Estudio de arte en Greenwich Village a finales de otoño (noviembre).",
                    "<strong>Personajes:</strong> Sue y Johnsy, dos jóvenes pintoras que comparten un departamento.",
                    "<strong>Amenaza:</strong> Una enfermedad respiratoria peligrosa (la pulmonía) entra al barrio."
                ]
            }
        ]
    }
}
