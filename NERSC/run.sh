

StartTime=$(date +%s)

##### -- DATA preprocessing + Train 

#python train.py --nb-epochs 20 --nb-train-events 412416 --batch-size 512 ./train.h5 ./val.h5 3ch-CNN  # Full set
#python train.py --nb-epochs 10 --nb-train-events 100000 --nb-test-events 10000 --batch-size 512 ./train.h5 ./val.h5 3ch-CNN
python train.py --nb-epochs 10 --nb-train-events 20000 --nb-test-events 1000 --batch-size 512 ./train.h5 ./val.h5 3ch-CNN




#####  ---1. DATA preprocessing(Run this before "2.Train Only" )
#python preprocess.py --nb-train-events 20000 --nb-test-events 1000 ./train.h5 ./val.h5 3ch-CNN

##### --- 2. Train Only( Run this afeter "1.DATA preprocessing" )
#python train_only.py --nb-epochs 10 --nb-train-events 20000 --nb-test-events 1000 --batch-size 512 ./Preprocessed_Train.h5 ./Preprocessed_Val.h5 3ch-CNN

EndTime=$(date +%s)

echo "It takes $(($EndTime - $StartTime)) seconds to complete this task."

