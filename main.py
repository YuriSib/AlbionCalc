from scrapper import material_pars, get_html, xpath_resources
from add_to_table import add_value


html_dict = get_html(xpath_resources)
metal_html = html_dict.get('metal')
leather_html = html_dict.get('leather')
cloth_html = html_dict.get('cloth')
wood_html = html_dict.get('wood')
stone_html = html_dict.get('stone')

resources_data = [metal_html, leather_html, cloth_html, wood_html, stone_html]
start_row = 80
for resource in resources_data:
    material_data = material_pars(resource)
    add_value(material_data, start_row)
    start_row += 22

# metal_data = material_pars(leather_html)
# add_value(metal_data, 2)
