import plotly.graph_objects as go

def create_flow_chart(df):
    # Tworzymy unikalną listę węzłów
    nodes = list(set(df["source"]).union(set(df["target"])))

    # Mapowanie nazw na indeksy
    node_map = {name: i for i, name in enumerate(nodes)}

    # Tworzymy listy dla Sankeya
    source = df["source"].map(node_map).tolist()
    target = df["target"].map(node_map).tolist()
    value = df["value"].tolist()

    # **2. Rysowanie Sankeya z osobnymi kolorami**
    # Kolory dla grup (możesz zmienić według uznania)
    color_map = {
        "lojalny": "blue",
        "systematyczny": "green",
        "3 lata w bazie": "orange",
        "pozostali": "gray",
        "odcięci": "red",
        "zwrot": "yellow",
    }

    # Przypisujemy kolory do węzłów na podstawie nazw
    node_colors = [
        next((color_map[key] for key in color_map if key in name), "black") for name in nodes
    ]

    # Rysowanie diagramu Sankeya
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=nodes,
            pad=15,
            thickness=20,
            color=node_colors  # Dodanie kolorów do węzłów
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        )
    )])

    fig.update_layout(title_text="Przepływy ludzi między grupami w latach 2011-2013", font_size=10)
    return fig
