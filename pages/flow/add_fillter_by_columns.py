import streamlit as st


class AddFillterByColumns:
    def __init__(self, df, selected_columns, selected_values, dictionary_with_options, filtr_title):
        self.df = df
        self.selected_columns = selected_columns
        self.selected_values = selected_values
        self.dictionary_with_options = dictionary_with_options
        self.filtr_title = filtr_title

    def init_session_state(self):

        # Inicjalizacja session state
        if self.selected_columns not in st.session_state:
            st.session_state[f"{self.selected_columns}"] = " "
        if self.selected_values not in st.session_state:
            st.session_state[f"{self.selected_values}"] = []

    def add_fillter_by_columns(self):

        # Lista opcji z domyślną wartością
        column_options = [" "] + list(self.df.columns)

        # Wybór kolumny
        selected_column = st.selectbox(f"{self.filtr_title}", column_options, index=0)

        # Jeśli użytkownik wybrał kolumnę, wyświetlamy multiselect
        if selected_column != " ":
            if selected_column != st.session_state[f"{self.selected_columns}"]:
                st.session_state[f"{self.selected_columns}"] = selected_column
                st.session_state[f"{self.selected_values}"] = []  # Reset wyboru

            # Pobranie unikalnych wartości dla wybranej kolumny
            options = self.df[selected_column].unique().tolist()

            # Multiselect z dynamicznymi opcjami
            selected_values = st.multiselect("Wybierz wartości", options,
                                             default=st.session_state[f"{self.selected_values}"])
            st.session_state[f"{self.selected_values}"] = selected_values

            # Wynikowy słownik filtrów
            # filters = {selected_column: selected_values}
            self.dictionary_with_options[selected_column] = selected_values

        return self.dictionary_with_options
