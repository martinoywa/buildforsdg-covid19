import math


def timeEstimateDays(periodType, timeToElapse):
    """
        Takes in period type and time to elapse
        and returns the days equivalent.
    """
    if periodType.lower() == "days":
        days = timeToElapse
    elif periodType.lower() == "weeks":
        days = 7 * timeToElapse
    else:
        days = 30 * timeToElapse

    return days


def estimator(data):
    """
        Takes input data and returns it in a
        specified format.
    """
    currentlyInfectedImpact = int(data["reportedCases"] * 10)
    currentlyInfectedSevere = int(data["reportedCases"] * 50)

    days = timeEstimateDays(data["periodType"], data["timeToElapse"])

    infectionsByRequestedTimeImpact = currentlyInfectedImpact * (2 ** int(days/3))
    infectionsByRequestedTimeSevere = currentlyInfectedSevere * (2 ** int(days/3))

    severeCasesByRequestedTimeImpact = int(0.15 * infectionsByRequestedTimeImpact)
    severeCasesByRequestedTimeSevere = int(0.15 * infectionsByRequestedTimeSevere)

    availableBeds = (0.35 * data["totalHospitalBeds"])

    hospitalBedsByRequestedTimeImpact = (availableBeds - severeCasesByRequestedTimeImpact)
    hospitalBedsByRequestedTimeSevere = (availableBeds - severeCasesByRequestedTimeSevere)

    casesForICUByRequestedTimeImpact = int(0.05 * infectionsByRequestedTimeImpact)
    casesForICUByRequestedTimeSevere = int(0.05 * infectionsByRequestedTimeSevere)

    casesForVentilatorsByRequestedTimeImpact = int(0.02 * infectionsByRequestedTimeImpact)
    casesForVentilatorsByRequestedTimeSevere = int(0.02 * infectionsByRequestedTimeSevere)

    dollarsInFlightImpact = int((infectionsByRequestedTimeImpact * data["region"]["avgDailyIncomePopulation"] * data["region"]["avgDailyIncomeInUSD"]) / days)
    dollarsInFlightSevere = int((infectionsByRequestedTimeSevere * data["region"]["avgDailyIncomePopulation"] * data["region"]["avgDailyIncomeInUSD"]) / days)


    output = {
            "data": data,
            "impact": {
                "currentlyInfected": currentlyInfectedImpact,
                "infectionsByRequestedTime": infectionsByRequestedTimeImpact,
                "severeCasesByRequestedTime": severeCasesByRequestedTimeImpact,
                "hospitalBedsByRequestedTime": hospitalBedsByRequestedTimeImpact,
                "casesForICUByRequestedTime": casesForICUByRequestedTimeImpact,
                "casesForVentilatorsByRequestedTime": casesForVentilatorsByRequestedTimeImpact,
                "dollarsInFlight": dollarsInFlightImpact},
            "severeImpact": {
                "currentlyInfected": currentlyInfectedSevere,
                "infectionsByRequestedTime": infectionsByRequestedTimeSevere,
                "severeCasesByRequestedTime": severeCasesByRequestedTimeSevere,
                "hospitalBedsByRequestedTime": hospitalBedsByRequestedTimeSevere,
                "casesForICUByRequestedTime": casesForICUByRequestedTimeSevere,
                "casesForVentilatorsByRequestedTime": casesForVentilatorsByRequestedTimeSevere,
                "dollarsInFlight": dollarsInFlightSevere}
            }

    return output
