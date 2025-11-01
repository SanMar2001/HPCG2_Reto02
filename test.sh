#!/bin/bash

> needle_timesV0.doc
> needle_timesV1.doc
> needle_timesV2.doc
> dboard_timesV0.doc
> dboard_timesV1.doc
> dboard_timesV2.doc

for j in {1..10}
do
    ./needlesV0 500000000 >> needle_timesV0.doc
    ./dboardV0 500000000 >> dboard_timesV0.doc
done

for j in {1..10}
do
    for k in 1 2 4 6 8
    do
        export OMP_NUM_THREADS=$k
        ./needlesV1 500000000 >> needle_timesV1.doc
        ./needlesV2 500000000 >> needle_timesV2.doc
        ./dboardV1 500000000 >> dboard_timesV1.doc
        ./dboardV2 500000000 >> dboard_timesV2.doc
    done
done