#ifndef PROJET_SENSOR_SOURCE_H
#define PROJET_SENSOR_SOURCE_H

#include <projet/series.h>

enum { SENSOR_SOURCE_UPDATED_AT_SIZE = 40 };

typedef struct {
    char updated_at[SENSOR_SOURCE_UPDATED_AT_SIZE];
    MeasureSeries points;
} SensorDataset;

void sensor_dataset_init(SensorDataset *dataset);
void sensor_dataset_clear(SensorDataset *dataset);

/*
 * Ces deux fonctions sont l'unique point de raccordement de la bibliotheque
 * HTTP/JSON fournie par l'enseignant. Elles remplissent un jeu de mesures
 * typées sans exposer JSON ni le reseau au reste du projet.
 */
int sensor_source_load_url(const char *url, SensorDataset *dataset);
int sensor_source_load_file(const char *path, SensorDataset *dataset);
const char *sensor_source_last_error(void);

#endif
