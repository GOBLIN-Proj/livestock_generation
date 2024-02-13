from livestock_generation.livestock import Cohorts
import unittest
import pandas as pd

class CohortsDataTestCase(unittest.TestCase):
    def setUp(self):
        # Create the DataFrame with the provided data


        data = [
            [0, "Dairy", "tank solid", 0, 0, 0.0879077282507005, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
            [0, "Dairy", "tank liquid", 172390.09063152, 0, 0.8, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
            [0, "Beef", "tank solid", 0, 0, 0.0879077282507005, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
            [0, "Beef", "tank liquid", 0, 27807.487070967, 0.0879077282507005, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
            [0, "Lowland sheep", "tank liquid", 0, 0, 0.0879077282507005, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 0, 0, 37812, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
            [0, "Upland sheep", "tank liquid", 0, 0, 0.0879077282507005, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 9453, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080]
        ]

        columns = ["Scenarios", "Cattle systems", "Manure management", "Dairy pop", "Beef pop", "Dairy prod", "Beef prod", "mm_storage", "Cattle EF", "AD prod", "Forest area", "Conifer proportion", "Conifer harvest", "Conifer thinned", "Broadleaf harvest", "Bioenergy area", "Crop area", "Wetland area", "Land rewetting", "Grass management", "Upland sheep pop", "Upland sheep prod", "Lowland sheep pop", "Lowland sheep prod", "Dairy Pasture fertilisation", "Beef Pasture fertilisation", "Broadleaf proportion", "Afforest Year"]
        
        self.data_frame = pd.DataFrame(data, columns=columns)
    
        self.cohorts_class = Cohorts("ireland",2020, 2050, self.data_frame)

        

    def test_cohorts_data(self):

        scenario_data = self.cohorts_class.compute_cohort_population_in_scenarios_for_year()

        print(self.cohorts_class.cohort_name_conversion(self.data_frame))

        scenario_data.to_csv("./data/scenario_cohort_data_test.csv")


if __name__ == "__main__":
    unittest.main()
