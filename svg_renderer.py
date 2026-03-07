from lxml import etree

def svg_overwrite(filename, age_data, commit_data, star_data, repo_data, contrib_data, loc_data):
    tree = etree.parse(filename)
    root = tree.getroot()
    
    justify_format(root, 'age_data', age_data, 29) 
    
    find_and_replace(root, 'repo_data', f"{repo_data:,}")
    find_and_replace(root, 'contrib_data', f"{contrib_data:,}")
    find_and_replace(root, 'star_data', f"{star_data:,}")
    find_and_replace(root, 'commit_data', f"{commit_data:,}")
    find_and_replace(root, 'loc_data', f"{loc_data[2]}")
    find_and_replace(root, 'loc_add', f"{loc_data[0]}")
    find_and_replace(root, 'loc_del', f"{loc_data[1]}")
    
    tree.write(filename, encoding='utf-8', xml_declaration=True)

def justify_format(root, element_id, new_text, length=0):
    new_text = str(new_text)
    find_and_replace(root, element_id, new_text)
    
    if length > 0:
        just_len = max(0, length - len(new_text))
        dot_string = " ." + ("." * just_len) + " "
        find_and_replace(root, f"{element_id}_dots", dot_string)

def find_and_replace(root, element_id, new_text):
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = new_text