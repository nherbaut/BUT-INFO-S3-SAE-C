#ifndef PROJET_REPORT_H
#define PROJET_REPORT_H

#include <stdio.h>

#include <projet/sensor_source.h>

void sensor_report_print(FILE *output, const SensorDataset *dataset);

#endif
