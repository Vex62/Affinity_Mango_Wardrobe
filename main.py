# This is the main file of the project
import os

import pandas as pd
from OutfitViewer import OutfitViewer
from PatternDiscovery import PatternDiscovery
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


def print_log(message):
    # Use a breakpoint in the code line below to debug your script.
    print(f'{message}')  # Press Ctrl+F8 to toggle the breakpoint.


def create_outfit(tops_data, bottoms_data, footwear_data, patterns):
    # generate random top and for every pattern save the specific characteristic of top
    top = tops_data.sample()
    top_pattern = []
    sex = top['des_sex'].values[0]
    for pattern in patterns:
        top_pattern.append(top[pattern[0]].values[0])

    # find a valid bottom
    validBottom = False
    while not validBottom:
        bottom = bottoms_data.sample()
        for idx, pattern in enumerate(patterns):
            if bottom[pattern[0]].values[0] == top_pattern[idx]\
                    and (bottom['des_sex'].values[0] == sex or bottom['des_sex'].values[0] == 'Unisex'):
                validBottom = True
            else:
                validBottom = False

    # find a valid footwear
    validFootwear = False
    while not validFootwear:
        footwear = footwear_data.sample()
        for idx, pattern in enumerate(patterns):
            if footwear[pattern[0]].values[0] == top_pattern[idx]\
                    and (footwear['des_sex'].values[0] == sex or footwear['des_sex'].values[0] == 'Unisex'):
                validFootwear = True
            else:
                validFootwear = False


    return [top['cod_modelo_color'], bottom['cod_modelo_color'], footwear['cod_modelo_color']]


def add_outfit(new_products_list):
    path = 'datathon/dataset/custom_outfit_data.csv'
    custom_outfit_data = pd.read_csv(path)

    if custom_outfit_data.shape[0] > 1:
        print("filas: "+str(custom_outfit_data.shape[0]))
        nuevo_cod_outfit = custom_outfit_data['cod_outfit'].max() + 1
    else:
        nuevo_cod_outfit = 1

    # Crea un nuevo DataFrame con los códigos dados y el nuevo código de outfit
    for product_code in new_products_list:
        nuevos_datos = pd.DataFrame({'cod_outfit': nuevo_cod_outfit,
                                     'cod_modelo_color': product_code})
        custom_outfit_data = pd.concat([custom_outfit_data, nuevos_datos], ignore_index=True)

    custom_outfit_data.to_csv(path, mode='w', index=False)


def csv_to_dic(pattern_data, idx_col, heuristic):
    df = pd.read_csv(pattern_data, index_col=idx_col)

    relaciones_dict = {}
    for color in df.index:
        fila = df.loc[color]
        colores_relacionados = fila[fila >= heuristic].index.tolist()
        relaciones_dict[color] = colores_relacionados

    return relaciones_dict


def main():
    outfit_data = pd.read_csv('datathon/dataset/outfit_data.csv')
    product_data = pd.read_csv('datathon/dataset/product_data.csv')
    joined_data = pd.read_csv('datathon/dataset/joined_data.csv')

    """joined_data = pd.merge(outfit_data, product_data, on='cod_modelo_color', how='inner')
    joined_data = joined_data.sort_values(by='cod_outfit')
    joined_data.to_csv('datathon/dataset/joined_data.csv', index=False)"""

    # type of elements of one outfi
    tops_data = product_data[product_data['des_product_category'] == 'Tops']
    bottoms_data = product_data[product_data['des_product_category'] == 'Bottoms']
    footwear_data = product_data[product_data['des_product_family'] == 'Footwear']

    # declaration of patterns
    patterns = []
    color_matching = csv_to_dic("datathon/patterns/color_matching.csv", "des_agrup_color_eng", 300)
    patterns.append(["des_agrup_color_eng",color_matching])

    # outfits creation
    for i in range(0,9):
        list_outfit_products = create_outfit(tops_data, bottoms_data, footwear_data, patterns)
        add_outfit(list_outfit_products)

    custom_outfit_data = pd.read_csv('datathon/dataset/custom_outfit_data.csv')
    custom_joined_data = pd.merge(custom_outfit_data, product_data, on='cod_modelo_color', how='inner')
    custom_joined_data.to_csv('datathon/dataset/custom_joined_data.csv', index=False)


    #patternDiscovery = PatternDiscovery()
    #patternDiscovery.color_matching()

    viewer = OutfitViewer()
    viewer.run()




if __name__ == '__main__':
    main()
