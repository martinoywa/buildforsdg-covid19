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


def dollarsInFlight(infectionsByRequestedTimeImpact,
                    infectionsByRequestedTimeSevere, avgDailyIncomeInUSD,
                    avgDailyIncomePopulation, periodType, timeToElapse):
    """
     Takes as input the infections by requeste time for impact
     and severe, the average daily income and the population that
     get's this income, and period type time to elapse. Returns daily
     flight for both impact and severe.
    """
    if periodType == "days":
        impact = int((infectionsByRequestedTimeImpact *
                      avgDailyIncomePopulation *
                      avgDailyIncomeInUSD) / timeToElapse)
        severe = int((infectionsByRequestedTimeSevere *
                      avgDailyIncomePopulation *
                      avgDailyIncomeInUSD) / timeToElapse)
    elif periodType == "weeks":
        days = 7 * timeToElapse
        impact = int((infectionsByRequestedTimeImpact *
                      avgDailyIncomePopulation *
                      avgDailyIncomeInUSD) / days)
        severe = int((infectionsByRequestedTimeSevere *
                      avgDailyIncomePopulation *
                      avgDailyIncomeInUSD) / days)
    else:
        days = 30 * timeToElapse
        impact = int((infectionsByRequestedTimeImpact *
                      avgDailyIncomePopulation * avgDailyIncomeInUSD) / days)
        severe = int((infectionsByRequestedTimeSevere *
                      avgDailyIncomePopulation * avgDailyIncomeInUSD) / days)

    return impact, severe


def estimator(data):
    """
        Takes input data and returns it in a
        specified format.
    """
    currentlyInfectedImpact = int(data["reportedCases"] * 10)
    currentlyInfectedSevere = int(data["reportedCases"] * 50)

    days = timeEstimateDays(data["periodType"], data["timeToElapse"])

    infectionsByRequestedTimeImpact = currentlyInfectedImpact * (2 ** (math.floor(days/3)))
    infectionsByRequestedTimeSevere = currentlyInfectedSevere * (2 ** (math.floor(days/3)))

    severeCasesByRequestedTimeImpact = math.floor(0.15 * infectionsByRequestedTimeImpact)
    severeCasesByRequestedTimeSevere = math.floor(0.15 * infectionsByRequestedTimeSevere)

    availableBeds = marh.floor(0.35 * data["totalHospitalBeds"])

    hospitalBedsByRequestedTimeImpact = availableBeds - severeCasesByRequestedTimeImpact
    hospitalBedsByRequestedTimeSevere = availableBeds - severeCasesByRequestedTimeSevere

    # 5% of infectionsByRequestedTime that require ICU care.
    casesForICUByRequestedTimeImpact = int(0.05 *
                                           infectionsByRequestedTimeImpact)
    casesForICUByRequestedTimeSevere = int(0.05 *
                                           infectionsByRequestedTimeSevere)

    # 2% of infectionsByRequestedTime that require Ventilators.
    casesForVentilatorsByRequestedTimeImpact = \
        int(0.02 * infectionsByRequestedTimeImpact)
    casesForVentilatorsByRequestedTimeSevere = \
        int(0.02 * infectionsByRequestedTimeSevere)

    dollarsInFlightImpact, dollarsInFlightSevere = \
        dollarsInFlight(infectionsByRequestedTimeImpact,
                        infectionsByRequestedTimeSevere,
                        data["region"]["avgDailyIncomeInUSD"],
                        data["region"]["avgDailyIncomePopulation"],
                        data["periodType"], data["timeToElapse"])

    output = {
            "data": data,
            "impact": {
                "currentlyInfected": currentlyInfectedImpact,
                "infectionsByRequestedTime": infectionsByRequestedTimeImpact,
                "severeCasesByRequestedTime": severeCasesByRequestedTimeImpact,
                "hospitalBedsByRequestedTime": hospitalBedsByRequestedTimeImpact,

                "casesForICUByRequestedTime": casesForICUByRequestedTimeImpact,
                "casesForVentilatorsByRequestedTime":
                    casesForVentilatorsByRequestedTimeImpact,
                "dollarsInFlight": dollarsInFlightImpact},
            "severeImpact": {
                "currentlyInfected": currentlyInfectedSevere,
                "infectionsByRequestedTime": infectionsByRequestedTimeSevere,
                "severeCasesByRequestedTime": severeCasesByRequestedTimeSevere,
                "hospitalBedsByRequestedTime": hospitalBedsByRequestedTimeSevere,

                "casesForICUByRequestedTime": casesForICUByRequestedTimeSevere,
                "casesForVentilatorsByRequestedTime":
                    casesForVentilatorsByRequestedTimeSevere,
                "dollarsInFlight": dollarsInFlightSevere}
            }

    return output
