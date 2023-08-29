
from livestock_generation.data_loader import Loader


class DataManager:

    def __init__(self, ef_country, calibration_year, target_year, scenario_inputs_df):

        self.loader_class = Loader(ef_country)

        self.calibration_year = calibration_year
        self.default_calibration_year = 2015
        self.target_year = target_year

        self.cohort_name_conversion_dict = {
            "Dairy pop": "dairy_cows",
            "Beef pop": "suckler_cows",
            "Lowland sheep pop": "Lowland ewes",
            "Upland sheep pop": "Upland ewes",
        }

        self.COHORTS_DICT = {
            "Cattle": [
                "dairy_cows",
                "suckler_cows",
                "bulls",
                "DxD_calves_m",
                "DxD_calves_f",
                "DxB_calves_m",
                "DxB_calves_f",
                "BxB_calves_m",
                "BxB_calves_f",
                "DxD_heifers_less_2_yr",
                "DxD_steers_less_2_yr",
                "DxB_heifers_less_2_yr",
                "DxB_steers_less_2_yr",
                "BxB_heifers_less_2_yr",
                "BxB_steers_less_2_yr",
                "DxD_heifers_more_2_yr",
                "DxD_steers_more_2_yr",
                "DxB_heifers_more_2_yr",
                "DxB_steers_more_2_yr",
                "BxB_heifers_more_2_yr",
                "BxB_steers_more_2_yr",
            ],
            "Sheep": [
                "Lowland ewes",
                "Upland ewes",
                "Lowland lamb_less_1_yr",
                "Upland lamb_less_1_yr",
                "Lowland lamb_more_1_yr",
                "Upland lamb_more_1_yr",
                "Upland male_less_1_yr",
                "Lowland male_less_1_yr",
                "Lowland ram",
                "Upland ram",
            ],
        }

        self.DAIRY_BEEF_COHORTS = {
            "Dairy": [
                "dairy_cows",
                "DxD_calves_m",
                "DxD_calves_f",
                "DxD_heifers_less_2_yr",
                "DxD_steers_less_2_yr",
                "DxD_heifers_more_2_yr",
                "DxD_steers_more_2_yr",
            ],
            "Beef": [
                "suckler_cows",
                "bulls",
                "DxB_calves_m",
                "DxB_calves_f",
                "BxB_calves_m",
                "BxB_calves_f",
                "DxB_heifers_less_2_yr",
                "DxB_steers_less_2_yr",
                "BxB_heifers_less_2_yr",
                "BxB_steers_less_2_yr",
                "DxB_heifers_more_2_yr",
                "DxB_steers_more_2_yr",
                "BxB_heifers_more_2_yr",
                "BxB_steers_more_2_yr",
            ],
        }

        self.EXPORT_WEIGHT_KEYS = {
            "DxD_m":{"Pop_Cohort":"DxD_steers_less_2_yr",
                     "Calf_LWG":"DxD_calves_m_weight_gain",
                     "Steer_Heifer_less_2_LWG": "DxD_steers_less_2_yr_weight_gain",
                     "Steer_Heifer_more_2_LWG": "DxD_steers_more_2_yr_weight_gain"
            },
            "DxD_f":{"Pop_Cohort":"DxD_heifers_less_2_yr",
                     "Calf_LWG":"DxD_calves_f_weight_gain",
                     "Steer_Heifer_less_2_LWG": "DxD_heifers_less_2_yr_weight_gain",
                     "Steer_Heifer_more_2_LWG": "DxD_heifers_more_2_yr_weight_gain"
            },
            "DxB_m": {"Pop_Cohort": "DxB_steers_less_2_yr",
                      "Calf_LWG": "DxB_calves_m_weight_gain",
                      "Steer_Heifer_less_2_LWG": "DxB_steers_less_2_yr_weight_gain",
                      "Steer_Heifer_more_2_LWG": "DxB_steers_more_2_yr_weight_gain"
                      },
            "DxB_f": {"Pop_Cohort": "DxB_heifers_less_2_yr",
                      "Calf_LWG": "DxB_calves_f_weight_gain",
                      "Steer_Heifer_less_2_LWG": "DxB_heifers_less_2_yr_weight_gain",
                      "Steer_Heifer_more_2_LWG": "DxB_heifers_more_2_yr_weight_gain"
                      },
            "BxB_m": {"Pop_Cohort": "BxB_steers_less_2_yr",
                      "Calf_LWG": "BxB_calves_m_weight_gain",
                      "Steer_Heifer_less_2_LWG": "BxB_steers_less_2_yr_weight_gain",
                      "Steer_Heifer_more_2_LWG": "BxB_steers_more_2_yr_weight_gain"
                      },
            "BxB_f": {"Pop_Cohort": "BxB_heifers_less_2_yr",
                      "Calf_LWG": "BxB_calves_f_weight_gain",
                      "Steer_Heifer_less_2_LWG": "BxB_heifers_less_2_yr_weight_gain",
                      "Steer_Heifer_more_2_LWG": "BxB_heifers_more_2_yr_weight_gain"
                      }
        }

        self.HERD_RELATION = {
            "Cattle": {
                "DxD_calves_f": ["dairy_cows"],
                "DxD_calves_m": ["dairy_cows"],
                "DxB_calves_f": ["dairy_cows"],
                "DxB_calves_m": ["dairy_cows"],
                "BxB_calves_f": ["suckler_cows"],
                "BxB_calves_m": ["suckler_cows"],
                "DxD_heifers_less_2_yr": ["dairy_cows"],
                "DxD_steers_less_2_yr": ["dairy_cows"],
                "DxB_heifers_less_2_yr": ["dairy_cows"],
                "DxB_steers_less_2_yr": ["dairy_cows"],
                "BxB_heifers_less_2_yr": ["suckler_cows"],
                "BxB_steers_less_2_yr": ["suckler_cows"],
                "DxD_heifers_more_2_yr": ["dairy_cows"],
                "DxD_steers_more_2_yr": ["dairy_cows"],
                "DxB_heifers_more_2_yr": ["dairy_cows"],
                "DxB_steers_more_2_yr": ["dairy_cows"],
                "BxB_heifers_more_2_yr": ["suckler_cows"],
                "BxB_steers_more_2_yr": ["suckler_cows"],
                "bulls": ["dairy_cows", "suckler_cows"],
            },
            "Sheep": {
                "Lowland lamb_less_1_yr": ["Lowland ewes"],
                "Lowland male_less_1_yr": ["Lowland ewes"],
                "Lowland lamb_more_1_yr": ["Lowland ewes"],
                "Lowland ram": ["Lowland ewes"],
                "Upland lamb_less_1_yr": ["Upland ewes"],
                "Upland male_less_1_yr": ["Upland ewes"],
                "Upland lamb_more_1_yr": ["Upland ewes"],
                "Upland ram": ["Upland ewes"],
            },
        }

        self.COHORT_NAME_DICT = {
            "dairy_cows": "dairy_cows",
            "suckler_cows": "suckler_cows",
            "DxD_calves_f": "DxD_calves_f",
            "DxD_calves_m": "DxD_calves_m",
            "DxB_calves_f": "DxB_calves_f",
            "DxB_calves_m": "DxB_calves_m",
            "BxB_calves_m": "BxB_calves_m",
            "BxB_calves_f": "BxB_calves_f",
            "DxD_heifers_less_2_yr": "DxD_heifers_less_2_yr",
            "DxD_steers_less_2_yr": "DxD_steers_less_2_yr",
            "DxB_heifers_less_2_yr": "DxB_heifers_less_2_yr",
            "DxB_steers_less_2_yr": "DxB_steers_less_2_yr",
            "BxB_heifers_less_2_yr": "BxB_heifers_less_2_yr",
            "BxB_steers_less_2_yr": "BxB_steers_less_2_yr",
            "DxD_heifers_more_2_yr": "DxD_heifers_more_2_yr",
            "DxD_steers_more_2_yr": "DxD_steers_more_2_yr",
            "DxB_heifers_more_2_yr": "DxB_heifers_more_2_yr",
            "DxB_steers_more_2_yr": "DxB_steers_more_2_yr",
            "BxB_heifers_more_2_yr": "BxB_heifers_more_2_yr",
            "BxB_steers_more_2_yr": "BxB_steers_more_2_yr",
            "bulls": "bulls",
            "Lowland ewes": "ewes",
            "Upland ewes": "ewes",
            "Lowland lamb_less_1_yr": "lamb_less_1_yr",
            "Upland lamb_less_1_yr": "lamb_less_1_yr",
            "Lowland lamb_more_1_yr": "lamb_more_1_yr",
            "Upland lamb_more_1_yr": "lamb_more_1_yr",
            "Upland male_less_1_yr": "male_less_1_yr",
            "Lowland male_less_1_yr": "male_less_1_yr",
            "Lowland ram": "ram",
            "Upland ram": "ram",
        }

        self.COHORT_TIME_INDOORS = {
            "t_indoors": {
                "dairy_cows": 8.153424658,
                "suckler_cows": 9.66575,
                "DxD_calves_f": 9.60000,
                "DxD_calves_m": 9.60000,
                "DxB_calves_f": 9.60000,
                "DxB_calves_m": 9.60000,
                "BxB_calves_m": 9.60000,
                "BxB_calves_f": 9.60000,
                "DxD_heifers_less_2_yr": 9.73151,
                "DxD_steers_less_2_yr": 9.53425,
                "DxB_heifers_less_2_yr": 9.73151,
                "DxB_steers_less_2_yr": 9.53425,
                "BxB_heifers_less_2_yr": 9.73151,
                "BxB_steers_less_2_yr": 9.53425,
                "DxD_heifers_more_2_yr": 9.73151,
                "DxD_steers_more_2_yr": 9.60000,
                "DxB_heifers_more_2_yr": 9.73151,
                "DxB_steers_more_2_yr": 9.60000,
                "BxB_heifers_more_2_yr": 9.73151,
                "BxB_steers_more_2_yr": 9.60000,
                "bulls": 9.46849,
                "ewes":2.64,
                "ram":2.64,
                "lamb_more_1_yr":2.64,
                "lamb_less_1_yr":2.64,
                "male_less_1_yr":2.64,
            },
            "t_outdoors": {
                "dairy_cows": 15.84658,
                "suckler_cows": 14.33425,
                "DxD_calves_f": 14.40000,
                "DxD_calves_m": 14.40000,
                "DxB_calves_f": 14.40000,
                "DxB_calves_m": 14.40000,
                "BxB_calves_m": 14.40000,
                "BxB_calves_f": 14.40000,
                "DxD_heifers_less_2_yr": 14.26849,
                "DxD_steers_less_2_yr": 14.46575,
                "DxB_heifers_less_2_yr": 14.26849,
                "DxB_steers_less_2_yr": 14.46575,
                "BxB_heifers_less_2_yr": 14.26849,
                "BxB_steers_less_2_yr": 14.46575,
                "DxD_heifers_more_2_yr": 14.26849,
                "DxD_steers_more_2_yr": 14.40000,
                "DxB_heifers_more_2_yr": 14.26849,
                "DxB_steers_more_2_yr": 14.40000,
                "BxB_heifers_more_2_yr": 14.26849,
                "BxB_steers_more_2_yr": 14.40000,
                "bulls": 14.53151,
                "ewes":21.36,
                "ram":21.36,
                "lamb_more_1_yr":21.36,
                "lamb_less_1_yr":21.36,
                "male_less_1_yr":21.36,
            },
        }

        self.COHORTS_CONCENTRATE = {"NO_FEED": [
            "DxD_heifers_less_2_yr", "DxD_steers_less_2_yr", "DxB_heifers_less_2_yr",
            "DxB_steers_less_2_yr", "BxB_heifers_less_2_yr", "BxB_steers_less_2_yr",
            "DxD_heifers_more_2_yr", "DxD_steers_more_2_yr", "DxB_heifers_more_2_yr",
            "DxB_steers_more_2_yr", "BxB_heifers_more_2_yr", "BxB_steers_more_2_yr"
        ],
        "FEED": [
        "DxD_calves_f", "DxD_calves_m", "DxB_calves_f", "DxB_calves_m",
        "BxB_calves_f", "BxB_calves_m"
        ]}

        self.systems = ["Cattle", "Sheep"]
        self.cattle_systems = ["Dairy", "Beef"]
        self.sheep_systems = ["Lowland sheep", "Upland sheep"]

        self.calf_weight_gain_lookup = {
        ("DxD", "male"): "DxD_calves_m_weight_gain",
        ("DxD", "female"): "DxD_calves_f_weight_gain",
        ("DxB", "male"): "DxB_calves_m_weight_gain",
        ("DxB", "female"): "DxB_calves_f_weight_gain",
        ("BxB", "male"): "BxB_calves_m_weight_gain",
        ("BxB", "female"): "BxB_calves_f_weight_gain",
        }

        self.steer_heifer_weight_gain_lookup = {
            ("DxD", "male"): "DxD_steers_less_2_yr_weight_gain",
            ("DxD", "female"): "DxD_heifers_less_2_yr_weight_gain",
            ("DxB", "male"): "DxB_steers_less_2_yr_weight_gain",
            ("DxB", "female"): "DxB_heifers_less_2_yr_weight_gain",
            ("BxB", "male"): "BxB_steers_less_2_yr_weight_gain",
            ("BxB", "female"): "BxB_heifers_less_2_yr_weight_gain",
        }

        self.ANIMAL_SYSTEM_MAPPING = {
            "Dairy": "Dairy prod",
            "Beef": "Beef prod",
            "Lowland": "Lowland sheep prod",
            "Upland": "Upland sheep prod"
        }

        self.CATTLE_COHORT_WEIGHT = {
            "dairy_cows": {
                "weight_column": "mature_weight_dairy_cows",
                "age": "mature",
                "genetics": None,
                "gender": "female",
                "system":"Cattle"
            },
            "suckler_cows": {
                "weight_column": "mature_weight_suckler_cows",
                "age": "mature",
                "genetics": None,
                "gender": "female",
                "system":"Cattle"
            },
            "bulls": {
                "weight_column": "mature_weight_bulls",
                "age": "mature",
                "genetics": None,
                "gender": "male",
                "system":"Cattle"
            },
            "DxD_calves_f": {
                "weight_column": "DxD_calves_f_weight_gain",
                "age": "calf",
                "genetics": "DxD",
                "gender": "female",
                "system":"Cattle"
            },
            "DxD_calves_m": {
                "weight_column": "DxD_calves_m_weight_gain",
                "age": "calf",
                "genetics": "DxD",
                "gender": "male",
                "system":"Cattle"
            },
            "DxB_calves_f": {
                "weight_column": "DxB_calves_f_weight_gain",
                "age": "calf",
                "genetics": "DxB",
                "gender": "female",
                "system":"Cattle"
            },
            "DxB_calves_m": {
                "weight_column": "DxB_calves_m_weight_gain",
                "age": "calf",
                "genetics": "DxB",
                "gender": "male",
                "system":"Cattle"
            },
            "BxB_calves_f": {
                "weight_column": "BxB_calves_f_weight_gain",
                "age": "calf",
                "genetics": "BxB",
                "gender": "female",
                "system":"Cattle"
            },
            "BxB_calves_m": {
                "weight_column": "BxB_calves_m_weight_gain",
                "age": "calf",
                "genetics": "BxB",
                "gender": "male",
                "system":"Cattle"
            },
            "DxD_heifers_less_2_yr": {
                "weight_column": "DxD_heifers_less_2_yr_weight_gain",
                "age": "less_than_2_yr",
                "genetics": "DxD",
                "gender": "female",
                "system":"Cattle"
            },
            "DxD_steers_less_2_yr": {
                "weight_column": "DxD_steers_less_2_yr_weight_gain",
                "age": "less_than_2_yr",
                "genetics": "DxD",
                "gender": "male",
                "system":"Cattle"
            },
            "DxB_heifers_less_2_yr": {
                "weight_column": "DxB_heifers_less_2_yr_weight_gain",
                "age": "less_than_2_yr",
                "genetics": "DxB",
                "gender": "female",
                "system":"Cattle"
            },
            "DxB_steers_less_2_yr": {
                "weight_column": "DxB_steers_less_2_yr_weight_gain",
                "age": "less_than_2_yr",
                "genetics": "DxB",
                "gender": "male",
                "system":"Cattle"
            },
            "BxB_heifers_less_2_yr": {
                "weight_column": "BxB_heifers_less_2_yr_weight_gain",
                "age": "less_than_2_yr",
                "genetics": "BxB",
                "gender": "female",
                "system":"Cattle"
            },
            "BxB_steers_less_2_yr": {
                "weight_column": "BxB_steers_less_2_yr_weight_gain",
                "age": "less_than_2_yr",
                "genetics": "BxB",
                "gender": "male",
                "system":"Cattle"
            },
            "DxD_heifers_more_2_yr": {
                "weight_column": "DxD_heifers_more_2_yr_weight_gain",
                "age": "more_than_2_yr",
                "genetics": "DxD",
                "gender": "female",
                "system":"Cattle"
            },
            "DxD_steers_more_2_yr": {
                "weight_column": "DxD_steers_more_2_yr_weight_gain",
                "age": "more_than_2_yr",
                "genetics": "DxD",
                "gender": "male",
                "system":"Cattle"
            },
            "DxB_heifers_more_2_yr": {
                "weight_column": "DxB_heifers_more_2_yr_weight_gain",
                "age": "more_than_2_yr",
                "genetics": "DxB",
                "gender": "female",
                "system":"Cattle"
            },
            "DxB_steers_more_2_yr": {
                "weight_column": "DxB_steers_more_2_yr_weight_gain",
                "age": "more_than_2_yr",
                "genetics": "DxB",
                "gender": "male",
                "system":"Cattle"
            },
            "BxB_heifers_more_2_yr": {
                "weight_column": "BxB_heifers_more_2_yr_weight_gain",
                "age": "more_than_2_yr",
                "genetics": "BxB",
                "gender": "female",
                "system":"Cattle"
            },
            "BxB_steers_more_2_yr": {
                "weight_column": "BxB_steers_more_2_yr_weight_gain",
                "age": "more_than_2_yr",
                "genetics": "BxB",
                "gender": "male",
                "system":"Cattle"
                
            },
            "ewes": {
                "weight_column": "mature_weight_female",
                "system":"Sheep",
                "age": "mature"
                
            },
            "ram": {
                "weight_column": "mature_weight_male",
                "system":"Sheep",
                "age": "mature"
                
            },
            "lamb_less_1_yr": {
                "weight_column": "lamb_less_1_yr_weight_after_weaning",
                "system":"Sheep",
                "age": "immature"
                
            },
            "lamb_more_1_yr": {
                "weight_column": "lamb_more_1_yr_weight",
                "system":"Sheep",
                "age": "immature"
                
            },
            "male_less_1_yr": {
                "weight_column": "lamb_less_1_yr_weight_after_weaning",
                "system":"Sheep",
                "age": "immature"
                
            }
        }

        self.dairy_daily_milk_baseline = 14.953 #kg per day


        self.suckler_daily_milk_baseline = 1.410958904 #kg per day

        self.carcass_weight_as_prop_of_LW = 0.521

        self.milk_protein_content = 0.035

        self.beef_protein_content = 0.23

        self.sheep_system_dict = {"Lowland": "flat_", "Upland": "hilly_"}

        self.system_parameters = {
            "Cattle": {
                "con_type": "concentrate",
                "daily_spread": "broadcast",
                "forage": "irish_grass",
                "grazing": "pasture",
                "baseline_manure_management":"tank liquid"
            },
            "Sheep": {
                "con_type": "concentrate",
                "daily_spread": "broadcast",
                "concentrate": 0,
                "wool": 4.5,
                "manure_management": "solid",
                "forage": "average",
                "grazing": "pasture"
            }
        }


        self.scenario_inputs_df = scenario_inputs_df


