from livestock_generation.livestock import AnimalData
from livestock_generation.livestock_exports import Exports
import pandas as pd


def main():
    # Create the DataFrame with the provided data, this represents scenario inputs
    data = [
        [0, "Dairy", "tank solid", 0, 0, 0, 0, 0, 0, 0, 0.801458098547012,
         0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0,
         0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
        [0, "Dairy", "tank liquid", 1555000, 0, 0, 0, 0, 0, 0, 0.801458098547012,
         0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0,
         0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
        [0, "Beef", "tank solid", 0, 0, 0, 0, 0, 0, 0, 0.801458098547012,
         0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0,
         0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
        [0, "Beef", "tank liquid", 0, 915000, 0, 0, 0, 0, 0,
         0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073,
         0.120049095269181, 0, 0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221,
         2080],
        [0, "Lowland sheep", "tank liquid", 0, 0, 0, 0, 0, 0, 0, 0.801458098547012,
         0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0,
         0.0879200186051467, 0, 0, 2045000, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
        [0, "Upland sheep", "tank liquid", 0, 0, 0, 0, 0, 0, 0, 0.801458098547012,
         0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0,
         0.0879200186051467, 511000, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080]
    ]

    columns = ["Scenarios", "Cattle systems", "Manure management", "Dairy pop", "Beef pop", "Dairy prod", "Beef prod",
               "mm_storage", "Cattle EF", "AD prod", "Forest area", "Conifer proportion", "Conifer harvest",
               "Conifer thinned", "Broadleaf harvest", "Bioenergy area", "Crop area", "Wetland area", "Land rewetting",
               "Grass management", "Upland sheep pop", "Upland sheep prod", "Lowland sheep pop", "Lowland sheep prod",
               "Dairy Pasture fertilisation", "Beef Pasture fertilisation", "Broadleaf proportion", "Afforest Year"]

    scenario_dataframe = pd.DataFrame(data, columns=columns)

    # create additional parameters
    baseline_year = 2018
    target_year = 2050
    ef_country = "ireland"

    # create classes for the generation of animal data and livestock ouput data
    animal_class = AnimalData(ef_country, baseline_year, target_year, scenario_dataframe)
    export_class = Exports(ef_country, baseline_year, target_year, scenario_dataframe)

    # create dataframe for baseline year animals
    baseline_data = animal_class.create_baseline_animal_dataframe()

    # create dataframe for scenarios animals
    scenario_data = animal_class.create_animal_dataframe()

    # Create dataframes for beef and milk output
    beef_outputs = export_class.compute_system_protien_exports(scenario_data, baseline_data)

    dairy_outputs = export_class.compute_system_milk_exports(scenario_data, baseline_data)

    protein_outputs = export_class.compute_system_total_protein_exports(scenario_data, baseline_data)

    # Print generated data
    print(baseline_data)

    print(scenario_data)

    print(beef_outputs)

    print(dairy_outputs)

    print(protein_outputs)


if __name__ == "__main__":
    main()
