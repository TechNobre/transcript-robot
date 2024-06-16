def format_duration(seconds):
    # Convert seconds to hours, minutes, and seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    # Build the formatted string
    formatted_time = []
    if hours > 0:
        formatted_time.append(f"{hours}h")
    if minutes > 0 or hours > 0:  # Include minutes if there are any hours
        formatted_time.append(f"{minutes:02}m")
    formatted_time.append(f"{seconds:02}s")

    return " ".join(formatted_time)
