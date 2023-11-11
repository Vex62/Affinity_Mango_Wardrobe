import kivy
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button


class OutfitViewer(App):
    def build(self):
        self.outfit_data = pd.read_csv('datathon/dataset/custom_joined_data.csv')
        self.outfits_iter = iter(self.outfit_data['cod_outfit'].unique())
        self.layout = BoxLayout(orientation='vertical')
        self.show_outfit()
        return self.layout

    def show_outfit(self):
        try:
            outfit_actual = next(self.outfits_iter)
        except StopIteration:
            self.layout.clear_widgets()
            self.layout.add_widget(Button(text="Fin del dataset", size_hint=(None, None), size=(200, 100)))
            return

        self.layout.clear_widgets()

        # Mostrar el código del outfit actual
        etiqueta = Button(text=f"Outfit: {outfit_actual}", size_hint=(None, None), size=(200, 100))
        etiqueta.bind(on_press=lambda instance: self.show_outfit())
        self.layout.add_widget(etiqueta)

        # Mostrar imágenes de productos asociados al outfit actual
        productos = self.outfit_data[self.outfit_data['cod_outfit'] == outfit_actual]
        fila_actual = BoxLayout(orientation='horizontal', spacing=10)

        for index, row in productos.iterrows():
            imagen_path = row['des_filename']
            imagen = Image(source=imagen_path, size=(200, 200), size_hint=(None, None))
            fila_actual.add_widget(imagen)

            # Mostrar hasta 3 elementos por fila
            if len(fila_actual.children) == 5:
                self.layout.add_widget(fila_actual)
                fila_actual = BoxLayout(orientation='horizontal', spacing=10)

        # Agregar la última fila si no tiene 3 elementos
        if len(fila_actual.children) > 0:
            self.layout.add_widget(fila_actual)
