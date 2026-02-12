def str_to_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes", "y", "on")

def normalize_heading(degrees):
    # 1. Reduce the angle to 0 - 360 range first (handles large numbers like 720)
    degrees = degrees % 360
    # 2. Force it to be the positive remainder, so that -90 becomes 270
    degrees = (degrees + 360) % 360
    # 3. Shift to -180 to 180
    if (degrees > 180):
        degrees -= 360
    return degrees