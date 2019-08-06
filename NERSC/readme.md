## NERSC HEP-CNN 코드입니다.  
#### Code_Ref: https://drive.google.com/drive/folders/1EZ8l9cevPTEc9-tHRT0NH-sfbgvqSCXm  
#### Data_Ref: https://docs.nersc.gov/analytics/machinelearning/science-use-cases/hep-cnn  
---
### 1. 데이터 샘플 다운로드  
```bash
wget https://portal.nersc.gov/project/mpccc/wbhimji/RPVSusyData/train.h5
wget https://portal.nersc.gov/project/mpccc/wbhimji/RPVSusyData/test.h5
wget https://portal.nersc.gov/project/mpccc/wbhimji/RPVSusyData/val.h5
```  

### 2. 코드 설명  
1) 데이터 전처리와 학습 한번에 다 돌리기  
run.sh 로 train.py 코드를 실행합니다.  

2) 데이터 전처리후 학습 하기.(코드분리)  
run.sh 로 preprocess.py 를 먼저 실행 한 후, run.sh 로 train_only.py를 실행합니다.  

3) ROC curve 그리기  
ROC.py 실행: 학습 코드의 output과 val.h5를 가지고, ROC curve를 그리고, AUC 값을 구합니다.

--- 3. Horovod를 이용한 분산처리  
1) 샘플 다운로드 후 run.sh를 이용해서 preprocess.py코드 돌리기 (전처리)  
2) horovod 디렉토리로 이동, run.sh를 이용해서 train_only.py코드 돌리기 (학습)  
3) 1-3 의 코드로 ROC curve 그리기

