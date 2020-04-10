import json

def currentlyInfected(reportedCases):
    """
        Takes input as reportedCases and
        returns currenty infected estimations
        for impact and severe.
    """
    impact = reportedCases * 10
    severe = reportedCases * 50

    return impact, severe

def infectionsByRequestedTime(currentlyInfectedImpact, currentlyInfectedSevere, periodType, timeToElapse):
    """
        Takes input as currenty infected estimations
        for impact and severe, period type and time
        to elapse returns infections by requested time
        for impact and severe.
    """

    # Currently infected doubles every 3 days.
    if periodType == "days":
        factor = int(timeToElapse/3)
        impact = currentlyInfectedImpact * pow(2, factor)
        severe = currentlyInfectedSevere * pow(2, factor)
    elif periodType == "weeks":
        days = 7 * timeToElapse
        factor = int(days/3)
        impact = currentlyInfectedImpact * pow(2, factor)
        severe = currentlyInfectedSevere * pow(2, factor)
    else:   # For months. Days default to 30 days.
        factor = int(30/3)
        impact = currentlyInfectedImpact * pow(2, factor)
        severe = currentlyInfectedSevere * pow(2, factor)

    return impact, severe


def estimator(data):
    return data


if __name__ == '__main__':
    data = json.loads(open("src/input.json").read())
    estimator(data)
