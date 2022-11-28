import pandas as pd
#from matplotlib import pyplot as plt
#test = pd.read_csv('./pages/ma_details_files/tmp_file/people_camp_pay.csv')
#test_pt = test.pivot_table(values='id_korespondenta', index=['grupa_akcji_2_wplaty', 'grupa_akcji_3_wplaty'], aggfunc='count')
#test_pt.plot()
#plt.show()
#plt.close()
#print(test_pt)

import plotly.express as px
#data_canada = px.data.gapminder().query("country == 'Canada'")
test = pd.read_csv('./pages/ma_details_files/tmp_file/people_camp_pay.csv')
test_pt = test.pivot_table(values='id_korespondenta', index=['grupa_akcji_2_wplaty', 'grupa_akcji_3_wplaty'], aggfunc='count')
fig = px.bar(test_pt, x=['grupa_akcji_2_wplaty', 'grupa_akcji_3_wplaty'], y='id_korespondenta')
fig.show()
