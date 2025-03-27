from datetime import date

def extract_date_parts(date_obj: date):
    return {
        "year": str(date_obj.year),
        "month": str(date_obj.month),
        "day": str(date_obj.day),
        "until_date": date_obj
    }