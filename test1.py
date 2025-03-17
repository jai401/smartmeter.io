from datetime import datetime, timedelta

def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days

start_date = datetime(2008, 8, 1)
end_date = datetime(2008, 8, 3)
    
print(date_range(start_date, end_date))
