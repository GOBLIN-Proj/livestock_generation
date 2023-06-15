from livestock_generation.data_loader import Loader
from livestock_generation.livestock_data_manager import DataManager
import pandas as pd
import numpy as np

    
class Cohorts:
    def __init__(self, ef_country, calibration_year, target_year, scenario_inputs_df):
        self.scenario_inputs_df = scenario_inputs_df
        self.loader_class = Loader(ef_country)
        self.data_manager_class = DataManager(ef_country, calibration_year, target_year, scenario_inputs_df)
        self.calibration_year = calibration_year


    def generate_cohorts_dictionary(self):

        data_frame = self.loader_class.cattle_herd_data()

        cohort_output = {}

        for _, row in data_frame.iterrows():

            cohort = row.get(str("Cohorts"))

            if cohort not in cohort_output.keys():

                cohort_output[cohort] = (
                    row[1:] 
                )

            else:

                cohort_output[cohort] += (
                    row[1:] 
                )
    
        return cohort_output


    def generate_baseline_cohorts_dictionary(self):
        calibration_year = str(self.calibration_year)
        default_calibration_year = str(self.data_manager_class.default_calibration_year)

        data_frame = self.loader_class.cattle_herd_data()
        cohort_output = {}

        for _, row in data_frame.iterrows():
            cohort = row.get(str("Cohorts"))

            try:
                cohort_output[cohort] = row[calibration_year]
            except KeyError:
                cohort_output[cohort] = row[default_calibration_year]

        return cohort_output

        
    def cohort_name_conversion(self, df):
        
        column_name_dict = self.data_manager_class.cohort_name_conversion_dict

        df = df.rename(columns=column_name_dict)
    
        return df


    def compute_coef_cohort_population(self):
        """
        sums the beef and dairy adult population. The individual cohorts are divided
        by the result to give the cohort coef.
        """
        cohort_dict = self.generate_baseline_cohorts_dictionary()

        coef ={}

        herd_relation_dict = self.data_manager_class.HERD_RELATION
        systems = self.data_manager_class.systems

        for sys in systems:   
            for cohort in herd_relation_dict[sys].keys():

                coef[cohort] = cohort_dict[cohort] / np.sum(
                    [cohort_dict[i] for i in herd_relation_dict[sys][cohort]], axis=0
                )
    
        return coef
    

    def compute_cohort_population_in_scenarios_for_year(self):

        cohort_list =[]
        cohort_list.extend(self.data_manager_class.COHORTS_DICT["Cattle"])
        cohort_list.extend(self.data_manager_class.COHORTS_DICT["Sheep"])

        herd_relation_dict = self.data_manager_class.HERD_RELATION
        systems = self.data_manager_class.systems
        
        scenario_df = self.cohort_name_conversion(self.scenario_inputs_df)

        scenario_herd = pd.DataFrame(columns=cohort_list)
        
        coef =self.compute_coef_cohort_population()

        for sys in systems:
            for cohort in cohort_list:
                try:
                    if cohort in herd_relation_dict[sys].keys():
                        
                        scenario_herd[cohort] = np.sum(
                            [
                                np.mean(coef[cohort]) * scenario_df[i]
                                for i in herd_relation_dict[sys][cohort]
                            ],
                            axis=0,
                        )

                    else:
                        
                        scenario_herd[cohort] = scenario_df[cohort]
                except KeyError:
                    continue
   
            
        scenario_herd["Scenarios"] = scenario_df["Scenarios"]
            
        return scenario_herd
    

    def compute_cohort_population_in_baseline(self):

        cohort_list =[]
        cohort_list.extend(self.data_manager_class.COHORTS_DICT["Cattle"])
        cohort_list.extend(self.data_manager_class.COHORTS_DICT["Sheep"])

        calibration_year = self.calibration_year
        
        baseline_herd = pd.DataFrame(index = [calibration_year], columns=cohort_list)
        
   
        baseline_dict =self.generate_baseline_cohorts_dictionary()

        
        for cohort in cohort_list:
            baseline_herd.loc[calibration_year,cohort] = baseline_dict[cohort]
                    
            
        return baseline_herd
    

class AnimalData:
    def __init__(self, ef_country, calibration_year, target_year, scenario_inputs_df):

        self.scenario_inputs_df = scenario_inputs_df
        self.loader_class = Loader(ef_country)
        self.data_manager_class = DataManager(ef_country, calibration_year, target_year, scenario_inputs_df)
        self.cohorts_class = Cohorts(ef_country, calibration_year, target_year, scenario_inputs_df)
        self.target_year = target_year
        self.calibration_year = calibration_year
        self.ef_country = ef_country


    def get_element_from_productivity(self,
        lca_parameter_name,
        goblin_parameter_name,
        coef_for_parameter_from_scenario,
    ):

        parameter_data_base = self.loader_class.parameter_data()

        lca_parameter_mask = parameter_data_base["LCAparameter"] == lca_parameter_name
        goblin_parameter_mask = parameter_data_base["Goblinparameter"].str.contains(
            goblin_parameter_name
        )

        parameter_output = (
            float(
                parameter_data_base.loc[
                    lca_parameter_mask & goblin_parameter_mask, "Min"
                ].values[0]
            )
            + (
                float(
                    parameter_data_base.loc[
                        lca_parameter_mask & goblin_parameter_mask, "Max"
                    ].values[0]
                )
                - float(
                    parameter_data_base.loc[
                        lca_parameter_mask & goblin_parameter_mask, "Min"
                    ].values[0]
                )
            )
            * coef_for_parameter_from_scenario
        )

        return parameter_output


    def compute_concentrate(self, cohort, milk, weight):
        """
        Computation of concentrate requirement for cattle. Constant value assumed for sheep_models.
        """
        con_dict = self.data_manager_class.COHORTS_CONCENTRATE
        df = self.loader_class.concentrate_per_animal_dataframe()
        ef_country = self.ef_country

        if cohort == "dairy_cows":
            return milk * df.loc[ef_country, "dairy_kg_con_per_kg_milk"]

        if cohort in con_dict["FEED"]:
            return 1

        if cohort in con_dict["NO_FEED"]:
            return 0

        return df.loc[ef_country, "total_dry_cow_concentrate_kg_per_LU"] / weight

    

    def create_animal_dataframe(self):

        scenario_data_frame = self.scenario_inputs_df
        cohort_dict = self.data_manager_class.COHORTS_DICT
        cohort_name_dict = self.data_manager_class.COHORT_NAME_DICT
        target_year = self.target_year
        herd_data_frame = self.cohorts_class.compute_cohort_population_in_scenarios_for_year()

        weight_gain_cattle = self.loader_class.weight_gain_cattle()
        weight_gain_sheep = self.loader_class.weight_gain_sheep()

        sheep_system_dict = self.data_manager_class.sheep_system_dict

        cattle_cohort_time_indoors_2015 = self.data_manager_class.COHORT_TIME_INDOORS

        systems = self.data_manager_class.systems
        cattle_systems = self.data_manager_class.cattle_systems
        sheep_systems = self.data_manager_class.sheep_systems
        cohort_weight = self.data_manager_class.CATTLE_COHORT_WEIGHT

        productivity_mapping = self.data_manager_class.ANIMAL_SYSTEM_MAPPING 
        system_params = self.data_manager_class.system_parameters

        ef_country = self.ef_country


        data = pd.DataFrame()

        new_index = 0

        for animal_type in systems:

            if animal_type == "Cattle":
                animal_name_list = cattle_systems
            else:
                animal_name_list = sheep_systems

            index_to_mask = scenario_data_frame["Cattle systems"].isin(animal_name_list)

            for index, row in scenario_data_frame.loc[index_to_mask, :].iterrows():

                if row["Cattle systems"] in cattle_systems:
                    animal_type = "Cattle"
                elif "sheep" in row["Cattle systems"]:
                    animal_type = "Sheep"

                for animal_category in cohort_dict[animal_type]:
                    for animal_system, productivity in productivity_mapping.items():
                        if animal_system in row["Cattle systems"]:
                            animal_system_for_productivity = productivity
                            break

                    data.loc[new_index, "ef_country"] = ef_country
                    data.loc[new_index, "farm_id"] = index
                    data.loc[new_index, "Scenarios"] = row["Scenarios"]
                    data.loc[new_index, "year"] = target_year
                    data.loc[new_index, "cohort"] = cohort_name_dict[
                        animal_category
                    ]
                    data.loc[new_index, "pop"] = herd_data_frame.loc[
                        index, animal_category
                    ]

                    # Colm changed
                    if data.loc[new_index, "cohort"] == "dairy_cows":
                        data.loc[
                            new_index, "daily_milk"
                        ] = self.get_element_from_productivity(
                            "daily_milk",
                            row["Cattle systems"],
                            scenario_data_frame.loc[
                                index, animal_system_for_productivity
                            ]
                        )
                    elif data.loc[new_index, "cohort"] == "suckler_cows":
                        data.loc[
                            new_index, "daily_milk"
                        ] = (
                            self.data_manager_class.suckler_daily_milk_baseline
                        )  # equates to 515 kg milk per year
                    else:
                        data.loc[new_index, "daily_milk"] = 0

                    if animal_type == "Cattle":
                        #Weights
                        weight_col = cohort_weight[data.loc[new_index, "cohort"]]["weight_column"]
                        weight_gain = weight_gain_cattle.loc[ef_country, weight_col]

                        if cohort_weight[data.loc[new_index, "cohort"]]["mature"]:
                            weight = weight_gain
                        elif cohort_weight[data.loc[new_index, "cohort"]]["more_than_2_years"]:
                            weight = weight_gain_cattle.loc[ef_country, "birth_weight"] + (weight_gain * 365) / 2
                        else:
                            weight = weight_gain_cattle.loc[ef_country, "birth_weight"] + (weight_gain * 365)

                        data.loc[new_index, "weight"] = weight
                    else:
                        weight_col = cohort_weight[data.loc[new_index, "cohort"]]["weight_column"]
                        weight_gain = weight_gain_sheep.loc[ef_country, weight_col]
                        if cohort_weight[data.loc[new_index, "cohort"]]["mature"]:
                            weight = weight_gain
                        else: 
                            weight = weight_gain_sheep.loc[ef_country, "lamb_weight_at_birth"] + weight_gain

                        data.loc[new_index, "weight"] = weight



                    data.loc[new_index, "forage"] = system_params[animal_type]["forage"]

                    if animal_type == "Cattle":
                        data.loc[new_index, "grazing"] = system_params[animal_type]["grazing"]
                    else:
                        data.loc[new_index, "grazing"] = (
                            sheep_system_dict[animal_category.split(" ")[0]] + system_params[animal_type]["grazing"]
                        )
                    data.loc[new_index, "con_type"] = system_params[animal_type]["con_type"]

                    if animal_type == "Sheep":
                        data.loc[new_index, "con_amount"] = system_params[animal_type]["concentrate"]
                        data.loc[new_index, "wool"] = system_params[animal_type]["wool"]

                    elif animal_type == "Cattle":

                        con_amount = self.compute_concentrate(
                            data.loc[new_index, "cohort"],
                            data.loc[new_index, "daily_milk"],
                            data.loc[new_index, "weight"],
                        )
                        data.loc[new_index, "con_amount"] = con_amount
                        data.loc[new_index, "wool"] = 0

                    if animal_type == "Cattle":
                        if (
                            data.loc[new_index, "cohort"]
                            in cattle_cohort_time_indoors_2015["t_indoors"].keys()
                        ):
                            data.loc[
                                new_index, "t_outdoors"
                            ] = cattle_cohort_time_indoors_2015["t_outdoors"][
                                data.loc[new_index, "cohort"]
                            ]
                            data.loc[
                                new_index, "t_indoors"
                            ] = cattle_cohort_time_indoors_2015["t_indoors"][
                                data.loc[new_index, "cohort"]
                            ]
                            data.loc[new_index, "t_stabled"] = 0
                    else:
                        data.loc[
                            new_index, "t_outdoors"
                        ] = self.get_element_from_productivity(
                            "t_outdoors",
                            row["Cattle systems"],
                            scenario_data_frame.loc[
                                index, animal_system_for_productivity
                            ],
                        )
                        data.loc[
                            new_index, "t_indoors"
                        ] = self.get_element_from_productivity(
                            "t_indoors",
                            row["Cattle systems"],
                            scenario_data_frame.loc[
                                index, animal_system_for_productivity
                            ],
                        )
                        data.loc[
                            new_index, "t_stabled"
                        ] = self.get_element_from_productivity(
                            "t_stabled",
                            row["Cattle systems"],
                            scenario_data_frame.loc[
                                index, animal_system_for_productivity
                            ],
                        )

                    if animal_type == "Sheep":
                        data.loc[new_index, "mm_storage"] = system_params[animal_type]["manure_management"]
                    else:
                        data.loc[new_index, "mm_storage"] = row.iloc[2]

                    data.loc[new_index, "daily_spreading"] = system_params[animal_type]["daily_spread"]
                    data.loc[new_index, "n_sold"] = 0
                    data.loc[new_index, "n_bought"] = 0

                    new_index += 1
        return data


    def create_baseline_animal_dataframe(self):

        cohort_dict = self.data_manager_class.COHORTS_DICT
        cohort_name_dict = self.data_manager_class.COHORT_NAME_DICT

        calibration_year = self.calibration_year
        herd_data_frame = self.cohorts_class.compute_cohort_population_in_baseline()

        weight_gain_cattle = self.loader_class.weight_gain_cattle()
        weight_gain_sheep = self.loader_class.weight_gain_sheep()

        sheep_system_dict = self.data_manager_class.sheep_system_dict

        cattle_cohort_time_indoors_2015 = self.data_manager_class.COHORT_TIME_INDOORS

        cohort_weight = self.data_manager_class.CATTLE_COHORT_WEIGHT

        system_params = self.data_manager_class.system_parameters

        ef_country = self.ef_country


        data = pd.DataFrame()

        new_index = 0

        for animal in herd_data_frame.columns:


            data.loc[new_index, "ef_country"] = ef_country
            data.loc[new_index, "farm_id"] = calibration_year
            data.loc[new_index, "Scenarios"] = -1
            data.loc[new_index, "year"] = calibration_year
            data.loc[new_index, "cohort"] = cohort_name_dict[animal]
            data.loc[new_index, "pop"] = herd_data_frame.loc[calibration_year,animal]
                    # Colm changed
            if data.loc[new_index, "cohort"] == "dairy_cows":
                data.loc[new_index, "daily_milk"] = self.data_manager_class.dairy_daily_milk_baseline
            elif data.loc[new_index, "cohort"] == "suckler_cows":
                data.loc[new_index, "daily_milk"] = self.data_manager_class.suckler_daily_milk_baseline
        
            else:
                data.loc[new_index, "daily_milk"] = 0

            if data.loc[new_index, "cohort"] in cohort_dict["Cattle"]:
                #Weights
                weight_col = cohort_weight[data.loc[new_index, "cohort"]]["weight_column"]
                weight_gain = weight_gain_cattle.loc[ef_country, weight_col]

                if cohort_weight[data.loc[new_index, "cohort"]]["mature"]:
                    weight = weight_gain
                elif cohort_weight[data.loc[new_index, "cohort"]]["more_than_2_years"]:
                    weight = weight_gain_cattle.loc[ef_country, "birth_weight"] + (weight_gain * 365) / 2
                else:
                    weight = weight_gain_cattle.loc[ef_country, "birth_weight"] + (weight_gain * 365)

                data.loc[new_index, "weight"] = weight
            else:
                weight_col = cohort_weight[data.loc[new_index, "cohort"]]["weight_column"]
                weight_gain = weight_gain_sheep.loc[ef_country, weight_col]
                if cohort_weight[data.loc[new_index, "cohort"]]["mature"]:
                    weight = weight_gain
                else: 
                    weight = weight_gain_sheep.loc[ef_country, "lamb_weight_at_birth"] + weight_gain

                data.loc[new_index, "weight"] = weight


            if data.loc[new_index, "cohort"] in cohort_dict["Cattle"]:
                data.loc[new_index, "forage"] = system_params["Cattle"]["forage"]
                data.loc[new_index, "grazing"] = system_params["Cattle"]["grazing"]
                data.loc[new_index, "con_type"] = system_params["Cattle"]["con_type"]

            else:
                data.loc[new_index, "forage"] = system_params["Sheep"]["forage"]
                data.loc[new_index, "grazing"] = (
                            sheep_system_dict[animal.split(" ")[0]] + system_params["Sheep"]["grazing"]
                        )
                data.loc[new_index, "con_type"] = system_params["Sheep"]["con_type"]

            if data.loc[new_index, "cohort"] in cohort_name_dict[animal]:
                
                data.loc[new_index, "con_amount"] = system_params["Sheep"]["concentrate"]
                data.loc[new_index, "wool"] = system_params["Sheep"]["wool"]

            elif data.loc[new_index, "cohort"] in cohort_dict["Cattle"]:

                con_amount = self.compute_concentrate(
                    data.loc[new_index, "cohort"],
                    data.loc[new_index, "daily_milk"],
                    data.loc[new_index, "weight"],
                )
                data.loc[new_index, "con_amount"] = con_amount
                data.loc[new_index, "wool"] = 0

            if data.loc[new_index, "cohort"] in cohort_dict["Cattle"]:
                if (
                    data.loc[new_index, "cohort"]
                    in cattle_cohort_time_indoors_2015["t_indoors"].keys()
                ):
                    data.loc[
                        new_index, "t_outdoors"
                    ] = cattle_cohort_time_indoors_2015["t_outdoors"][
                        data.loc[new_index, "cohort"]
                    ]
                    data.loc[
                        new_index, "t_indoors"
                    ] = cattle_cohort_time_indoors_2015["t_indoors"][
                        data.loc[new_index, "cohort"]
                    ]
                    data.loc[new_index, "t_stabled"] = 0
            else:
                data.loc[
                    new_index, "t_outdoors"
                ] = cattle_cohort_time_indoors_2015["t_outdoors"][
                        data.loc[new_index, "cohort"]]
                data.loc[
                    new_index, "t_indoors"
                ] = cattle_cohort_time_indoors_2015["t_indoors"][
                        data.loc[new_index, "cohort"]]
                data.loc[
                    new_index, "t_stabled"
                ] =0
                
            if data.loc[new_index, "cohort"] in cohort_dict["Cattle"]:
                    data.loc[new_index, "mm_storage"] = system_params["Cattle"]["baseline_manure_management"]
                    data.loc[new_index, "daily_spreading"] = system_params["Cattle"]["daily_spread"]
            else:
                data.loc[new_index, "mm_storage"] = system_params["Sheep"]["manure_management"]
                data.loc[new_index, "daily_spreading"] = system_params["Sheep"]["daily_spread"]
            
            data.loc[new_index, "n_sold"] = 0
            data.loc[new_index, "n_bought"] = 0

            new_index += 1

        return data


