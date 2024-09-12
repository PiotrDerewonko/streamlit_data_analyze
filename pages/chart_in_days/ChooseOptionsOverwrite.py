from pages.ma_details_files.choose_options import ChooseOptions


class ChooseOptionsOverwrite(ChooseOptions):

    def choose_options(self, count_of_years=-1):
        return super().choose_options(count_of_years)
