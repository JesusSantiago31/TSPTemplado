from flask import Flask, render_template, request
import math
import random

app = Flask(__name__)

coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

def distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])
    return total

def simulated_annealing(ruta, coord, T, T_MIN, V_enfriamiento):
    while T > T_MIN:
        dist_actual = evalua_ruta(ruta, coord)
        for _ in range(V_enfriamiento):
            # Intercambiar solo ciudades intermedias (sin cambiar origen ni destino)
            i = random.randint(1, len(ruta) - 2)
            j = random.randint(1, len(ruta) - 2)
            while i == j:
                j = random.randint(1, len(ruta) - 2)

            ruta_tmp = ruta[:]
            ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
            dist = evalua_ruta(ruta_tmp, coord)
            delta = dist_actual - dist
            if dist < dist_actual or random.random() < math.exp(delta / T):
                ruta = ruta_tmp
                break
        T -= 0.005
    return ruta

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            T = float(request.form["temperatura"])
            T_MIN = float(request.form["temperatura_minima"])
            V_enfriamiento = int(request.form["velocidad_enfriamiento"])
            origen = request.form["ciudad_origen"]
            destino = request.form["ciudad_destino"]

            if origen not in coord or destino not in coord:
                return "Ciudad origen o destino no válida."

            ciudades = list(coord.keys())
            ciudades.remove(origen)
            ciudades.remove(destino)
            random.shuffle(ciudades)
            ruta = [origen] + ciudades + [destino]

            ruta_optimizada = simulated_annealing(ruta, coord, T, T_MIN, V_enfriamiento)
            distancia_total = evalua_ruta(ruta_optimizada, coord)

            return render_template("resultado.html",
                                   ruta=ruta_optimizada,
                                   distancia=round(distancia_total, 14),
                                   origen=origen,
                                   destino=destino,
                                   T=T,
                                   T_MIN=T_MIN,
                                   V_enfriamiento=V_enfriamiento)
        except Exception as e:
            return f"Error en el procesamiento: {e}"
    return render_template("index.html", ciudades=coord.keys())

if __name__ == "__main__":
    app.run(debug=True)
