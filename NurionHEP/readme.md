## Nurion HEP-CNN  
### 1. Raw Data Sample location  
Path: KISTI ui20 Machine: **/hcp/data/data02/jwkim2/WORK/Nurion/preprocess/RPV_jhg_v0.h5(for BKG: QCD.h5)**  

### 2. Preprocess1 (N01_split_data.py)  
1) Combine Background and Signal, 2) suffle them, and  3) split them as train and validation dataset  
The output are train.h5 and val.h5  
Default set: 10,000 BKG 10,000 Signal --> 16,000 train 4,000 validation  

### 3. Visualize (N02_Visualization.ipynb)  
Visualize signal and background data for HCAL,ECAL, and Tracker  
This codes were written as Ipython  
If you cannot see it, please try copying url here:https://nbviewer.jupyter.org/

