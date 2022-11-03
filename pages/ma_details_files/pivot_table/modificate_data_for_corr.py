def modificate_data_for_corr(data, column_options):
    for i in column_options:
        tmp = data[i].drop_duplicates()
        for j, row in tmp.iterrows():
            pass
        #todo dokonczyc automatyczna zmiane wszystkich kolumn poza suma i liczba wplat, dodac sprawdzenie czy nie jest liczba