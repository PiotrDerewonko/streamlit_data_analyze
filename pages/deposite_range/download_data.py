import pandas as pd

from pages.ma_details_files.data_about_people_and_campaign_pay import data_pay_all


def download_data(deposite_range, year_range, year_range_to_analize, con, refresh_data) -> pd.DataFrame:
    '''Funkcja ma za zadanie pobrac i odfiltrowac dane. W pierwszym kroku znajduje id osob ktore w podanym czasie
    dokonaly choc jednej wplaty w wybranym przedziale. W drugim, filtruje df tylko z osobami znalezionymi
    w kroku 1 i we wskaznym przez uzytkownika czasie'''
    data_about_pay_all = data_pay_all(con, refresh_data)
    data_filtered_id_kor = data_about_pay_all['id_korespondenta'].loc[
        (data_about_pay_all['grupa_akcji_3_wplaty'] >= year_range[0]) &
        (data_about_pay_all['grupa_akcji_3_wplaty'] <= year_range[1]) &
        (data_about_pay_all['przedzialy'] == deposite_range)].drop_duplicates().to_frame()
    data_filtered_id_kor['tmp_column'] = 'do_analizy'
    data_filtered_year = data_about_pay_all.loc[
        (data_about_pay_all['grupa_akcji_3_wplaty'] >= year_range_to_analize[0]) &
        (data_about_pay_all['grupa_akcji_3_wplaty'] <= year_range_to_analize[1])]
    data_to_return = pd.merge(data_filtered_year, data_filtered_id_kor, how='left', on='id_korespondenta').dropna(
        subset='tmp_column')
    return data_to_return


def create_pivot_table(data, index_for_pivot) -> pd.DataFrame:
    '''Funkcja ma za zadanie zwrocic tabele przestawna oraz slownik niezbedny do stworzenia wykresow '''
    pivot_table = pd.pivot_table(data, index=index_for_pivot, columns='przedzialy', values='id_korespondenta',
                                 aggfunc='count')
    return pivot_table
