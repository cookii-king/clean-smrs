def clean_none_empty(data):
    """
    Recursively remove keys with None or empty string values from dictionaries,
    and remove empty lists and dictionaries.
    """
    if isinstance(data, dict):
        return {
            key: clean_none_empty(value)
            for key, value in data.items()
            if value not in [None, ''] and clean_none_empty(value) not in [None, {}, []]
        }
    elif isinstance(data, list):
        cleaned_list = [clean_none_empty(item) for item in data]
        return [item for item in cleaned_list if item not in [None, {}, []]]
    else:
        return data