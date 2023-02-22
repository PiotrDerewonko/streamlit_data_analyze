#from geopy.geocoders import Nominatim

#geolocator = Nominatim(user_agent="my_app")
#location = geolocator.geocode("Warszawa lwowska 15")
#print((location.latitude, location.longitude))


import pandas as pd
import pydeck as pdk
import streamlit as st

df = pd.DataFrame(data={'latitude': [52.30739130000000, 52.22207805], 'longitude':[21.164590055417932, 21.01236116061687], 'etykieta': ['20','1']})

etykiety = df.etykieta.unique().tolist()
kolory = ['#00FF00', '#FF0000'] # Lista kolorów odpowiadających kolejnym etykietom
layer = [pdk.Layer(
    "ScatterplotLayer",
    data=df[:1],
    get_position=["longitude", "latitude"],
    get_fill_color=['200'],
    get_radius=100,
), pdk.Layer(
    "ScatterplotLayer",
    data=df[1:],
    get_position=["longitude", "latitude"],
    get_fill_color=['1'],
    get_radius=100,
)]
view_state = pdk.ViewState(latitude=df.latitude.mean(), longitude=df.longitude.mean(), zoom=8, bearing=0, pitch=0)
tooltip = {"html": "<b>Etykieta:</b> {etykieta}<br />", "style": {"color": "red"}}
map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer], tooltip=tooltip)
st.pydeck_chart(map)