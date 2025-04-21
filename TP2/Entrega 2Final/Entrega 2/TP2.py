import requests
import json

def get_gini():
    gini_data = {}
    # URL para obtener datos de todos los países y regiones
    url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Verificar que la respuesta contiene datos válidos
        if len(data) > 1 and isinstance(data[1], list):
            # Extraer el nombre del país/región, el año y los valores del índice GINI
            for entry in data[1]:
                if entry["value"] is not None:
                    country = entry["country"]["value"]
                    year = int(entry["date"])  # Convertir el año a entero
                    gini = entry["value"]
                    # Si el país/región no está en gini_data o el año es más reciente, actualizar
                    if country not in gini_data or gini_data[country]["year"] < year:
                        gini_data[country] = {"gini": gini, "year": year}
    else:
        print(f"Error al obtener los datos: {response.status_code}")
    # Convertir el diccionario a una lista de diccionarios
    return [{"country": country, "gini": data["gini"], "year": data["year"]} for country, data in gini_data.items()]

if __name__ == "__main__":
    gini = get_gini()
    print("Índice GINI más reciente por país/región:", gini)

    if gini:  # Verificar si la lista no está vacía
        try:
            with open("gini.json", "w") as file:
                json.dump(gini, file, indent=4)
            print("Datos guardados en gini.json")
        except Exception as e:
            print(f"Error al guardar los datos en gini.json: {e}")
    else:
        print("No se obtuvieron datos del índice GINI.")