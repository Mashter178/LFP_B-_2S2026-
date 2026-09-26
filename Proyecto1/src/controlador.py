from collections import defaultdict


class ControladorHorario:
    def __init__(self, horario):
        self.horario = horario
        self.cursos = horario.get("cursos", [])
        self.catedraticos = horario.get("catedraticos", [])
        self.aulas = horario.get("aulas", [])
        self.clases = horario.get("clases", [])

    def clasificar(self):
        return {
            "cursos": list(self.cursos),
            "catedraticos": list(self.catedraticos),
            "aulas": list(self.aulas),
            "clases": list(self.clases),
            "clases_por_dia": self.clases_por_dia(),
            "clases_por_catedratico": self.clases_por_catedratico(),
            "clases_por_aula": self.clases_por_aula(),
        }

    def clases_por_dia(self):
        grupos = defaultdict(list)
        for clase in self.clases:
            grupos[clase["dia"]].append(self.normalizar_clase(clase))
        return dict(grupos)

    def clases_por_catedratico(self):
        grupos = defaultdict(list)
        for clase in self.clases:
            grupos[self.limpiar(clase["catedratico"])].append(
                self.normalizar_clase(clase)
            )
        return dict(grupos)

    def clases_por_aula(self):
        grupos = defaultdict(list)
        for clase in self.clases:
            grupos[self.limpiar(clase["aula"])].append(
                self.normalizar_clase(clase)
            )
        return dict(grupos)

    def estadisticas(self):
        horas_por_dia = {
            dia: self.minutos_grupo(clases)
            for dia, clases in self.clases_por_dia().items()
        }
        horas_totales = sum(horas_por_dia.values())
        aulas_utilizadas = {
            self.limpiar(clase["aula"]) for clase in self.clases
        }
        catedraticos_utilizados = {
            self.limpiar(clase["catedratico"]) for clase in self.clases
        }
        cursos_programados = {
            self.limpiar(clase["curso"]) for clase in self.clases
        }

        return {
            "total_cursos": len(self.cursos),
            "total_catedraticos": len(self.catedraticos),
            "total_aulas": len(self.aulas),
            "total_clases": len(self.clases),
            "cursos_programados": len(cursos_programados),
            "cursos_sin_clase": len(self.cursos) - len(cursos_programados),
            "aulas_utilizadas": len(aulas_utilizadas),
            "aulas_disponibles": len(self.aulas) - len(aulas_utilizadas),
            "catedraticos_utilizados": len(catedraticos_utilizados),
            "horas_totales": horas_totales / 60,
            "minutos_totales": horas_totales,
            "promedio_minutos_por_clase": (
                horas_totales / len(self.clases) if self.clases else 0
            ),
            "clases_por_dia": {
                dia: len(clases)
                for dia, clases in self.clases_por_dia().items()
            },
            "horas_por_dia": horas_por_dia,
            "clases_por_aula": {
                aula: len(clases)
                for aula, clases in self.clases_por_aula().items()
            },
            "clases_por_catedratico": {
                catedratico: len(clases)
                for catedratico, clases in self.clases_por_catedratico().items()
            },
        }

    def datos_para_reportes(self):
        return {
            "clasificacion": self.clasificar(),
            "estadisticas": self.estadisticas(),
        }

    @staticmethod
    def limpiar(valor):
        return valor.strip('"')

    def normalizar_clase(self, clase):
        normalizada = dict(clase)
        for campo in ("curso", "catedratico", "aula", "seccion"):
            normalizada[campo] = self.limpiar(normalizada[campo])
        return normalizada

    @staticmethod
    def minutos(hora):
        horas, minutos = hora.split(":")
        return int(horas) * 60 + int(minutos)

    def minutos_grupo(self, clases):
        total = 0
        for clase in clases:
            total += self.minutos(clase["fin"]) - self.minutos(clase["inicio"])
        return total
