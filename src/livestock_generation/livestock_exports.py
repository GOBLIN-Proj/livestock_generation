
import pandas as pd
from livestock_generation.livestock_data_manager import DataManager
from livestock_generation.data_loader import Loader


    
class Exports:
    def __init__(self,ef_country, calibration_year, target_year, scenario_inputs_df):
        self.loader_class = Loader(ef_country)
        self.data_manager_class = DataManager(ef_country, calibration_year, target_year, scenario_inputs_df)
        self.ef_country = ef_country


    def compute_system_milk_exports(self, scenario_animal_data, baseline_animal_data):

        df_index = list(baseline_animal_data.Scenarios.unique())
        df_index.extend(scenario_animal_data.Scenarios.unique())
        sc_herd_dataframe = pd.concat([scenario_animal_data, baseline_animal_data], ignore_index=True)


        milk_system_export = pd.DataFrame(
            index=df_index,
            columns=["Scenarios", "total_milk_kg"],
        )

        for sc in milk_system_export.index:

            mask = (
                (sc_herd_dataframe["cohort"] == "dairy_cows")
                & (sc_herd_dataframe["Scenarios"] == sc)
                & (sc_herd_dataframe["pop"] != 0)
            )

            milk_system_export.loc[sc, "total_milk_kg"] = (
                sc_herd_dataframe.loc[mask, "daily_milk"].values[0]
                * sc_herd_dataframe.loc[mask, "pop"].values[0]
                * 365
            )
            milk_system_export.loc[sc, "Scenarios"] = sc

        return milk_system_export
    

    def compute_system_protien_exports(self, scenario_animal_data, baseline_animal_data):

        """
        total beef weight exported from entire system.


        """

        df_index = list(baseline_animal_data.Scenarios.unique())
        df_index.extend(scenario_animal_data.Scenarios.unique())
        sc_herd_dataframe = pd.concat([scenario_animal_data, baseline_animal_data], ignore_index=True)

        weight_gain_cattle = self.loader_class.weight_gain_cattle()

        carcass_weight_as_prop_of_LW = self.data_manager_class.carcass_weight_as_prop_of_LW

        export_weight_keys = self.data_manager_class.EXPORT_WEIGHT_KEYS

        ef_country = self.ef_country

        weight_df = pd.DataFrame(
            index=df_index,
            columns=["Scenarios", "carcass_weight_kg"],
        )

        for sc in weight_df.index:

            sc_weight = 0
            herd_slice = sc_herd_dataframe[
                sc_herd_dataframe["Scenarios"] == sc
            ]  # take slice of data

            weight_df.loc[sc, "Scenarios"] = sc
            for i in herd_slice.index:  # iterate to the scenario

                if herd_slice.loc[i, "cohort"] in export_weight_keys["calf_f"].keys():
                    if sc_herd_dataframe.loc[i, "pop"] != 0:

                        sc_weight += (
                            weight_gain_cattle.loc[ef_country, "birth_weight"]
                            + (
                                weight_gain_cattle.loc[
                                    ef_country, herd_slice.loc[i, "cohort"] + "_weight_gain"
                                ]
                                * 365
                            )
                            + (
                                weight_gain_cattle.loc[
                                    ef_country,
                                    export_weight_keys["calf_f"][
                                        herd_slice.loc[i, "cohort"]
                                    ]
                                    + "_weight_gain",
                                ]
                                * 365
                            )
                        ) * herd_slice.loc[i, "pop"]

                        weight_df.loc[
                            sc,
                            export_weight_keys["calf_f"][herd_slice.loc[i, "cohort"]]
                            + "_kg",
                        ] = (
                            (
                                weight_gain_cattle.loc[ef_country, "birth_weight"]
                                + (
                                    weight_gain_cattle.loc[
                                        ef_country,
                                        herd_slice.loc[i, "cohort"] + "_weight_gain",
                                    ]
                                    * 365
                                )
                                + (
                                    weight_gain_cattle.loc[
                                        ef_country,
                                        export_weight_keys["calf_f"][
                                            herd_slice.loc[i, "cohort"]
                                        ]
                                        + "_weight_gain",
                                    ]
                                    * 365
                                )
                            )
                            * herd_slice.loc[i, "pop"]
                        ) * carcass_weight_as_prop_of_LW

                elif (
                    sc_herd_dataframe.loc[i, "cohort"]
                    in export_weight_keys["calf_m"].keys()
                ):
                    if sc_herd_dataframe.loc[i, "pop"] != 0:

                        sc_weight += (
                            weight_gain_cattle.loc[ef_country, "birth_weight"]
                            + (
                                weight_gain_cattle.loc[
                                    ef_country, herd_slice.loc[i, "cohort"] + "_weight_gain"
                                ]
                                * 365
                            )
                            + (
                                weight_gain_cattle.loc[
                                    ef_country,
                                    export_weight_keys["calf_m"][
                                        herd_slice.loc[i, "cohort"]
                                    ]
                                    + "_weight_gain",
                                ]
                                * 365
                            )
                        ) * herd_slice.loc[i, "pop"]

                        weight_df.loc[
                            sc,
                            export_weight_keys["calf_m"][herd_slice.loc[i, "cohort"]]
                            + "_kg",
                        ] = (
                            (
                                weight_gain_cattle.loc[ef_country, "birth_weight"]
                                + (
                                    weight_gain_cattle.loc[
                                        ef_country,
                                        herd_slice.loc[i, "cohort"] + "_weight_gain",
                                    ]
                                    * 365
                                )
                                + (
                                    weight_gain_cattle.loc[
                                        ef_country,
                                        export_weight_keys["calf_m"][
                                            herd_slice.loc[i, "cohort"]
                                        ]
                                        + "_weight_gain",
                                    ]
                                    * 365
                                )
                            )
                            * herd_slice.loc[i, "pop"]
                        ) * carcass_weight_as_prop_of_LW

            weight_df.loc[sc, "carcass_weight_kg"] = (
                sc_weight * carcass_weight_as_prop_of_LW
            )

        return weight_df