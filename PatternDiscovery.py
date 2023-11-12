from kivy.app import App
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt


class PatternDiscovery(App):

    # Returns the times two colors are use to go together
    def color_matching(self):
        # Crear un DataFrame de ejemplo
        data = pd.read_csv("datathon/dataset/joined_data.csv")
        df = pd.DataFrame(data)

        # Crear una matriz de co-ocurrencia
        co_occurrence_matrix = pd.crosstab(index=df['des_agrup_color_eng'], columns=df['cod_outfit'])
        # Inicializar una matriz de resultados con ceros
        result_matrix = pd.DataFrame(0, index=co_occurrence_matrix.index, columns=co_occurrence_matrix.index)
        # Sumar las ocurrencias para cada par de colores
        for outfit in co_occurrence_matrix.columns:
            outfit_colors = co_occurrence_matrix[co_occurrence_matrix[outfit] > 0].index
            result_matrix.loc[outfit_colors, outfit_colors] += 1
        # Mostrar la tabla resultante
        result_matrix.to_csv("datathon/patterns/color_matching.csv")

    def fabric_matching(self):
        # Crear un DataFrame de ejemplo
        data = pd.read_csv("datathon/dataset/joined_data.csv")
        df = pd.DataFrame(data)

        # Crear una matriz de co-ocurrencia
        co_occurrence_matrix = pd.crosstab(index=df['des_fabric'], columns=df['cod_outfit'])
        # Inicializar una matriz de resultados con ceros
        result_matrix = pd.DataFrame(0, index=co_occurrence_matrix.index, columns=co_occurrence_matrix.index)
        # Sumar las ocurrencias para cada par de colores
        for outfit in co_occurrence_matrix.columns:
            outfit_colors = co_occurrence_matrix[co_occurrence_matrix[outfit] > 0].index
            result_matrix.loc[outfit_colors, outfit_colors] += 1
        # Mostrar la tabla resultante
        result_matrix.to_csv("datathon/patterns/fabric_matching.csv")


    def feature_matching(self, feature_name, data):
        # Crear un DataFrame
        df = pd.DataFrame(data)

        # Crear una matriz de co-ocurrencia
        co_occurrence_matrix = pd.crosstab(index=df[feature_name], columns=df['cod_outfit'])

        # Inicializar una matriz de resultados con ceros
        result_matrix = pd.DataFrame(0, index=co_occurrence_matrix.index, columns=co_occurrence_matrix.index)

        # Iterar sobre los outfits
        for outfit in co_occurrence_matrix.columns:
            # Obtener los tipos de productos para el outfit actual
            outfit_types = co_occurrence_matrix[co_occurrence_matrix[outfit] > 0].index

            # Comparar los tipos de productos entre sÃ­
            for i in range(len(outfit_types)):
                for j in range(i + 1, len(outfit_types)):
                    type1, type2 = outfit_types[i], outfit_types[j]

                    # Contabilizar la coincidencia solo si son diferentes
                    isColor = False
                    if feature_name == "des_agrup_color_eng":
                        isColor = True
                    if type1 != type2 or isColor:
                        result_matrix.at[type1, type2] += 1
                        result_matrix.at[type2, type1] += 1

        # Guardar la matriz en un archivo CSV
        result_matrix.to_csv(f"datathon/patterns/{feature_name}_matching.csv")