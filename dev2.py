import pandas as pd
import streamlit as st

# Przykładowy DataFrame
data = {
    "Czy ma książkę XYZ": ["tak", "nie", "tak", "nie", "tak"],
    "Ile książek ma łącznie": [0, 1, 2, 3, 4],
    "Ulubiony gatunek": ["fantasy", "sci-fi", "kryminał", "fantasy", "sci-fi"]
}
df = pd.DataFrame(data)

# Inicjalizacja session state
if "selected_column" not in st.session_state:
    st.session_state["selected_column"] = " "
if "selected_values" not in st.session_state:
    st.session_state["selected_values"] = []

# Lista opcji z domyślną wartością
column_options = [" "] + list(df.columns)

# Wybór kolumny
selected_column = st.selectbox("Wybierz kolumnę do filtrowania", column_options, index=0)

# Jeśli użytkownik wybrał kolumnę, wyświetlamy multiselect
if selected_column != " ":
    if selected_column != st.session_state["selected_column"]:
        st.session_state["selected_column"] = selected_column
        st.session_state["selected_values"] = []  # Reset wyboru

    # Pobranie unikalnych wartości dla wybranej kolumny
    options = df[selected_column].unique().tolist()

    # Multiselect z dynamicznymi opcjami
    selected_values = st.multiselect("Wybierz wartości", options, default=st.session_state["selected_values"])
    st.session_state["selected_values"] = selected_values

    # Wynikowy słownik filtrów
    filters = {selected_column: selected_values}
    st.write("Zastosowane filtry:", filters)
