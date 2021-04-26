## Application of scalable deep learning in High energy physics usgin Nurion HPC ( Kisti )  

 - Abstract in Korean Physics Society (http://www.kps.or.kr/conference/event/content/program/search_result_abstract.php?id=1692&tid=162)
 - Current Github organization: (https://github.com/nurion4hep)


---
## AtoZ in Nurion  

1. Clone the offical Nurion repository  
```bash
git clone https://github.com/nurion4hep/HEP-CNN.git
```  

2. Install PyTorch and related libs in Nurion  
```bash
./HEP-CNN/scripts/install_torch_nurion.sh
```  
3. Setup Conda Environment  
```bash
source HEP-CNN/scripts/setup.sh
```  
 - h5py, pandas, matplotlib 등 python lib는 이 conda 환경 위에서 사용합시다   

4. Copy data from Jiwoong's directory to HEP-CNN/data
 - 64x64 iamge
    - Kisti server: /xrootd/store/user/jiwoong/HEP_CNN_OFFICIAL/trackpt_hdf5_32PU_64x64
    - Nurion : /scratch/hpc22a03/HEP-CNN/data/trackpt_hdf5_32PU_64x64

 - 224x224 image
    - Kisti server: /xrootd/store/user/jiwoong/HEP_CNN_OFFICIAL/trackpt_hdf5_32PU_224x224
    - Nurion : /scratch/hpc22a03/HEP-CNN/data/trackpt_hdf5_32PU_224x224
    
5. Set data path  
```bash
vi HEP-CNN/run/config.yml
```  

6. Make distributed-running script  
```bash
qsub run.sh
``` 
