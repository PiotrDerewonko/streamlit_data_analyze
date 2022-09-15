import pandas as pd
import streamlit as st
def create_df(data_all, label, value):
    data_all[f'{label}'] = value
    print('test')