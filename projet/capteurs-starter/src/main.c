#include <stdio.h>
#include <string.h>

#include <projet/report.h>
#include <projet/sensor_source.h>

#define SENSORS_URL "https://tribequa.org/assets/data/sensors-history.json"
#define DEFAULT_CSV_PATH "rapport.csv"
#define DEFAULT_REPORT_LABEL "Rapport capteurs"

static void usage(const char *program)
{
    fprintf(stderr,
        "Usage: %s [--url URL | --file FICHIER] [--csv FICHIER] [--label TEXTE]\n",
        program);
}

typedef struct {
    const char *url;
    const char *file;
    const char *csv_path;
    const char *label;
} ProgramOptions;

static int parse_options(int argc, char *argv[], ProgramOptions *options)
{
    (void)argc;
    (void)argv;

    if (options == NULL) {
        return 0;
    }

    options->url = NULL;
    options->file = NULL;
    options->csv_path = DEFAULT_CSV_PATH;
    options->label = DEFAULT_REPORT_LABEL;

    /* TODO S2/S4 : parcourir argv avec une boucle. Accepter --url URL ou
     * --file FICHIER (au plus un), ainsi que --csv FICHIER et --label TEXTE,
     * dans n'importe quel ordre. Les deux derniers remplacent respectivement
     * DEFAULT_CSV_PATH et DEFAULT_REPORT_LABEL. Utiliser strcmp et refuser les
     * options inconnues, dupliquees ou incompletes. Sans source, l'URL par
     * defaut est utilisee. */
    return 1;
}

static int write_csv_report(
    const char *path,
    const SensorDataset *dataset,
    const SensorReportOptions *report_options
)
{
    (void)path;
    (void)dataset;
    (void)report_options;

    /* TODO S4 : ouvrir path avec fopen("w"), appeler
     * sensor_report_write_csv, detecter les erreurs (dont fclose), fermer le
     * fichier dans tous les cas et retourner 1 en cas de succes. */
    return 0;
}

int main(int argc, char *argv[])
{
    SensorDataset dataset;
    SensorReportOptions report_options;
    ProgramOptions options;
    int loaded;

    sensor_dataset_init(&dataset);

    if (!parse_options(argc, argv, &options)) {
        usage(argv[0]);
        return 2;
    }

    if (!sensor_report_options_init(&report_options, options.label)) {
        fprintf(stderr, "Libelle de rapport invalide ou memoire insuffisante.\n");
        return 1;
    }

    if (options.file != NULL) {
        loaded = sensor_source_load_file(options.file, &dataset);
    } else if (options.url == NULL) {
        loaded = sensor_source_load_url(SENSORS_URL, &dataset);
    } else {
        loaded = sensor_source_load_url(options.url, &dataset);
    }

    if (!loaded) {
        fprintf(stderr, "Impossible de charger les capteurs: %s\n",
            sensor_source_last_error());
        sensor_report_options_clear(&report_options);
        sensor_dataset_clear(&dataset);
        return 1;
    }

    sensor_report_print(stdout, &dataset, &report_options);
    /* Le stub TODO retourne toujours 0 avant son implementation. */
    // cppcheck-suppress knownConditionTrueFalse
    if (!write_csv_report(options.csv_path, &dataset, &report_options)) {
        fprintf(stderr, "Impossible d'ecrire le rapport CSV.\n");
        sensor_report_options_clear(&report_options);
        sensor_dataset_clear(&dataset);
        return 1;
    }

    sensor_report_options_clear(&report_options);
    sensor_dataset_clear(&dataset);
    return 0;
}
