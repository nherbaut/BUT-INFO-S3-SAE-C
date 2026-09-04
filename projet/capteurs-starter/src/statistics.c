#include <projet/statistics.h>

/**
 * Calcule les statistiques d'une seule temperature dans une serie deja
 * construite. Cette fonction ne doit ni allouer de memoire ni modifier la
 * serie : au jalon S3, les mesures sont fournies par un tableau sur la pile.
 *
 * Etapes attendues :
 *
 * 1. Refuser `series == NULL`, `statistics == NULL`, une serie vide, ou une
 *    serie incoherente (`series->items == NULL` alors que `series->count > 0`).
 * 2. Refuser une valeur de `kind` differente de TEMPERATURE_INDOOR et
 *    TEMPERATURE_OUTDOOR.
 * 3. Pour chaque element de `series->items`, choisir soit
 *    `indoor_temperature`, soit `outdoor_temperature` selon `kind`.
 * 4. Initialiser minimum, maximum et la somme avec la premiere valeur, puis
 *    parcourir les valeurs restantes pour mettre a jour minimum, maximum et
 *    la somme.
 * 5. En cas de succes, affecter `statistics->count`, `statistics->minimum`,
 *    `statistics->maximum` et `statistics->average` (somme / count), puis
 *    retourner 1. Retourner 0 dans tous les cas invalides.
 */
int temperature_statistics_compute(
    const MeasureSeries *series,
    TemperatureKind kind,
    TemperatureStatistics *statistics
)
{
    (void)series;
    (void)kind;
    (void)statistics;

    /* TODO S3 : suivre les etapes decrites au-dessus. */
    return 0;
}

int temperature_average_gap(const MeasureSeries *series, double *gap)
{
    (void)series;
    (void)gap;

    /* TODO S3: calculer la moyenne de temperature interieure - exterieure. */
    return 0;
}
