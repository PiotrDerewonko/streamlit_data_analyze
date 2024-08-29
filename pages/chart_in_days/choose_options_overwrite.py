from typing import List

from pages.ma_details_files.choose_options import ChooseOptions


class ChooseOptionsOverwrite(ChooseOptions):
    def find_years(self, current_year, count_return_elements=-1) -> List[int]:
        return super().find_years(current_year, -1)