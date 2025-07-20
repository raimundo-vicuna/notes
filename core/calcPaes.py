class Paes():
    def calcScore(nem, ranking, lectura, m1, m2, historia_ciencias):
        ponderaciones = {
            "nem": 0.15,
            "ranking": 0.25,
            "lectura": 0.10,
            "m1": 0.35,
            "m2": 0.05,
            "historia_ciencias": 0.10
        }

        puntaje_total = (
            nem * ponderaciones["nem"] +
            ranking * ponderaciones["ranking"] +
            lectura * ponderaciones["lectura"] +
            m1 * ponderaciones["m1"] +
            m2 * ponderaciones["m2"] +
            historia_ciencias * ponderaciones["historia_ciencias"]
        )

        return puntaje_total