#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <json-c/json.h>

// Declaración de la función ensamblador
extern int convert(float value);

void process_gini(const char *country, float gini_value, int index) {
    int result = convert(gini_value); // Llamar a la función ensamblador
    printf("País: %s, GINI[%d]: %d\n", country, index, result);
}

int main() {
    // Abrir el archivo JSON
    struct json_object *parsed_json;
    parsed_json = json_object_from_file("gini.json");
    if (!parsed_json) {
        fprintf(stderr, "Error al abrir o parsear el archivo gini.json\n");
        return 1;
    }

    // Verificar que el JSON contiene un array
    if (!json_object_is_type(parsed_json, json_type_array)) {
        fprintf(stderr, "El archivo JSON no contiene un array\n");
        json_object_put(parsed_json);
        return 1;
    }

    // Obtener el tamaño del array
    size_t n_gini = json_object_array_length(parsed_json);

    // Leer los valores del array
    for (size_t i = 0; i < n_gini; i++) {
        struct json_object *entry = json_object_array_get_idx(parsed_json, i);
        struct json_object *country_obj;
        struct json_object *gini_obj;

        // Obtener el país y el índice GINI
        json_object_object_get_ex(entry, "country", &country_obj);
        json_object_object_get_ex(entry, "gini", &gini_obj);

        const char *country_temp = json_object_get_string(country_obj);
        char country[100]; // Crear un buffer para almacenar la copia del país
        strncpy(country, country_temp, sizeof(country) - 1);
        country[sizeof(country) - 1] = '\0'; // Asegurar la terminación nula

        float gini_value = json_object_get_double(gini_obj);

        // Procesar el valor
        process_gini(country, gini_value, i);
    }

    // Liberar memoria del objeto JSON
    json_object_put(parsed_json);

    return 0;
}