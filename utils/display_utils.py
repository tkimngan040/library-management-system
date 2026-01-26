def format_date(date_str):
    if not date_str:
        return "N/A"
    try:
        from datetime import datetime
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return date_str

def format_currency(amount):
    return f"{amount:,.0f} VND"
