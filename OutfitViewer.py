import streamlit as st
import pandas as pd


class OutfitViewer:
    def __init__(self, data):
        self.data = data
        self.outfit_ids = self.data['cod_outfit'].unique()
        self.current_outfit_id = None

    def show_next_outfit(self):
        if self.current_outfit_id is None:
            self.current_outfit_id = self.outfit_ids[0]
        else:
            current_index = list(self.outfit_ids).index(self.current_outfit_id)
            next_index = (current_index + 1) % len(self.outfit_ids)
            self.current_outfit_id = self.outfit_ids[next_index]

    def get_current_outfit_images(self):
        current_outfit_data = self.data[self.data['cod_outfit'] == self.current_outfit_id]
        images = current_outfit_data['des_filename'].tolist()
        return images
