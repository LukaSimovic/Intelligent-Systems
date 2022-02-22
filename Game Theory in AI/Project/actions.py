class Action:
    NORTH = 'NORTH'
    NE = 'NE'
    EAST = 'EAST'
    SE = 'SE'
    SOUTH = 'SOUTH'
    SW = 'SW'
    WEST = 'WEST'
    NW = 'NW'
    actions = {
        NORTH: (-1, 0),
        NE: (-1, 1),
        EAST: (0, 1),
        SE: (1, 1),
        SOUTH: (1, 0),
        SW: (1, -1),
        WEST: (0, -1),
        NW: (-1, -1)
    }
