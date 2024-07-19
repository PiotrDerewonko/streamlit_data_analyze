from datetime import datetime

from pages.ma_details_files.choose_options import ChooseOptions


class ChooseOptionsForIntentions(ChooseOptions):
    options_gr1 = ['MAILING ADRESOWY', 'INTENCJE ŚWIĘTYCH']
    options_gr2 = ['KARDYNALSKA LUTY', 'MAILING Q1', 'MAILING Q2', 'KARDYNALSKA SIERPIEŃ',
                   'MAILING Q3 KUSTOSZ LIPIEC', 'MAILING Q3', 'MAILING Q4', 'COB-WWW', 'CENTRUM OPATRZNOŚCI']
    default_gr1 = 'INTENCJE ŚWIĘTYCH'

    def __init__(self, con):
        super().__init__(con)

    def find_last_mailing(self):
        #todo to jeszcze do przemyslenia co ma sie tu domyslnie wysiwetlac
        default_camp = 'MAILING Q2'
        current_year = datetime.now().year
        return default_camp, current_year

    def choose_options(self):
        return super().choose_options()

