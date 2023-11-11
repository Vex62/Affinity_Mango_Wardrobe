import kivy
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import pandas as pd
from kivy.uix.image import Image
from kivy.uix.button import Button


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
