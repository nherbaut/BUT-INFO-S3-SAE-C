#include <projet/statistics.h>

int temperature_statistics_compute(
    const MeasureSeries *series,
    TemperatureKind kind,
    TemperatureStatistics *statistics
)
{
    (void)series;
    (void)kind;
    (void)statistics;

    /* TODO S3: calculer minimum, maximum et moyenne pour la grandeur demandee. */
    return 0;
}

int temperature_average_gap(const MeasureSeries *series, double *gap)
{
    (void)series;
    (void)gap;

    /* TODO S3: calculer la moyenne de temperature interieure - exterieure. */
    return 0;
}
