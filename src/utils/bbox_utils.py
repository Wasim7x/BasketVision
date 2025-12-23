def get_center_of_bbox(bbox):
    """
    Calculate the center (x, y) coordinates of a bounding box.

    Args:
        bbox (tuple): A tuple representing the bounding box (x, y, width, height).

    Returns:
        tuple: A tuple containing the center (x, y) coordinates.
    """
    x1, y1, x2, y2 = bbox
    return (int((x1 + x2) / 2), int((y1 + y2) / 2))

def get_bbox_width(bbox):
    """
    Calculate the width of a bounding box.

    Args:
        bbox (tuple): A tuple representing the bounding box (x, y, width, height).

    Returns:
        int: The width of the bounding box.
    """
    
    return int(bbox[2] - bbox[0])

def get_foot_position(bbox):
    """
    Calculate the position of the bottom center point of a bounding box.

    Args:
        bbox (tuple): Bounding box coordinates in format (x1, y1, x2, y2).

    Returns:
        tuple: Coordinates (x, y) of the bottom center point.
    """
    x1,y1,x2,y2 = bbox
    return int((x1+x2)/2),int(y2)