# 🐄🐏 Livstock generation tool for cattle herds and sheep flocks

 Based on the [GOBLIN](https://gmd.copernicus.org/articles/15/2239/2022/) (**G**eneral **O**verview for a **B**ackcasting approach of **L**ivestock **IN**tensification) Cattle herd module. The package is designed to take as inputs the scenario parameters, while outputing dataframes of animal parameters for scenarios and the chosen baseline year. It also contains classes to export milk and beef outputs. 

 The package is shipped with key data for past herd numbers, concentrate feed inputs, and animal features. 

 Currently parameterised for Ireland, the framework can be adapted for other contexts.

Outputs dataframes based on scenario inputs in relation to:

    -   Livestock by cohort
    -   Livestock population
    -   Daily milk
    -   Live weight
    -   Forage type
    -   Grazing type
    -   Concentrate input type and quantity
    -   Time outdoors, indoors and stabled
    -   Wool
    -   Manure management systems
    -   Daily spread systems
    -   Number bought and sold


## Installation

Install from git hub. 

When prompted enter your ```<username>``` and password, which is your ```<access_token>```.

```<access_token>``` is provided by the repo manager.

```<username>``` pass your own github username.


```bash
pip install "livestock_generation@git+https://github.com/colmduff/livestock_generation.git@main" 

```

## Usage
```python
from livestock_generation.livestock import AnimalData
from livestock_generation.livestock_exports import Exports
import pandas as pd


def main():
        

    # Create the DataFrame with the provided data, this represents scenario inputs
    data = [
        [0, "Dairy", "tank solid", 0, 0, 0.0879077282507005, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
        [0, "Dairy", "tank liquid", 172390.09063152, 0, 0.8, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
        [0, "Beef", "tank solid", 0, 0, 0.0879077282507005, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
        [0, "Beef", "tank liquid", 0, 27807.487070967, 0.0879077282507005, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 0, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
        [0, "Lowland sheep", "tank liquid", 0, 0, 0.0879077282507005, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 0, 0, 37812, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080],
        [0, "Upland sheep", "tank liquid", 0, 0, 0.0879077282507005, 0.500607270596862, 0, 0, 0, 0.801458098547012, 0.36840211684271, 0.0555663357895664, 0.126070113756632, 0, 0, 0.0784928061838073, 0.120049095269181, 0, 0.0879200186051467, 9453, 0, 0, 0, 136.870524806694, 105.00171069052, 0.591628596827221, 2080]
    ]

    columns = ["Scenarios", "Cattle systems", "Manure management", "Dairy pop", "Beef pop", "Dairy prod", "Beef prod", "mm_storage", "Cattle EF", "AD prod", "Forest area", "Conifer proportion", "Conifer harvest", "Conifer thinned", "Broadleaf harvest", "Bioenergy area", "Crop area", "Wetland area", "Land rewetting", "Grass management", "Upland sheep pop", "Upland sheep prod", "Lowland sheep pop", "Lowland sheep prod", "Dairy Pasture fertilisation", "Beef Pasture fertilisation", "Broadleaf proportion", "Afforest Year"]
    
    scenario_dataframe = pd.DataFrame(data, columns=columns)
    
    #create additional parameters
    baseline_year = 2018
    target_year = 2050
    ef_country = "ireland"
    

    #create classes for the generation of animal data and livestock ouput data 
    animal_class = AnimalData(ef_country, baseline_year, target_year, scenario_dataframe)
    export_class = Exports(ef_country, baseline_year, target_year, scenario_dataframe)
        
    #create dataframe for baseline year animals
    baseline_data = animal_class.create_baseline_animal_dataframe()

    #create dataframe for scenarios animals
    scenario_data = animal_class.create_animal_dataframe()

        
    #Create dataframes for beef and milk output
    beef_outputs = export_class.compute_system_protien_exports(scenario_data, baseline_data)

    dairy_outputs = export_class.compute_system_milk_exports(scenario_data, baseline_data)

    #Print generated data
    print(baseline_data)

    print(scenario_data)

    print(beef_outputs)

    print(dairy_outputs)

if __name__ == "__main__":
    main()
    
```
## License
This project is licensed under the terms of the MIT license.
