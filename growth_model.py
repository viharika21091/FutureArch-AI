def predict_growth(current_users, annual_growth):

    predictions = {}

    users = current_users

    for year in [1, 3, 5]:
        users = current_users * ((1 + annual_growth / 100) ** year)
        predictions[f"Year {year}"] = round(users)

    return predictions


def determine_growth_level(users):

    if users < 10000:
        return "Low"
    elif users < 100000:
        return "Medium"
    elif users < 1000000:
        return "High"
    else:
        return "Very High"