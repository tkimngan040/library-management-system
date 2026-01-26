from datetime import datetime
import config

def calculate_overdue_fine(due_date_str, return_date_str=None):
    if return_date_str is None:
        return_date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    due = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M:%S')
    ret = datetime.strptime(return_date_str, '%Y-%m-%d %H:%M:%S')
    
    if ret <= due:
        return 0, 0
    
    overdue_days = (ret - due).days
    fine = overdue_days * config.FINE_PER_DAY
    return overdue_days, fine
