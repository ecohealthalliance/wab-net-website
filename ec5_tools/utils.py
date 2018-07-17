import re

def format_name(name):
    # Special names used in the application logic are formatted without
    # number prefixes so that refactoring is not necessary if the numbers
    # change. Removing number prefixes from all names doesn't work
    # since some questions would have matching names without them.
    if "_Country" in name:
        return "country"
    elif "bat_information" in name:
        return "BatData"
    elif "field_data_forms" in name:
        return "SiteData"
    elif "trapping_event_information" in name:
        return "TrappingEvent"
    else:
        # xs are appended to prevent errors caused by leading or training
        # underscores in django models. Double underscores are also invalid
        # in django models.
        return re.sub("_+", "_", ("x_" + name + "_x"))
