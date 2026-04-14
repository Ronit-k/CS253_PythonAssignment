def calculate_raw_materials(item, quantity, recipes):
    """ 
    Args:
        item (str): The name of the item to craft.
        quantity (int): The desired quantity of the item.
        recipes (dict): A nested dictionary of crafting recipes.
        
    Returns:
        dict: A dictionary containing the total base raw materials and their quantities.
    """
    # base case, where the item itself is a raw material
    if item not in recipes:
        return {item: quantity}
    
    total_materials = {}
    
    recipe = recipes[item]
    for component, component_quantity_needed_per_item in recipe.items():
        # Total amount of component needed for the given quantity of 'item'
        total_component_needed = component_quantity_needed_per_item * quantity
        
        # Recursively find the raw materials for this component
        raw_materials_for_component = calculate_raw_materials(component, total_component_needed, recipes)
        
        # Update the total materials dictionary with the raw materials for the current component
        for raw_material, raw_material_quantity in raw_materials_for_component.items():
            total_materials[raw_material] = total_materials.get(raw_material, 0) + raw_material_quantity # add the raw material quantity to the total materials
            
    return total_materials

if __name__ == "__main__":
    recipes = {
        'SteelSword': {'SteelIngot': 2, 'LeatherGrip': 1},
        'SteelIngot': {'IronOre': 3, 'Coal': 2},
        'LeatherGrip': {'Leather': 1, 'String': 2},
        'String': {'PlantFibers': 3}
    }
    
    print(calculate_raw_materials('SteelSword', 5, recipes))
    # Output: {'IronOre': 30, 'Coal': 20, 'Leather': 5, 'PlantFibers': 30}
