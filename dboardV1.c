// Version 1
// Using OpenMP to optimize

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <omp.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    long long n = atoll(argv[1]);
    if (n <= 0) return 1;

    const double factor = 1.0 / RAND_MAX;
    long long hits = 0;

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    #pragma omp parallel
    {
        unsigned int seed = time(NULL) ^ omp_get_thread_num();
        long long local_hits = 0;

        #pragma omp for nowait
        for (long long k = 0; k < n; ++k) {
            double x = rand_r(&seed) * factor;
            double y = rand_r(&seed) * factor;
            if (x*x + y*y <= 1.0) {
                ++local_hits;
            }
        }

        #pragma omp atomic
        hits += local_hits;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double pi_approx = 4.0 * (double)hits / (double)n;
    double elapsed = (end.tv_sec - start.tv_sec)
                   + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("%.9f\n", elapsed);
    return 0;
}