def datetime_ops():
    from datetime import datetime, timedelta
    
    dates = []
    start = datetime.now()
    
    for i in range(10000):
        dates.append(start + timedelta(days=i))
    
    # Sort dates
    sorted_dates = sorted(dates)
    
    # Calculate differences
    diffs = []
    for i in range(len(dates) - 1):
        diffs.append(dates[i+1] - dates[i])
    
    return len(diffs)

datetime_ops()