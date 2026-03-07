from lxml import etree

def svg_overwrite(filename, age_data, commit_data, star_data, repo_data, contrib_data, loc_data):
    tree = etree.parse(filename)
    root = tree.getroot()
    
    justify_format(root, 'age_data', age_data)
    justify_format(root, 'commit_data', commit_data)
    justify_format(root, 'star_data', star_data)
    justify_format(root, 'repo_data', repo_data)
    justify_format(root, 'contrib_data', contrib_data)
    justify_format(root, 'loc_data', loc_data[2])
    justify_format(root, 'loc_add', loc_data[0])
    justify_format(root, 'loc_del', loc_data[1])
    
    tree.write(filename, encoding='utf-8', xml_declaration=True)

def justify_format(root, element_id, new_text, length=0):
    if isinstance(new_text, int):
        new_text = f"{'{:,}'.format(new_text)}"
    new_text = str(new_text)
    find_and_replace(root, element_id, new_text)
    
    just_len = max(0, length - len(new_text))
    if just_len <= 2:
        dot_map = {0: '', 1: ' ', 2: '. '}
        dot_string = dot_map[just_len]
    else:
        dot_string = ' ' + ('.' * just_len) + ' '
    find_and_replace(root, f"{element_id}_dots", dot_string)

def find_and_replace(root, element_id, new_text):
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = new_text