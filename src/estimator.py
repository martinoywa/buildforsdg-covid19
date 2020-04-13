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

    # get days
    days = timeEstimateDays(data["periodType"], data["timeToElapse"])

    # Challenge 1
    # Currently infected estimates
    currentlyInfectedImpact = int(data["reportedCases"] * 10)
    currentlyInfectedSevere = int(data["reportedCases"] * 50)

    # Infections by requested time estimates
    infectionsByRequestedTimeImpact = currentlyInfectedImpact * \
        (2 ** int(days/3))
    infectionsByRequestedTimeSevere = currentlyInfectedSevere * \
        (2 ** int(days/3))

    # Challenge 2
    # Severe positive cases estimates requiring hospitalization
    severeCasesByRequestedTimeImpact = \
        int(0.15 * infectionsByRequestedTimeImpact)
    severeCasesByRequestedTimeSevere = \
        int(0.15 * infectionsByRequestedTimeSevere)

    # Available beds
    availableBeds = (0.35 * data["totalHospitalBeds"])

    # Hospital beds by requested time estimates
    hospitalBedsByRequestedTimeImpact = \
        int(availableBeds - severeCasesByRequestedTimeImpact)
    hospitalBedsByRequestedTimeSevere = \
        int(availableBeds - severeCasesByRequestedTimeSevere)

    # Challenge 3
    # severe positive cases that will require ICU care estimates
    casesForICUByRequestedTimeImpact = \
        int(0.05 * infectionsByRequestedTimeImpact)
    casesForICUByRequestedTimeSevere = \
        int(0.05 * infectionsByRequestedTimeSevere)

    # severe positive cases that will require ventilators estimates
    casesForVentilatorsByRequestedTimeImpact = \
        int(0.02 * infectionsByRequestedTimeImpact)
    casesForVentilatorsByRequestedTimeSevere = \
        int(0.02 * infectionsByRequestedTimeSevere)

    # estimate how much money the economy is likely to lose daily
    dollarsInFlightImpact = \
        int((infectionsByRequestedTimeImpact *
            data["region"]["avgDailyIncomePopulation"] *
            data["region"]["avgDailyIncomeInUSD"]) / days)
    dollarsInFlightSevere = \
        int((infectionsByRequestedTimeSevere *
            data["region"]["avgDailyIncomePopulation"] *
            data["region"]["avgDailyIncomeInUSD"]) / days)

    output = {
            "data": data,
            "impact": {
                "currentlyInfected": currentlyInfectedImpact,
                "infectionsByRequestedTime": infectionsByRequestedTimeImpact,
                "severeCasesByRequestedTime": severeCasesByRequestedTimeImpact,
                "hospitalBedsByRequestedTime":
                    hospitalBedsByRequestedTimeImpact,
                "casesForICUByRequestedTime": casesForICUByRequestedTimeImpact,
                "casesForVentilatorsByRequestedTime":
                    casesForVentilatorsByRequestedTimeImpact,
                "dollarsInFlight": dollarsInFlightImpact},
            "severeImpact": {
                "currentlyInfected": currentlyInfectedSevere,
                "infectionsByRequestedTime": infectionsByRequestedTimeSevere,
                "severeCasesByRequestedTime": severeCasesByRequestedTimeSevere,
                "hospitalBedsByRequestedTime":
                    hospitalBedsByRequestedTimeSevere,
                "casesForICUByRequestedTime": casesForICUByRequestedTimeSevere,
                "casesForVentilatorsByRequestedTime":
                    casesForVentilatorsByRequestedTimeSevere,
                "dollarsInFlight": dollarsInFlightSevere}
            }

    return output
