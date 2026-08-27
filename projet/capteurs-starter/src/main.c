#include <stdio.h>
#include <string.h>

#include <projet/report.h>
#include <projet/sensor_source.h>

#define SENSORS_URL "https://tribequa.org/assets/data/sensors-history.json"

static void usage(const char *program)
{
    fprintf(stderr, "Usage: %s [--url URL | --file FICHIER]\n", program);
}

int main(int argc, char *argv[])
{
    SensorDataset dataset;
    int loaded;

    sensor_dataset_init(&dataset);

    if (argc == 1) {
        loaded = sensor_source_load_url(SENSORS_URL, &dataset);
    } else if (argc <= 3 && strcmp(argv[1], "--url") == 0) {
        loaded = sensor_source_load_url(argv[2], &dataset);
    } else if (argc == 3 && strcmp(argv[1], "--file") == 0) {
        loaded = sensor_source_load_file(argv[2], &dataset);
    } else {
        usage(argv[0]);
        sensor_dataset_clear(&dataset);
        return 2;
    }

    if (!loaded) {
        fprintf(stderr, "Impossible de charger les capteurs: %s\n",
            sensor_source_last_error());
        sensor_dataset_clear(&dataset);
        return 1;
    }

    sensor_report_print(stdout, &dataset);
    sensor_dataset_clear(&dataset);
    return 0;
}
