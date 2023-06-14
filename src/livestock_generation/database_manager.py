import sqlalchemy as sqa
import pandas as pd
from livestock_generation.database import get_local_dir
import os


class DataManager:
    def __init__(self):
        self.database_dir = get_local_dir()
        self.engine = self.data_engine_creater()

    def data_engine_creater(self):
        database_path = os.path.abspath(
            os.path.join(self.database_dir, "livestock_database.db")
        )
        engine_url = f"sqlite:///{database_path}"

        return sqa.create_engine(engine_url)
    

    def get_concentrate_per_animal_dataframe(self, ef_country):
        table = "concentrate_amounts_per_unit_output"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, ef_country),
            self.engine,
            index_col=["ef_country"],
        )

        return dataframe



    def get_weight_gain_cattle(self, ef_country):

        table = "animal_features_data"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, ef_country),
            self.engine,
            index_col=["ef_country"],
        )

        return dataframe
    

    def get_weight_gain_sheep(self, ef_country):

        table = "sheep_animal_features_data"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, ef_country),
            self.engine,
            index_col=["ef_country"],
        )

        return dataframe
    
    
    def get_cattle_herd_data(self):

        table = "2012_to_2020_herd_numbers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        dataframe.iloc[: ,1:] *= 1000
        
        return dataframe


    def get_parameter_data(self, ef_country):
        table = "param_data"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, ef_country),
            self.engine,
            index_col=["ef_country"],
        )


        return dataframe