import numpy as np

class Notas:
    def __init__(self, data):
        self.data = data

    def calc_promedio(self, asignatura):
        datos = self.data.get(asignatura, {})
        if not datos:
            return None

        suma_ponderada = 0
        suma_ponderaciones = 0

        for tipo_eval, contenido in datos.items():
            ponderacion = contenido['ponderacion']
            notas = contenido.get('notas', [])

            if notas:
                promedio_notas = sum(notas) / len(notas)
                suma_ponderada += promedio_notas * ponderacion
                suma_ponderaciones += ponderacion

        if suma_ponderaciones == 0:
            return None

        promedio_final = suma_ponderada / suma_ponderaciones
        return round(promedio_final, 1)

    def add_nota(self, materia, nota, tipo):
        if nota > 7:
            return
        if materia in self.data and tipo in self.data[materia]:
            self.data[materia][tipo]['notas'].append(nota)
    
    def quit_note(self, materia, nota, tipo):
        if materia == '':
            return
        if materia in self.data and tipo in self.data[materia]:
            self.data[materia][tipo]['notas'].pop(nota)
            
    def calc_promedio_final(self):
        suma_promedios = 0
        cantidad_asignaturas = 0

        for asignatura in self.data:
            promedio = self.calc_promedio(asignatura)
            if promedio is not None:
                suma_promedios += promedio
                cantidad_asignaturas += 1

        if cantidad_asignaturas == 0:
            return None

        promedio_final = suma_promedios / cantidad_asignaturas
        return round(promedio_final, 1)
    def generar_escala(self, p_max, e, n_min, n_apr, n_max):
        filas = []
        filas.append(f"{'Puntaje':>8} → {'Nota':>4}")
        filas.append("-" * 18)
        for i in range(0, p_max + 1):
            if i < e * p_max:
                n = (n_apr - n_min) * (i / (e * p_max)) + n_min
            else:
                n = (n_max - n_apr) * ((i - e * p_max) / (p_max * (1 - e))) + n_apr
            filas.append(f"{i:8} → {round(n, 1):>4}")
        return filas
    def convertir_puntaje_a_nota(self, p, p_max, e, n_min, n_apr, n_max):
        if p < e * p_max:
            n = (n_apr - n_min) * (p / (e * p_max)) + n_min
        else:
            n = (n_max - n_apr) * ((p - e * p_max) / (p_max * (1 - e))) + n_apr
        return round(n, 1)
    def nota_necesaria(self, promedio_esperado, asignatura, tipo):
        datos = self.data.get(asignatura, {})
        if not datos or tipo not in datos:
            return "Asignatura o tipo de evaluación no encontrado"

        ponderacion_tipo = datos[tipo]['ponderacion']
        notas_tipo = datos[tipo]['notas']

        suma_ponderada = 0
        suma_ponderaciones = 0

        for tipo_eval, contenido in datos.items():
            if tipo_eval == tipo:
                continue 

            ponderacion = contenido['ponderacion']
            notas = contenido.get('notas', [])

            if notas:
                promedio_notas = sum(notas) / len(notas)
                suma_ponderada += promedio_notas * ponderacion
                suma_ponderaciones += ponderacion

        for nota_simulada in np.arange(2.0, 7.05, 0.05):
            nueva_suma_ponderada = suma_ponderada + (nota_simulada * ponderacion_tipo)
            nuevo_total_ponderacion = suma_ponderaciones + ponderacion_tipo
            nuevo_promedio = nueva_suma_ponderada / nuevo_total_ponderacion

            if round(nuevo_promedio, 1) >= promedio_esperado:
                nota_necesaria = float(round(nota_simulada, 1))
                return f"Necesitas un {nota_necesaria} en {tipo} para alcanzar un {promedio_esperado} en {asignatura}"

        return f"No alcanza con ninguna nota posible en {tipo} para llegar a {promedio_esperado} en {asignatura}"
