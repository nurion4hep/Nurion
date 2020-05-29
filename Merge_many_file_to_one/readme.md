### Manual  

1. Make following directories:  
- pre_train: Directory for unmerged train datasets  
- pre_val: Directory for unmerged validation datasets  
- pre_test: Directory for unmerged test datasets  
- dest_train: Directory for output (merged) train dataset  
- dest_val: Directory for output (merged) validation dataset  
- dest_test: Directory for output (merged) test dataset  

2. Run 
```bash
source run_all_merge.sh  
```  

#### The source code read pre_X directories and output merged files on dest_X directories  
#### Please empty the dest directories before start mergeing   
