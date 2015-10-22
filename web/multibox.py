from package import Package
from binpack import binpack
"""
***USER INTERFACE***
    1. Objective
        -An application which allows the user to find the optimal box(s)
        to put a list of merchandice in.
        -Order : Contains the merchandice which need to be boxed
        -Merchandice
            Need dimentions
            Need weight
            Need Amount
        -dimentions will be a string
            "(X)x(Y)x(z)" ie "9x7x5"

    2.

***Algorithm input***
    1. List of "Package" objects, containing all of the merchandice associated
    with an Order.  This will contain duplicates if there are more than one of
    a single item.
"""

base_boxes = {
    "box21": Package("9x7x5"),
    "box24": Package("10x8x6"),
    "box28": Package("12x10x6"),
    "box30": Package("12x10x8"),
    "box32": Package("12x10x10"),
    "box36": Package("16x12x8"),
    "box40": Package("16x14x10"),
    "box42": Package("18x14x10"),
    "box48": Package("18x16x14"),
    "box52": Package("20x16x16"),
    "box58": Package("24x18x16"),
    "box66": Package("28x20x18")
}


def eff(Merch, boxes):
    """
    Effency of a box is a percentage.
    eff = used_volume/total_volume
    """
    total_volume = 0
    for box in boxes:
        total_volume += box.volume
    used_volume = 0
    for m in Merch:
        used_volume += m.volume
    return used_volume/total_volume


def fit_to_boxes(Merch):
    """
    Find the The number of each box it would take to fill an order
    returned result is a list of dictionaries sorted
    first by amount of boxes used then by Effency
    """
    result = []
    for box_name, box_value in base_boxes.items():
        used,  not_used = binpack(Merch, box_value, 5000)
        if len(not_used) > 0:  # if one of the merch doesnt fit in this box dont use
            continue
        else:
            t = {
                'name': box_name,
                'amount': len(used),
                'eff': int(eff(Merch, [box_value]*len(used))*100)  # list of all boxes used
            }
            result.append(t)
    result.sort(key=lambda x: (x['amount'], -x['eff']))
    return result
