#ifndef PROJET_SERIES_H
#define PROJET_SERIES_H

#include <stddef.h>

#include <projet/measure.h>

typedef struct {
    TemperatureMeasure *items;
    size_t count;
    size_t capacity;
} MeasureSeries;

void measure_series_init(MeasureSeries *series);
int measure_series_append(MeasureSeries *series, TemperatureMeasure measure);
void measure_series_clear(MeasureSeries *series);

#endif
