from PySide6.QtCore import QRect

def getWidgetEdgeGeometry(screen_width: int, screen_height: int, edge: str, widget_width: int, widget_height: int) -> QRect:

    # Determine the position based on the edge argument
    if edge == 'top':
        # Positioned at the top, centered horizontally
        x = (screen_width - widget_width) // 2
        y = 0
        return QRect(x, y, widget_width, widget_height)
    
    elif edge == 'bottom':
        # Positioned at the bottom, centered horizontally
        x = (screen_width - widget_width) // 2
        y = screen_height - widget_height
        return QRect(x, y, widget_width, widget_height)
    
    elif edge == 'left':
        # Positioned on the left, centered vertically
        x = 0
        y = (screen_height - widget_height) // 2
        return QRect(x, y, widget_width, widget_height)
    
    elif edge == 'right':
        # Positioned on the right, centered vertically
        x = screen_width - widget_width
        y = (screen_height - widget_height) // 2
        return QRect(x, y, widget_width, widget_height)

    elif edge == 'top-left':
        # Positioned at the top-left corner
        return QRect(0, 0, widget_width, widget_height)

    elif edge == 'top-right':
        # Positioned at the top-right corner
        x = screen_width - widget_width
        return QRect(x, 0, widget_width, widget_height)

    elif edge == 'bottom-left':
        # Positioned at the bottom-left corner
        y = screen_height - widget_height
        return QRect(0, y, widget_width, widget_height)

    elif edge == 'bottom-right':
        # Positioned at the bottom-right corner
        x = screen_width - widget_width
        y = screen_height - widget_height
        return QRect(x, y, widget_width, widget_height)

    else:
        raise ValueError("Invalid edge argument. Choose from 'left', 'right', 'top', 'bottom', 'top-left', 'top-right', 'bottom-left', 'bottom-right'.")