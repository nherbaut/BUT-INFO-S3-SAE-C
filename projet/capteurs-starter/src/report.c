#include <projet/report.h>

int sensor_report_options_init(SensorReportOptions *options, const char *label)
{
    (void)label;

    if (options != NULL) {
        options->label = NULL;
    }

    /* TODO S4 : verifier le libelle, le copier avec strlen/malloc/memcpy,
     * puis renvoyer 1. Refuser ',', '"', '\n' et '\r'. */
    return 0;
}

void sensor_report_options_clear(SensorReportOptions *options)
{
    (void)options;

    /* TODO S4 : liberer options->label et remettre le pointeur a NULL. */
}

void sensor_report_print(
    FILE *output,
    const SensorDataset *dataset,
    const SensorReportOptions *options
)
{
    (void)dataset;
    (void)options;

    /* TODO S4: afficher le rapport a partir des statistiques. */
    fputs("Rapport a implementer.\n", output);
}

int sensor_report_write_csv(
    FILE *output,
    const SensorDataset *dataset,
    const SensorReportOptions *options
)
{
    (void)output;
    (void)dataset;
    (void)options;

    /* TODO S4 : calculer les statistiques et ecrire l'en-tete CSV puis la
     * ligne de synthese. Utiliser fprintf et verifier ses valeurs de retour. */
    return 0;
}
