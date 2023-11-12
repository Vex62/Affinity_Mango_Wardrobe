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


def create_outfit(tops_data, products_data_list, patterns, joined_data, complements_data):
    # generate random top and for every pattern save the specific characteristic of top
    newOutfit = False
    products = []
    types = []
    while not newOutfit:
        top = tops_data.sample()
        top_pattern = []
        sex = top['des_sex'].values[0]
        for pattern in patterns:
            top_pattern.append(top[pattern[0]].values[0])

        # append valid products
        products = [top['cod_modelo_color']]
        types = [top['des_product_type'].values[0]]

        # find a matching products matching top characteristics
        for product_data in products_data_list:
            validProduct = False
            product = product_data.sample()
            while not validProduct:
                product = product_data.sample()
                for idx, pattern in enumerate(patterns):
                    if product[pattern[0]].values[0] in pattern[1][top_pattern[idx]] \
                            and (product['des_sex'].values[0] == sex or product['des_sex'].values[0] == 'Unisex'):
                        validProduct = True
                    else:
                        validProduct = False
            products.append(product['cod_modelo_color'])
            types.append(product['des_product_type'].values[0])
        if isNewOutfit(joined_data, products):
            newOutfit = True

    # when created a new basic outfit, adding matching complements
    complements_df = [
        complements_data[(complements_data['des_product_family'] == 'Jewellery')],
        complements_data[(complements_data['des_product_family'] == 'Bags')],
        complements_data[(complements_data['des_product_family'] == 'Hats, scarves and gloves')],
        complements_data[(complements_data['des_product_family'] == 'Belts and Ties')],
        complements_data[(complements_data['des_product_aggregated_family'] == 'Outwear')]]

    for complement_data in complements_df:
        validComplement = False
        if not complement_data.empty:
            product = complement_data.sample()
            tries = 0
            while not validComplement:
                product = complement_data.sample()
                tries = tries + 1
                for t in types:
                    if (product[patterns[1][0]].values[0] in patterns[1][1][str(t)]
                        and (product['des_sex'].values[0] == sex or product['des_sex'].values[0] == 'Unisex'))\
                            or tries >= 8:
                        validComplement = True
                        break
                    else:
                        validComplement = False
                        break
                if tries >= 8:
                    break
            if tries < 8:
                products.append(product['cod_modelo_color'])

    return products


def add_outfit(new_products_list):
    path = 'datathon/dataset/custom_outfit_data.csv'
    custom_outfit_data = pd.read_csv(path)

    if custom_outfit_data.shape[0] > 1:
        print("filas: " + str(custom_outfit_data.shape[0]))
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


def isNewOutfit(data, lista_cod_modelo_color):
    # Agrupar por cod_outfit y verificar las combinaciones prohibidas
    grouped_df = data.groupby('cod_outfit')['cod_modelo_color'].apply(set).reset_index()

    # Verificar si hay combinaciones prohibidas en cada cod_outfit
    repeated = grouped_df['cod_modelo_color'].apply(lambda x: any(set(comb) <= x for comb in lista_cod_modelo_color))
    if len(repeated) > 0:
        return True
    else:
        return False


def main():
    outfit_data = pd.read_csv('datathon/dataset/outfit_data.csv')
    product_data = pd.read_csv('datathon/dataset/product_data.csv')
    joined_data = pd.read_csv('datathon/dataset/joined_data.csv')

    """complements_data = joined_data[
        ((joined_data['des_product_aggregated_family'] == 'Accessories') |
         (joined_data['des_product_aggregated_family'] == 'Outwear')) &
        (joined_data['des_product_family'] != 'Footwear')
        ]
    complements_data.to_csv('datathon/dataset/complements_data.csv', index=False)"""
    complements_data = pd.read_csv('datathon/dataset/complements_data.csv')

    # type of elements of one outfi
    products = []
    # Essential products: TOP, BOTTOM, FOOTWEAR
    tops_data = product_data[product_data['des_product_category'] == 'Tops']
    bottoms_data = product_data[product_data['des_product_category'] == 'Bottoms']
    products.append(bottoms_data)
    footwear_data = product_data[product_data['des_product_family'] == 'Footwear']
    products.append(footwear_data)
    # Additional products: OUTWEAR, JEWELLERY, BAGS, (HATS, SCRAVES AND GLOVES), (BELTS AND TIES)
    #jewellery_data = product_data[product_data['des_product_family'] == 'Jewellery']
    #products.append(jewellery_data)

    # declaration of patterns
    # patternDiscovery = PatternDiscovery()
    # patternDiscovery.feature_matching('des_product_type', joined_data)

    patterns = []
    color_matching = csv_to_dic("datathon/patterns/color_matching.csv", "des_agrup_color_eng", 300)
    patterns.append(["des_agrup_color_eng", color_matching])
    product_types = csv_to_dic("datathon/patterns/des_product_type_matching.csv", "des_product_type", 10)
    patterns.append(["des_product_type", product_types])

    # outfits creation
    for i in range(0, 9):
        list_outfit_products = create_outfit(tops_data, products, patterns, joined_data, complements_data)
        add_outfit(list_outfit_products)

    custom_outfit_data = pd.read_csv('datathon/dataset/custom_outfit_data.csv')
    custom_joined_data = pd.merge(custom_outfit_data, product_data, on='cod_modelo_color', how='inner')
    custom_joined_data.to_csv('datathon/dataset/custom_joined_data.csv', index=False)

    # view output
    print("Initiating viewer...")
    viewer = OutfitViewer()
    viewer.run()


if __name__ == '__main__':
    main()
