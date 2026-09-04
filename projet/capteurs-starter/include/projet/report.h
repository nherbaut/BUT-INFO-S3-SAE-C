#ifndef PROJET_REPORT_H
#define PROJET_REPORT_H

#include <stdio.h>

#include <projet/sensor_source.h>

/*
 * Le libelle appartient aux options : il est copie a l'initialisation et doit
 * donc etre libere avec sensor_report_options_clear.
 */
typedef struct {
    char *label;
} SensorReportOptions;

/* Renvoie 0 si un argument est invalide, si le CSV serait ambigu ou en cas
 * d'echec d'allocation. Si options est valide, options->label vaut NULL apres
 * un echec. */
int sensor_report_options_init(SensorReportOptions *options, const char *label);
void sensor_report_options_clear(SensorReportOptions *options);

void sensor_report_print(
    FILE *output,
    const SensorDataset *dataset,
    const SensorReportOptions *options
);

/* Ecrit l'en-tete puis une ligne de synthese CSV. Renvoie 0 en cas d'erreur
 * d'ecriture ou si les donnees ne permettent pas de calculer les statistiques.
 */
int sensor_report_write_csv(
    FILE *output,
    const SensorDataset *dataset,
    const SensorReportOptions *options
);

#endif
