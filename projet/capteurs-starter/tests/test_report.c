#include <assert.h>
#include <stdio.h>
#include <string.h>

#include <projet/report.h>

int main(void)
{
    TemperatureMeasure measures[] = {
        {"2026-09-24T08:15:00+02:00", 27.3, 27.8, 56.3, 55.5},
        {"2026-09-24T08:20:00+02:00", 27.2, 27.9, 56.3, 55.5},
        {"2026-09-24T08:25:00+02:00", 27.5, 27.6, 56.9, 55.4}
    };
    SensorDataset dataset = {
        "2026-09-24T08:30:00+02:00",
        {measures, 3, 3}
    };
    SensorReportOptions options;
    FILE *output;
    char csv[512];
    char label[] = "Atelier capteurs";

    assert(!sensor_report_options_init(NULL, "Atelier"));
    assert(!sensor_report_options_init(&options, "Avec,virgule"));
    assert(!sensor_report_options_init(&options, "Avec\"guillemet"));
    assert(sensor_report_options_init(&options, label));
    label[0] = 'X';
    assert(strcmp(options.label, "Atelier capteurs") == 0);

    output = tmpfile();
    assert(output != NULL);
    assert(sensor_report_write_csv(output, &dataset, &options));
    assert(fflush(output) == 0);
    rewind(output);
    assert(fgets(csv, sizeof csv, output) != NULL);
    assert(strcmp(csv,
        "label,updated_at,count,indoor_minimum,indoor_maximum,indoor_average,"
        "outdoor_minimum,outdoor_maximum,outdoor_average,average_gap\n") == 0);
    assert(fgets(csv, sizeof csv, output) != NULL);
    assert(strcmp(csv,
        "Atelier capteurs,2026-09-24T08:30:00+02:00,3,27.20,27.50,27.33,"
        "27.60,27.90,27.77,-0.43\n") == 0);
    assert(fclose(output) == 0);

    sensor_report_options_clear(&options);
    assert(options.label == NULL);
    return 0;
}
