import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from OutfitViewer import OutfitViewer


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
                        and (product['des_sex'].values[0] == sex or product['des_sex'].values[0] == 'Unisex')) \
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


def create_outfit_page():
    st.subheader("Outfit Creator")

    # Inicializar el estado de la sesión
    if 'outfit_viewer' not in st.session_state:
        st.session_state.outfit_viewer = OutfitViewer(pd.read_csv('datathon/dataset/custom_joined_data.csv'))

    # Botón para mostrar el próximo outfit
    if st.button("Next"):
        st.session_state.outfit_viewer.show_next_outfit()

    # Mostrar imágenes del outfit actual en filas de 5
    current_outfit_images = st.session_state.outfit_viewer.get_current_outfit_images()
    for i in range(0, len(current_outfit_images), 5):
        images_row = current_outfit_images[i:i + 5]
        st.image(images_row)


def heat_map_visualization(data, feature):
    # Utilizar seaborn para visualizar clústeres de afinidad
    sns.set(style="white")
    st.markdown(
        """
        <style>
            .stPlot {
                width: 100%;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Utilizar una paleta de colores con transición entre 6 colores (invertida)
    cmap = sns.color_palette("viridis", as_cmap=True)
    cmap = cmap.reversed()

    # Configurar el diseño de los subgráficos
    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(data, cmap=cmap, annot=True, fmt="d", linewidths=.5, vmin=0,
                vmax=data.max().max(), ax=ax)
    ax.set_title(f"{feature} Heat Map")

    # Mostrar el gráfico
    st.pyplot(fig)


def clustering_generic(data, feature):
    # Normalizar los datos
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(data)

    # Obtener el número de clusters
    n_clusters = len(data)

    # Realizar clustering jerárquico con método de enlace completo
    clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='complete')
    labels = clustering.fit_predict(normalized_data)

    # Añadir la columna de etiquetas al DataFrame original
    data_with_labels = pd.DataFrame(data=normalized_data, columns=data.columns)
    data_with_labels['Cluster'] = labels

    # Configurar el diseño de los subgráficos
    fig, ax = plt.subplots(figsize=(12, 8))

    # Utilizar seaborn para visualizar clústeres de afinidad
    sns.set(style="white")

    # Utilizar una paleta de colores con transición entre 6 colores (invertida)
    cmap = sns.color_palette("viridis", as_cmap=True)
    cmap = cmap.reversed()

    # Añadir nombres a los puntos en el Clustering
    data_with_labels['Point'] = data.index

    # Aumentar la distancia entre puntos para mejor dispersión y aumentar el tamaño de la fuente
    sns.scatterplot(x=data_with_labels['Cluster'], y=data_with_labels['Point'],
                    hue=data_with_labels['Cluster'], palette=cmap, legend=False, s=100)

    # Anotar el texto al lado de cada punto con una fuente más grande
    for index, row in data_with_labels.iterrows():
        ax.annotate(row['Point'], (row['Cluster'], index), textcoords="offset points", xytext=(5, 0), ha='center',
                    fontsize=12)

    plt.title(f"{feature} Clustering (Complete Linkage)")
    plt.xlabel("Clusters")

    # Eliminar el texto en el eje vertical
    ax.set_yticks([])
    ax.set_yticklabels([])

    # Ajustar la disposición para mayor dispersión
    plt.tight_layout()

    # Mostrar el gráfico
    st.pyplot(fig)


def show_statistics_page():
    st.subheader("Statistics")

    if st.button("Affinity Filters - Heat Maps"):
        # Cargar los datos de afinidad desde un archivo CSV (sustituye 'ruta_del_archivo.csv' con tu ruta)
        color_data = pd.read_csv('datathon/patterns/color_matching.csv', index_col=0)
        type_data = pd.read_csv('datathon/patterns/des_product_type_matching.csv', index_col=0)
        fabric_data = pd.read_csv('datathon/patterns/fabric_matching.csv', index_col=0)

        # Llamar a la función para visualizar clústeres para cada conjunto de datos
        heat_map_visualization(color_data, 'Color')
        heat_map_visualization(fabric_data, 'Fabric')
        clustering_generic(type_data, 'Type')  # Nueva función para clustering


def main():
    product_data = pd.read_csv('datathon/dataset/product_data.csv')
    joined_data = pd.read_csv('datathon/dataset/joined_data.csv')  # product and outfit data joined

    complements_data = pd.read_csv('datathon/dataset/complements_data.csv')

    # type of elements of one outfi
    products = []
    # Essential products: TOP, BOTTOM, FOOTWEAR
    tops_data = product_data[product_data['des_product_category'] == 'Tops']
    bottoms_data = product_data[product_data['des_product_category'] == 'Bottoms']
    products.append(bottoms_data)
    footwear_data = product_data[product_data['des_product_family'] == 'Footwear']
    products.append(footwear_data)

    # declaration of patterns
    # patternDiscovery = PatternDiscovery()
    # patternDiscovery.color_matching()
    # patternDiscovery.fabric_matching()

    patterns = []
    color_matching = csv_to_dic("datathon/patterns/color_matching.csv", "des_agrup_color_eng", 300)
    patterns.append(["des_agrup_color_eng", color_matching])
    product_types = csv_to_dic("datathon/patterns/des_product_type_matching.csv", "des_product_type", 10)
    patterns.append(["des_product_type", product_types])
    fabric_matching = csv_to_dic("datathon/patterns/fabric_matching.csv", "des_fabric", 1000)
    patterns.append(["des_fabric", fabric_matching])

    # outfits creation
    for i in range(0, 9):
        list_outfit_products = create_outfit(tops_data, products, patterns, joined_data, complements_data)
        add_outfit(list_outfit_products)

    custom_outfit_data = pd.read_csv('datathon/dataset/custom_outfit_data.csv')
    custom_joined_data = pd.merge(custom_outfit_data, product_data, on='cod_modelo_color', how='inner')
    custom_joined_data.to_csv('datathon/dataset/custom_joined_data.csv', index=False)

    st.set_page_config(
        page_title="Affinity Mango Wardrobe",
        page_icon="👚",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.title("Affinity Mango Wardrobe")

    # Página de inicio con dos botones
    selected_option = st.sidebar.radio("Select an option", ["Create Outfit", "Show Statistics"])

    if selected_option == "Create Outfit":
        create_outfit_page()
    elif selected_option == "Show Statistics":
        show_statistics_page()


if __name__ == '__main__':
    main()
