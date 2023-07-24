# USPNet


This is the  simplified inference code for paper 'USPNet: unbiased organism-agnostic and highly sensitive signal peptide predictor with deep protein language model'


We provide a pretrained-predicting header, and pretrained protein embeddings.<br>
Simply download all files and run prediction on test set.



## Local Environment Setup for running the test

First, download the repository and create the environment.<br>

### Create environment with conda
requirement
```
git clone https://github.com/JunboShen/USPNet.git
cd ./USPNet
conda env create -f ./environment.yml
```

### Download test set
[Test set](https://drive.google.com/file/d/1O-Uwo2HOk5H2IiyPHCqWiBCNX6MbPf4U/view?usp=sharing).<br>

### Download trained predictive model
[Prediction head](https://drive.google.com/file/d/1ZNDZ_ulmeZzol7u1_fMEODe7nvtWLFqh/view?usp=sharing)

[Without organism group information](https://drive.google.com/file/d/1YfFmGZNEhl4q86dljPeWub1WLLCH7VNx/view?usp=drive_link).<br>

### Download embeddings
[MSA embedding for test set](https://drive.google.com/file/d/1FPPKO9OaAdB0K9heUqQuymmqMN4m_XI3/view?usp=sharing).<br>

### Download categorical test data
[Categorical test data](https://drive.google.com/file/d/1r9sw5t3BVzYsw4RZG48N-7Y621pQFHJK/view?usp=sharing).<br>

## Usage
Put all the downloaded files into the same folder.<br>
Then run:
```
python data_processing.py
python predict.py

unzip test_data.zip
python test.py
```
For data without organism group information, please run:
```
python predict.py no_group_info

python test.py no_group_info
```

