import logging as log


def find_elem_by_class(soup, tag, att_val, get_text=True):
    if not soup:
        log.error(f"soup is of None type")
        return None
    try:
        if get_text:
            return soup.find(tag, class_=att_val).text
        else:
            return soup.find(tag, class_=att_val)
    except Exception as ex:
        log.error(ex)
        return None

def find_elems_by_class(soup, tag, att_val):
    if not soup:
        log.error(f"soup is of None type")
        return None
    try:
        return soup.find_all(tag, class_=att_val)
    except Exception as ex:
        log.error(ex)
        return None