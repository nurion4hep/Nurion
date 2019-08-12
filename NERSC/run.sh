

StartTime=$(date +%s)

### --train.py
#python train.py --nb-epochs 20 --nb-train-events 412416 --batch-size 512 ./train.h5 ./val.h5 3ch-CNN  # Full set
#python train.py --nb-epochs 10 --nb-train-events 100000 --nb-test-events 10000 --batch-size 512 ./train.h5 ./val.h5 3ch-CNN
#python train.py --nb-epochs 10 --nb-train-events 20000 --nb-test-events 1000 --batch-size 512 ./train.h5 ./val.h5 3ch-CNN


### ---preprocess.py
#python preprocess.py --nb-train-events 100000 --nb-test-events 10000 ./train.h5 ./val.h5 3ch-CNN


### ---preprocess_TFD.py
#python preprocess_TFD.py --nb-train-events 100000 --nb-test-events 10000 ./train.h5 ./val.h5 3ch-CNN



### --train_only.py
python train_only.py --nb-epochs 10 --nb-train-events 20000 --nb-test-events 1000 --batch-size 512 ./Preprocessed_Train.h5 ./Preprocessed_Val.h5 3ch-CNN


### --train_only_v2.py HDF5Matrix test
#python train_only_v2.py --nb-epochs 10 --nb-train-events 20000 --nb-test-events 1000 --batch-size 512 ./Preprocessed_Train.h5 ./Preprocessed_Val.h5 3ch-CNN

python test.py

EndTime=$(date +%s)

echo "It takes $(($EndTime - $StartTime)) seconds to complete this task."

