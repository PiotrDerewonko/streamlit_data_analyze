import streamlit as st

def choose():
    #todo dorobic abty rok dodawal sie sam
    qamp = st.multiselect(options=['KARDYNALSKA LUTY', 'MAILING Q1', 'MAILING Q2', 'KARDYNALSKA SIERPIEŃ',
                                   'MAILING Q3 KUSTOSZ LIPIEC', 'MAILING Q3', 'MAILING Q4'],
                          label='Proszę wybrać mailing',
                          default=['KARDYNALSKA LUTY'])
    years = st.multiselect(options=['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
                                    '2018', '2019', '2020', '2021', '2022', '2023'], label='Proszę wybrać rok mailingu',
                           default=[ '2020', '2021', '2022', '2023'])
    return qamp, years