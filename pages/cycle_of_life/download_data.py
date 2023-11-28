import datetime

import pandas as pd

from pages.cycle_of_life.add_corr import (download_correspondent_data, download_pay_data, download_mailings,
                                          download_good_adress, modificate_data)


def download_data_cycle_of_life(con, refresh_data, engine) -> pd.DataFrame:
    if refresh_data == 'True':
        aktualny_rok = int(datetime.datetime.now().year)
        data_all = pd.DataFrame()
        data_all = download_correspondent_data(con, aktualny_rok, data_all)
        data_all = download_pay_data(con, data_all, aktualny_rok)
        data_all = download_mailings(con, data_all, aktualny_rok)
        data_all = download_good_adress(con, data_all)
        data_all = modificate_data(data_all)
        pass
