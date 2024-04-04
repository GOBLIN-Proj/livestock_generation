import unittest
import os
from tempfile import TemporaryDirectory
from livestock_generation.livestock import AnimalData
from livestock_generation.livestock_exports import Exports
import pandas as pd
import os

class TestGenerateData(unittest.TestCase):
    def test_generate_scenario_dataframe_creates_file(self):
        # Use a temporary directory
        with TemporaryDirectory() as tmp_dir:
            path = "./data" 
            baseline_year = 2020
            target_year = 2050
            ef_country = "ireland"

            scenario_dataframe = pd.read_csv(os.path.join(path, "scenario_input_dataframe.csv"))

            # create classes for the generation of animal data and livestock ouput data
            animal_class = AnimalData(ef_country, baseline_year, target_year, scenario_dataframe)
            export_class = Exports(ef_country, baseline_year, target_year, scenario_dataframe)

            baseline_data_file_name = "baseline_data.csv"
            scenario_data_file_name = "scenario_data.csv"
            beef_outputs_file_name = "beef_outputs.csv"
            dairy_outputs_file_name = "dairy_outputs.csv"
            protein_outputs_file_name = "protein_outputs.csv"

            baseline_expected_file_path = os.path.join(tmp_dir, baseline_data_file_name)
            scenario_expected_file_path = os.path.join(tmp_dir, scenario_data_file_name)
            beef_expected_file_path = os.path.join(tmp_dir, beef_outputs_file_name)
            dairy_expected_file_path = os.path.join(tmp_dir, dairy_outputs_file_name)
            protein_expected_file_path = os.path.join(tmp_dir, protein_outputs_file_name)

            # create dataframe for baseline year animals
            baseline_data = animal_class.create_baseline_animal_dataframe()

            baseline_data.to_csv(baseline_expected_file_path)

            # create dataframe for scenarios animals
            scenario_data = animal_class.create_animal_dataframe()
            
            scenario_data.to_csv(scenario_expected_file_path)

            # Create dataframes for beef and milk output
            export_class.compute_system_protien_exports(scenario_data, baseline_data).to_csv(beef_expected_file_path)

            export_class.compute_system_milk_exports(scenario_data, baseline_data).to_csv(dairy_expected_file_path)

            export_class.compute_system_total_protein_exports(scenario_data, baseline_data).to_csv(protein_expected_file_path)

            # Check if the file was created as expected

            self.assertTrue(os.path.exists(baseline_expected_file_path), f"File {baseline_data_file_name} was not created in temporary directory.")

            self.assertTrue(os.path.exists(scenario_expected_file_path), f"File {scenario_data_file_name} was not created in temporary directory.")

            self.assertTrue(os.path.exists(beef_expected_file_path), f"File {beef_outputs_file_name} was not created in temporary directory.")

            self.assertTrue(os.path.exists(dairy_expected_file_path), f"File {dairy_outputs_file_name} was not created in temporary directory.")

            self.assertTrue(os.path.exists(protein_expected_file_path), f"File {protein_outputs_file_name} was not created in temporary directory.")


# Running the tests
if __name__ == '__main__':
    unittest.main()

