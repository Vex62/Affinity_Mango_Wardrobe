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


def cluster_outfits(data):
    # Supongamos que tienes un DataFrame llamado 'dataset' con las columnas 'cod_outfit', 'producto', 'color', 'talla', y otras columnas.
    # Reemplaza esto con tu propio DataFrame
    dataset = pd.DataFrame(data)

    # Seleccionar características relevantes (en este caso, solo 'color' y 'talla')
    X = dataset[['des_color_specification_esp', 'des_fabric']]

    # Codificar variables categóricas a valores numéricos
    X_encoded = pd.get_dummies(X)

    # Escalar las características para que todas tengan la misma importancia
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_encoded)

    # Aplicar el algoritmo DBSCAN
    dbscan = DBSCAN(eps=0.5, min_samples=2)  # Puedes ajustar los parámetros según tus necesidades
    dataset['cluster'] = dbscan.fit_predict(X_scaled)

    # Visualizar los clusters
    sns.scatterplot(x=X_scaled[:, 0], y=X_scaled[:, 1], hue=dataset['cluster'], palette='viridis', s=100)
    plt.title('Clusters de prendas compatibles')
    plt.xlabel('Color (escala)')
    plt.ylabel('Fabric (escala)')
    plt.legend(title='Cluster')
    plt.show()


def create_outfit(tops_data, bottoms_data, footwear_data):
    top = tops_data.sample()
    bottom = bottoms_data.sample()
    footwear = footwear_data.sample()
    """color = top['des_color_specification_esp'].values[0]
    print("color: ", color)
    if len(bottoms_data[bottoms_data['des_color_specification_esp'] == color]) > 0:
        bottom = bottoms_data[bottoms_data['des_color_specification_esp'] == color].sample()
    else:
        bottom = bottoms_data.sample()
    footwear = footwear_data.sample()"""
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


def main():
    outfit_data = pd.read_csv('datathon/dataset/outfit_data.csv')
    product_data = pd.read_csv('datathon/dataset/product_data.csv')
    joined_data = pd.read_csv('datathon/dataset/joined_data.csv')

    """joined_data = pd.merge(outfit_data, product_data, on='cod_modelo_color', how='inner')
    joined_data = joined_data.sort_values(by='cod_outfit')
    joined_data.to_csv('datathon/dataset/joined_data.csv', index=False)"""

    tops_data = product_data[product_data['des_product_category'] == 'Tops']
    bottoms_data = product_data[product_data['des_product_category'] == 'Bottoms']
    footwear_data = product_data[product_data['des_product_family'] == 'Footwear']

    for i in range(0,9):
        list_outfit_products = create_outfit(tops_data, bottoms_data, footwear_data)
        add_outfit(list_outfit_products)

    custom_outfit_data = pd.read_csv('datathon/dataset/custom_outfit_data.csv')
    custom_joined_data = pd.merge(custom_outfit_data, product_data, on='cod_modelo_color', how='inner')
    custom_joined_data.to_csv('datathon/dataset/custom_joined_data.csv', index=False)

    patternDiscovery = PatternDiscovery()
    patternDiscovery.color_matching()

    viewer = OutfitViewer()
    viewer.run()


if __name__ == '__main__':
    main()
