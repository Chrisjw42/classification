from enum import Enum

class Classes(Enum):
    BANK_STATEMENT = 1
    DRIVERS_LICENCE = 2
    INVOICE = 3

class FileTypes(Enum):
    pdf = 1
    jpg = 2
    # TODO assess file compat of each classifier, build a bigger list

