from app import db, Box
from sqlalchemy.exc import IntegrityError

stock_cartons = {
    'tag':    'stock',
    '14':     '6x4x4',
    '15':     '7x5x3',
    '16':     '6x6x4',
    '17':     '7x5x5',
    '18':     '8x6x4',
    '19':     '8x6x5',
    '20':     '8x6x6',
    '21':     '9x7x5',
    '22':     '11x7x6',
    '24':     '10x8x6',
    '26':     '10x8x8',
    '28':     '12x10x6',
    '30':     '12x10x8',
    '32':     '12x10x10',
    '34':     '14x12x8',
    '36':     '16x12x8',
    '38':     '16x12x10',
    '40':     '16x14x10',
    '42':     '18x14x10',
    '44':     '18x14x12',
    '46':     '18x14x14',
    '48':     '18x16x14',
    '50':     '20x16x14',
    '52':     '20x16x16',
    '54':     '20x18x16',
    '56':     '22x18x16',
    '58':     '24x18x16',
    '60':     '24x18x18',
    '62':     '24x20x18',
    '64':     '26x20x18',
    '66':     '28x20x18',
    '68':     '28x20x20',
    '70':     '26x24x20',
    '72':     '28x24x20',
    '74':     '26x24x24',
    '76':     '26x26x24',
    '78':     '30x24x24',
    '80':     '30x26x24',
    '88R':    '34x28x26',
    '88D':    '36x20x32',
}

printers = {
    'tag':        'printer',
    'p-3':    '11.25x8.75x3',
    'p-6':    '11.25x8.75x6',
    'p-9':    '11.25x8.75x9',
    'p-12':   '11.25x8.75x12',
    '17-4':   '17.25x11.25x4',
    '17-6':   '17.25x11.25x6',
    '17-8':   '17.25x11.25x8',
    '17-10':  '17.25x11.25x10',
    '17-12':  '17.25x11.25x12',
    '18-6':   '18.25x12.25x6',
    '18-8':   '18.25x12.25x8',
    '1.5D':   '18.5x12.5x10.5',
    '1D':     '12.5x9.5x13.5',
    '2D':     '18.5x12.5x13.5',
    '3D':     '18.5x12.5x20.5',
}

mc_line = {
    'tag':        'mc',
    'MC3':    '26x20x3',
    'MC4':    '26x20x4',
    'MC6':    '26x20x6',
    'MC8':    '26x20x8',
    'MC10':   '26x20x10',
    'MC12':   '26x20x12',
    'MC14':   '26x20x14',
    'MC16':   '26x20x16',
}

Cube = {
    'tag':        'cube',
    '4C':     '4x4x4',
    '5C':     '5x5x5',
    '6C':     '6x6x6',
    '7C':     '7x7x7',
    '8C':     '8x8x8',
    '9C':     '9x9x9',
    '10C':    '10x10x10',
    '12C':    '12x12x12',
    '14C':    '14x14x14',
    '16C':    '16x16x16',
    '18C':    '18x18x18',
    '20C':    '20x20x20',
    '22C':    '22x22x22',
}

line_30 = {
    'tag':        '30_line',
    '30-2':   '27x15x2',
    '30-3':   '27x15x3',
    '30-4':   '27x15x4',
    '30-6':   '27x15x6',
    '30-9':   '27x15x9',
    '30-12':  '27x15x12',
    '30-15':  '27x15x15',
}

line_34 = {
    'tag':        '34_line',
    '34-3':   '33x20x3',
    '34-4':   '33x20x4',
    '34-6':   '33x20x6',
    '34-8':   '33x20x8',
    '34-10':  '33x20x10',
    '34-12':  '33x20x12',
    '34-14':  '33x20x14',
    '34-16':  '33x20x16',
}

line_18 = {
    'tag':        '18_line',
    '18-3':   '30x18x3',
    '18-4':   '30x18x4',
    '18-5':   '30x18x5',
    '18-7':   '30x18x7',
    '18-9':   '30x18x9',
    '18-11':  '30x18x11',
    '18-13':  '30x18x13',
}

line_14 = {
    'tag':        '14_line',
    '14-2':   '14x10.5x2',
    '14-3':   '14x10.5x3',
    '14-4':   '14x10.5x4',
    '14-6':   '14x10.5x6',
    '14-8':   '14x10.5x8',
    '14-10':  '14x10.5x10',
}

line_36 = {
    'tag':        '36_line',
    '36-3':   '33x15x3',
    '36-4':   '33x15x4',
    '36-6':   '33x15x6',
    '36-9':   '33x15x9',
    '36-13':  '33x15x13',
    '36-17':  '33x15x17',
}

line_42 = {
    'tag':        '42_line',
    '42-4':   '39x15x4',
    '42-6':   '39x15x6',
    '42-9':   '39x15x9',
    '42-13':  '39x15x13',
    '42-17':  '39x15x17',
    '42-20':  '39x15x20',
}

misc = {
    'tag':        'misc',
    '111126':     '11x11x26',
    '11103':      '11.25x9.75x3.125',
    '12104':      '12x10x4',
    '121226':     '12x12x26',
    '12-11':      '12.5x10x11',
    '13-4':       '13x13x4.5',
    '13-20':      '13x13x7',
    '14-12':      '14x12x10',
    'BXK':        '15x10x10',
    '16-4':       '16x12x4',
    '16124':      '16x12x4.5',
    '40XX':       '16x14x5',
    '171012':     '16.75x9.5x11.5',
    '18-46':      '18x14x6',
    '181418':     '18x14x16',
    '1816':       '18x16x4',
    '181710':     '18x17x10.625',
    '19X15X4':    '19.75x16x4.125',
    '201310':     '20x13x10',
    '20-68':      '20x16x8',
    '20-12':      '20x18x12',
    '24-1':       '20.5x12.5x12',
    '2-7':        '21x14x7',
    'BR23':       '22x14x11.5',
    '22154':      '22x15x4',
    '22-10':      '22x18x10',
    '221914':     '22x19x14.5',
    '2318':       '23.5x11.75x12.75',
    'BGG':        '23.75x11.75x12.75',
    '241915':     '24x19x15',
    '24-10':      '24x12x10',
    '241512':     '24x15x12',
    '6D':         '24.5x18.5x20.5',
    '7D':         '24.5x18.5x23.5',
    '27174':      '27x17x4',
    '4D':         '27.5x12.5x17.12',
    '5D':         '27.5x12.5x22.5',
}

box_groups = [stock_cartons, printers, mc_line, Cube, line_30, line_34, line_18, line_14, line_36, line_42, misc]

owned_boxes = [
    'box21',
    'box24',
    'box28',
    'box30',
    'box32',
    'box34',
    'box36',
    'box40',
    'box42',
    'box44',
    'box48',
    'box52',
    'box58',
    'box66',
    'box18-6',
    'box3D',
    'box14-4',
    'box18-46',
    'box2-7'
]


def add_cartons(db, cartons, tag):
    """
    Add all of the boxes to the database
    """
    # stock cartons
    for key, value in cartons.iteritems():
        length, width, height = value.split('x')
        d = Box('box'+key, tags={tag}, length=int(float(length)), width=int(float(width)), height=int(float(height)))
        db.session.add(d)

    try:
        db.session.commit()
    except IntegrityError:
        return 1
        print("Duplicate boxes found!")
    return 0


def add_all_boxes():
    for item in box_groups:
        if add_cartons(db, item, item.pop('tag')) == 1:
            return 1


def add_tag(names, tag):
    """
    Adds the specified tag to all boxes with names
    input:
        names: ['name1', 'name2']
        tag: 'a_tag'
    """
    for name in names:
        b = Box.query.filter_by(box_name=name).first()
        b.box_tags.add(tag)
        db.session.commit()


db.create_all()  # creates the schemas
add_all_boxes()  # adds box data to db
add_tag(owned_boxes, 'owned')
