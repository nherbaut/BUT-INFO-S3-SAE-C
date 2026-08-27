#ifndef PROJET_STATISTICS_H
#define PROJET_STATISTICS_H

#include <stddef.h>

#include <projet/series.h>

typedef enum {
    TEMPERATURE_INDOOR,
    TEMPERATURE_OUTDOOR
} TemperatureKind;

typedef struct {
    size_t count;
    double minimum;
    double maximum;
    double average;
} TemperatureStatistics;

/* Renvoie 0 si la serie est vide ou si un argument est invalide. */
int temperature_statistics_compute(
    const MeasureSeries *series,
    TemperatureKind kind,
    TemperatureStatistics *statistics
);

/* Moyenne de (temperature interieure - temperature exterieure). */
int temperature_average_gap(const MeasureSeries *series, double *gap);

#endif
