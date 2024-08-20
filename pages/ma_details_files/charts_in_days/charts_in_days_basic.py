from pages.ma_details_files.download_data_fo_char_line import down_data_sum_and_count, down_data_cost_and_circulation
class ChartsInDaysBasic:
    def __init__(self, mailing, con, years, refresh_data, engine):
        self.mailing = mailing
        self.con = con
        self.years = years
        self.refresh_data = refresh_data
        self.engine = engine
        self.data_cost_and_circulation = None
        self.data_sum_count = None

    def get_data(self):
        self.data_cost_and_circulation = down_data_cost_and_circulation(self.con, self.refresh_data, self.engine)
        self.data_sum_count = down_data_sum_and_count(self.con, self.refresh_data, self.engine)
