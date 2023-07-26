
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

                if herd_slice.loc[i, "cohort"] == "DxD_steers_less_2_yr":
                    if sc_herd_dataframe.loc[i, "pop"] != 0:
                        sc_weight += (weight_gain_cattle.loc[ef_country, "birth_weight"] + (
                                weight_gain_cattle.loc[ef_country, "DxD_calves_m_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "DxD_steers_less_2_yr_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "DxD_steers_more_2_yr_weight_gain"] * 365)) * \
                                     herd_slice.loc[i, "pop"]

                        weight_df.loc[sc, "DxD_steers_system_kg"] = ((weight_gain_cattle.loc[
                                                                          ef_country, "birth_weight"] + (
                                                                              weight_gain_cattle.loc[
                                                                                  ef_country, "DxD_calves_m_weight_gain"] * 365) + \
                                                                      (weight_gain_cattle.loc[
                                                                           ef_country, "DxD_steers_less_2_yr_weight_gain"] * 365) + \
                                                                      (weight_gain_cattle.loc[
                                                                           ef_country, "DxD_steers_more_2_yr_weight_gain"] * 365)) *
                                                                     herd_slice.loc[
                                                                         i, "pop"]) * carcass_weight_as_prop_of_LW

                elif herd_slice.loc[i, "cohort"] == "DxB_steers_less_2_yr":
                    if sc_herd_dataframe.loc[i, "pop"] != 0:
                        sc_weight += (weight_gain_cattle.loc[ef_country, "birth_weight"] + (
                                weight_gain_cattle.loc[ef_country, "DxB_calves_m_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "DxB_steers_less_2_yr_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "DxB_steers_more_2_yr_weight_gain"] * 365)) * \
                                     herd_slice.loc[i, "pop"]

                        weight_df.loc[sc, "DxB_steers_system_kg"] = ((weight_gain_cattle.loc[
                                                                          ef_country, "birth_weight"] + (
                                                                              weight_gain_cattle.loc[
                                                                                  ef_country, "DxB_calves_m_weight_gain"] * 365) + \
                                                                      (weight_gain_cattle.loc[
                                                                           ef_country, "DxB_steers_less_2_yr_weight_gain"] * 365) + \
                                                                      (weight_gain_cattle.loc[
                                                                           ef_country, "DxB_steers_more_2_yr_weight_gain"] * 365)) *
                                                                     herd_slice.loc[
                                                                         i, "pop"]) * carcass_weight_as_prop_of_LW

                elif herd_slice.loc[i, "cohort"] == "BxB_steers_less_2_yr":
                    if sc_herd_dataframe.loc[i, "pop"] != 0:
                        sc_weight += (weight_gain_cattle.loc[ef_country, "birth_weight"] + (
                                weight_gain_cattle.loc[ef_country, "BxB_calves_m_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "BxB_steers_less_2_yr_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "BxB_steers_more_2_yr_weight_gain"] * 365)) * \
                                     herd_slice.loc[i, "pop"]

                        weight_df.loc[sc, "BxB_steers_system_kg"] = ((weight_gain_cattle.loc[
                                                                          ef_country, "birth_weight"] + (
                                                                              weight_gain_cattle.loc[
                                                                                  ef_country, "BxB_calves_m_weight_gain"] * 365) + \
                                                                      (weight_gain_cattle.loc[
                                                                           ef_country, "BxB_steers_less_2_yr_weight_gain"] * 365) + \
                                                                      (weight_gain_cattle.loc[
                                                                           ef_country, "BxB_steers_more_2_yr_weight_gain"] * 365)) *
                                                                     herd_slice.loc[
                                                                         i, "pop"]) * carcass_weight_as_prop_of_LW

                elif herd_slice.loc[i, "cohort"] == "DxD_heifers_less_2_yr":
                    if sc_herd_dataframe.loc[i, "pop"] != 0:
                        sc_weight += (weight_gain_cattle.loc[ef_country, "birth_weight"] + (
                                weight_gain_cattle.loc[ef_country, "DxD_calves_f_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "DxD_heifers_less_2_yr_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "DxD_heifers_more_2_yr_weight_gain"] * 365)) * \
                                     herd_slice.loc[i, "pop"]

                        weight_df.loc[sc, "DxD_heifers_system_kg"] = ((weight_gain_cattle.loc[
                                                                           ef_country, "birth_weight"] + (
                                                                               weight_gain_cattle.loc[
                                                                                   ef_country, "DxD_calves_f_weight_gain"] * 365) + \
                                                                       (weight_gain_cattle.loc[
                                                                            ef_country, "DxD_heifers_less_2_yr_weight_gain"] * 365) + \
                                                                       (weight_gain_cattle.loc[
                                                                            ef_country, "DxD_heifers_more_2_yr_weight_gain"] * 365)) *
                                                                      herd_slice.loc[
                                                                          i, "pop"]) * carcass_weight_as_prop_of_LW

                elif herd_slice.loc[i, "cohort"] == "DxB_heifers_less_2_yr":
                    if sc_herd_dataframe.loc[i, "pop"] != 0:
                        sc_weight += (weight_gain_cattle.loc[ef_country, "birth_weight"] + (
                                weight_gain_cattle.loc[ef_country, "DxB_calves_f_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "DxB_heifers_less_2_yr_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "DxB_heifers_more_2_yr_weight_gain"] * 365)) * \
                                     herd_slice.loc[i, "pop"]

                        weight_df.loc[sc, "DxB_heifers_system_kg"] = ((weight_gain_cattle.loc[
                                                                           ef_country, "birth_weight"] + (
                                                                               weight_gain_cattle.loc[
                                                                                   ef_country, "DxB_calves_f_weight_gain"] * 365) + \
                                                                       (weight_gain_cattle.loc[
                                                                            ef_country, "DxB_heifers_less_2_yr_weight_gain"] * 365) + \
                                                                       (weight_gain_cattle.loc[
                                                                            ef_country, "DxB_heifers_more_2_yr_weight_gain"] * 365)) *
                                                                      herd_slice.loc[
                                                                          i, "pop"]) * carcass_weight_as_prop_of_LW

                elif herd_slice.loc[i, "cohort"] == "BxB_heifers_less_2_yr":
                    if sc_herd_dataframe.loc[i, "pop"] != 0:
                        sc_weight += (weight_gain_cattle.loc[ef_country, "birth_weight"] + (
                                weight_gain_cattle.loc[ef_country, "BxB_calves_f_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "BxB_heifers_less_2_yr_weight_gain"] * 365) + \
                                      (weight_gain_cattle.loc[ef_country, "BxB_heifers_more_2_yr_weight_gain"] * 365)) * \
                                     herd_slice.loc[i, "pop"]

                        weight_df.loc[sc, "BxB_heifers_system_kg"] = ((weight_gain_cattle.loc[
                                                                           ef_country, "birth_weight"] + (
                                                                               weight_gain_cattle.loc[
                                                                                   ef_country, "BxB_calves_f_weight_gain"] * 365) + \
                                                                       (weight_gain_cattle.loc[
                                                                            ef_country, "BxB_heifers_less_2_yr_weight_gain"] * 365) + \
                                                                       (weight_gain_cattle.loc[
                                                                            ef_country, "BxB_heifers_more_2_yr_weight_gain"] * 365)) *
                                                                      herd_slice.loc[
                                                                          i, "pop"]) * carcass_weight_as_prop_of_LW

            weight_df.loc[sc, "carcass_weight_kg"] = sc_weight * carcass_weight_as_prop_of_LW

        return weight_df

    def compute_system_total_protein_exports(self, scenario_animal_data, baseline_animal_data):

        """
                total protein exported by the entire system, assuming a milk protein content of 3.5% and a beef protein content of 23%
        """

        df_index = list(baseline_animal_data.Scenarios.unique())
        df_index.extend(scenario_animal_data.Scenarios.unique())
        sc_herd_dataframe = pd.concat([scenario_animal_data, baseline_animal_data], ignore_index=True)

        milk_protein_content = self.data_manager_class.milk_protein_content
        beef_protein_content = self.data_manager_class.beef_protein_content




        protein_system_export = pd.DataFrame(
            index=df_index,
            columns=["total_protein", "milk_protein", "beef_protein"])

        for sc in protein_system_export.index:

            milk_output = self.compute_system_milk_exports(scenario_animal_data,baseline_animal_data)
            beef_output = self.compute_system_protien_exports(scenario_animal_data,baseline_animal_data)

            protein_system_export.loc[sc, "milk_protein"] = milk_output.loc[sc, "total_milk_kg"] * milk_protein_content
            protein_system_export.loc[sc, "beef_protein"] = beef_output.loc[sc, "carcass_weight_kg"] * beef_protein_content

            protein_system_export.loc[sc, "total_protein"] = protein_system_export.loc[sc, "milk_protein"] + protein_system_export.loc[sc, "beef_protein"]


        return protein_system_export
