from typing import List, Dict

class TypeConverter:
    """
    This class contains methods to convert types from one type to another
    """
    @staticmethod
    def convert_type_in_dict(dict_item, source_type, target_type):
        # This method iterates a dictionary looking for values of source_type and converts them to target_type
        # Embedded dictionaries and lists are called recursively.
        if dict_item is None: return None

        for k, v in list(dict_item.items()):
            if isinstance(v, dict):
                TypeConverter.convert_type_in_dict(v, source_type, target_type)
            elif isinstance(v, list):
                for l in v:
                    if not isinstance(l, dict):
                        continue
                    TypeConverter.convert_type_in_dict(l, source_type, target_type)
            elif isinstance(v, source_type):
                dict_item[k] = target_type(v)

        return dict_item

    @staticmethod
    def convert_type_in_list(list_instance: List, target_type):
        """
        This method converts each element of list into a target_type
        """
        for item in list_instance:
            target_type(item)

        return list_instance


