from livestock_generation.database_manager import DataManager



class Loader:
    def __init__(self, ef_country):
        self.dataframes = DataManager()
        self.ef_country = ef_country


    def concentrate_per_animal_dataframe(self):
        return self.dataframes.get_concentrate_per_animal_dataframe(self.ef_country)


    def weight_gain_cattle(self):
        return self.dataframes.get_weight_gain_cattle(self.ef_country)
    

    def weight_gain_sheep(self):
        return self.dataframes.get_weight_gain_sheep(self.ef_country)
    

    def cattle_herd_data(self):
        return self.dataframes.get_cattle_herd_data()
    

    def parameter_data(self):
        return self.dataframes.get_parameter_data(self.ef_country)
    

