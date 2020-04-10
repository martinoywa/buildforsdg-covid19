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
    """
        Takes in input data and returns it in a
        specified format.
    """
    currentlyInfectedImpact, currentlyInfectedSevere = currentlyInfected(data["reportedCases"])
    infectionsByRequestedTimeImpact, infectionsByRequestedTimeSevere = infectionsByRequestedTime(
                                                                            currentlyInfectedImpact,
                                                                            currentlyInfectedSevere,
                                                                            data["periodType"],
                                                                            data["timeToElapse"]
                                                                            )

    output = {
          "data": data,
          "impact": {
              "currentlyInfected": currentlyInfectedImpact,
              "infectionsByRequestedTime": infectionsByRequestedTimeImpact
              },
          "severe": {
              "currentlyInfected": currentlyInfectedSevere,
              "infectionsByRequestedTime": infectionsByRequestedTimeSevere
              }
            }

    return output
