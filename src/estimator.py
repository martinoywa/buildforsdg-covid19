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

def hospitalBedsByRequestedTime(severeCasesByRequestedTimeImpact, severeCasesByRequestedTimeSevere, totalHospitalBeds):
    """
        Takes input as severe cases by requested time
        for both impact and severe, and total hospital beds
        and returns total beds for estimated positive patients.
    """
    available = int(0.35 * totalHospitalBeds)
    impact = available - severeCasesByRequestedTimeImpact
    severe = available - severeCasesByRequestedTimeSevere

    return impact, severe


def estimator(data):
    """
        Takes input data and returns it in a
        specified format.
    """
    currentlyInfectedImpact, currentlyInfectedSevere = currentlyInfected(data["reportedCases"])
    infectionsByRequestedTimeImpact, infectionsByRequestedTimeSevere = infectionsByRequestedTime(
                                                                            currentlyInfectedImpact,
                                                                            currentlyInfectedSevere,
                                                                            data["periodType"],
                                                                            data["timeToElapse"]
                                                                            )

    # 15% of infectionsByRequestedTime. Positives
    severeCasesByRequestedTimeImpact = int(0.15 * infectionsByRequestedTimeImpact)
    severeCasesByRequestedTimeSevere = int(0.15 * infectionsByRequestedTimeSevere)

    hospitalBedsByRequestedTimeImpact, hospitalBedsByRequestedTimeSevere = hospitalBedsByRequestedTime(
                                                                                severeCasesByRequestedTimeImpact,
                                                                                severeCasesByRequestedTimeSevere,
                                                                                data["totalHospitalBeds"]
                                                                                )

    # 5% of infectionsByRequestedTime that require ICU care.
    casesForICUByRequestedTimeImpact = int(0.05 * infectionsByRequestedTimeImpact)
    casesForICUByRequestedTimeSevere = int(0.05 * infectionsByRequestedTimeSevere)

    # 2% of infectionsByRequestedTime that require Ventilators.
    casesForVentilatorsByRequestedTimeImpact = int(0.02 * infectionsByRequestedTimeImpact)
    casesForVentilatorsByRequestedTimeSevere = int(0.02 * infectionsByRequestedTimeSevere)



    output = {
          "data": data,
          "estimate": {
                "impact": {
                    "currentlyInfected": currentlyInfectedImpact,
                    "infectionsByRequestedTime": infectionsByRequestedTimeImpact,
                    "severeCasesByRequestedTime": severeCasesByRequestedTimeImpact,
                    "hospitalBedsByRequestedTime": hospitalBedsByRequestedTimeImpact,
                    "casesForICUByRequestedTime": casesForICUByRequestedTimeImpact,
                    "casesForVentilatorsByRequestedTime": casesForVentilatorsByRequestedTimeImpact
                    },
                "severeImpact": {
                    "currentlyInfected": currentlyInfectedSevere,
                    "infectionsByRequestedTime": infectionsByRequestedTimeSevere,
                    "severeCasesByRequestedTime": infectionsByRequestedTimeSevere,
                    "hospitalBedsByRequestedTime": hospitalBedsByRequestedTimeSevere,
                    "casesForICUByRequestedTime": casesForICUByRequestedTimeSevere,
                    "casesForVentilatorsByRequestedTime": casesForVentilatorsByRequestedTimeSevere
                    }
                }
          }

    return output


if __name__ == '__main__':
    data = json.loads(open("src/input.json").read())
    output = estimator(data)
    print(output)
