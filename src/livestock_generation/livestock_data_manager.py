
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
            "calf_f": {
                "DxD_calves_f": "DxD_heifers_less_2_yr",
                "DxB_calves_f": "DxB_heifers_less_2_yr",
                "BxB_calves_f": "BxB_heifers_less_2_yr",
            },
            "calf_m": {
                "DxD_calves_m": "DxD_steers_less_2_yr",
                "DxB_calves_m": "DxB_steers_less_2_yr",
                "BxB_calves_m": "BxB_steers_less_2_yr",
            },
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
                "dairy_cows": 10.4109589,
                "suckler_cows": 11.78082192,
                "DxD_calves_f": 16.10958904,
                "DxD_calves_m": 16.10958904,
                "DxB_calves_f": 16.10958904,
                "DxB_calves_m": 16.10958904,
                "BxB_calves_m": 16.10958904,
                "BxB_calves_f": 16.10958904,
                "DxD_heifers_less_2_yr": 12.49315068,
                "DxD_steers_less_2_yr": 5.534246575,
                "DxB_heifers_less_2_yr": 12.49315068,
                "DxB_steers_less_2_yr": 5.534246575,
                "BxB_heifers_less_2_yr": 12.49315068,
                "BxB_steers_less_2_yr": 5.534246575,
                "DxD_heifers_more_2_yr": 11.23491032,
                "DxD_steers_more_2_yr": 5.534246575,
                "DxB_heifers_more_2_yr": 11.23491032,
                "DxB_steers_more_2_yr": 5.534246575,
                "BxB_heifers_more_2_yr": 11.23491032,
                "BxB_steers_more_2_yr": 5.534246575,
                "bulls": 12.49315068,
                "ewes":2.64,
                "ram":2.64,
                "lamb_more_1_yr":2.64,
                "lamb_less_1_yr":2.64,
                "male_less_1_yr":2.64,
            },
            "t_outdoors": {
                "dairy_cows": 13.5890411,
                "suckler_cows": 12.21917808,
                "DxD_calves_f": 7.890410959,
                "DxD_calves_m": 7.890410959,
                "DxB_calves_f": 7.890410959,
                "DxB_calves_m": 7.890410959,
                "BxB_calves_m": 7.890410959,
                "BxB_calves_f": 7.890410959,
                "DxD_heifers_less_2_yr": 11.50684932,
                "DxD_steers_less_2_yr": 18.46575342,
                "DxB_heifers_less_2_yr": 11.50684932,
                "DxB_steers_less_2_yr": 18.46575342,
                "BxB_heifers_less_2_yr": 11.50684932,
                "BxB_steers_less_2_yr": 18.46575342,
                "DxD_heifers_more_2_yr": 12.76508968,
                "DxD_steers_more_2_yr": 18.46575342,
                "DxB_heifers_more_2_yr": 12.76508968,
                "DxB_steers_more_2_yr": 18.46575342,
                "BxB_heifers_more_2_yr": 12.76508968,
                "BxB_steers_more_2_yr": 18.46575342,
                "bulls": 11.50684932,
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


