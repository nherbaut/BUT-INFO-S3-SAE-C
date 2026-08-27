#include <assert.h>
#include <math.h>
#include <string.h>

#include <projet/sensor_source.h>

int main(void)
{
    SensorDataset dataset;

    sensor_dataset_init(&dataset);
    assert(sensor_source_load_file("tests/data/sensors-history.json", &dataset));
    assert(strcmp(dataset.updated_at, "2026-08-26T14:45:00.354680+02:00") == 0);
    assert(dataset.points.count == 3);
    assert(fabs(dataset.points.items[1].outdoor_temperature - 27.9) < 0.0001);
    sensor_dataset_clear(&dataset);
    return 0;
}
