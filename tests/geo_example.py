from geo_livestock_generation.geo_livestock import AnimalData
from geo_livestock_generation.geo_livestock_exports import Exports
import pandas as pd
import os

def main():
    # Create the DataFrame with the provided data, this represents scenario inputs
    path = "./geo_data/"

    scenario_dataframe = pd.read_csv(os.path.join(path, "scenario_input_dataframe.csv"))

    # create additional parameters
    baseline_year = 2020
    target_year = 2050
    ef_country = "ireland"

    # create classes for the generation of animal data and livestock ouput data
    animal_class = AnimalData(ef_country, baseline_year, target_year, scenario_dataframe)
    export_class = Exports(ef_country, baseline_year, target_year, scenario_dataframe)

    # create dataframe for baseline year animals
    baseline_data = animal_class.create_baseline_animal_dataframe()

    # create dataframe for scenarios animals
    scenario_data = animal_class.create_animal_dataframe()

    scenario_data.to_csv("./data/example_scenario_animal_data_test.csv")

    # Create dataframes for beef and milk output
    beef_outputs = export_class.compute_system_protien_exports(scenario_data, baseline_data)

    dairy_outputs = export_class.compute_system_milk_exports(scenario_data, baseline_data)

    protein_outputs = export_class.compute_system_total_protein_exports(scenario_data, baseline_data)

    # Print generated data
    print(baseline_data)

    baseline_data.to_csv("./geo_data/past_animals.csv")

    print(scenario_data)

    scenario_data.to_csv("./geo_data/future_animals.csv")

    print(beef_outputs)

    print(dairy_outputs)

    print(protein_outputs)


if __name__ == "__main__":
    main()