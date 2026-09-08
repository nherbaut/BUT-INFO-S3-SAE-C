#include "projet/series.h"

void measure_series_init(MeasureSeries *series)
{
    series->items = NULL;
    series->count = 0;
    series->capacity = 0;
}

int measure_series_append(MeasureSeries *series, TemperatureMeasure measure)
{
    (void)series;
    (void)measure;

    /* TODO S4: malloc lors de la premiere insertion, puis realloc si besoin. */
    return 0;
}

void measure_series_clear(MeasureSeries *series)
{
    (void)series;

    /* TODO S4: liberer le tableau et remettre la serie dans son etat initial. */
}
