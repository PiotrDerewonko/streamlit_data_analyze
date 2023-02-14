import streamlit as st


def label_orientations():
    with st.container():
        c1, c2, c3 = st.columns(3)
        options = ['vertical', 'horizontal', 3.14/4, -3.14/4]
        list_of_objects = [['major', 'vertical'], ['group', 'vertical'], ['sub_group', 'vertical']]
        for x in list_of_objects:
            if x[0] not in st.session_state:
                st.session_state[x[0]] = x[1]
        dict_of_oriantation = {'major': 'vertical', 'group': 'vertical', 'sub_group': 'vertical' }
        def change_dict(x, y):
            dict_of_oriantation[x] = y
        with c1:
            select_axis = st.selectbox('Orientacja dla głównej etykiet', options=options,
                                       on_change=change_dict("major", st.session_state.major),
                                       key="major")
        with c2:
            select_axis = st.selectbox('Orientacja dla grupy etykiet', options=options,
                                       on_change=change_dict("group", st.session_state.group),
                                       key="group")
        with c3:
            select_axis = st.selectbox('Orientacja dla sub grupy etykiet', options=options,
                                       on_change=change_dict("sub_group", st.session_state.sub_group),
                                       key="sub_group")
        return dict_of_oriantation

