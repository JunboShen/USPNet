# USPNet


This repository contains code for the paper 'USPNet: unbiased organism-agnostic and highly sensitive signal peptide predictor with deep protein language model'


You can use either USPNet or USPNet-fast to predict the signal peptide of a protein sequence.<br>
We also provide MSA Transformer embeddings of the benchmark set as a demo.<br>




## Local Environment Setup for running the test

First, download the repository and create the environment.<br>

### Create an environment with conda
requirement
```bash
git clone https://github.com/JunboShen/USPNet.git
cd ./USPNet
conda env create -f ./environment.yml
```

### Download the benchmark set
[Test set](https://drive.google.com/file/d/1O-Uwo2HOk5H2IiyPHCqWiBCNX6MbPf4U/view?usp=sharing).<br>

### Download categorical benchmark data
[Categorical test data](https://drive.google.com/file/d/1r9sw5t3BVzYsw4RZG48N-7Y621pQFHJK/view?usp=sharing).<br>

### Download embeddings for the benchmark set
[MSA embedding for test set](https://drive.google.com/file/d/1FPPKO9OaAdB0K9heUqQuymmqMN4m_XI3/view?usp=sharing).<br>

### Download trained predictive models
[USPNet prediction head](https://drive.google.com/file/d/1ZNDZ_ulmeZzol7u1_fMEODe7nvtWLFqh/view?usp=sharing)

[USPNet prediction head (without organism group information)](https://drive.google.com/file/d/1YfFmGZNEhl4q86dljPeWub1WLLCH7VNx/view?usp=drive_link).

[USPNet-fast prediction head](https://drive.google.com/file/d/1eQMBVPvu3Nd7zEgLGinY09GUXbhn_LOy/view?usp=sharing).<br>


## Usage
Put all the downloaded files into the same folder.<br>

If you want to use USPNet on our benchmark set, please run:
```python
python data_processing.py
python predict.py

# categorical benchmark data
unzip test_data.zip
python test.py
```

Demo of USPNet on benchmark data without organism group information:
```python
python predict.py no_group_info

python test.py no_group_info
```

Demo of USPNet-fast on benchmark data:
```python
python predict_fast.py

python test_fast.py
```

To generate MSA embeddings on your own protein sequences and use USPNet to perform signal peptide prediction, please run:
```python
# MSA embedding generation
python data_processing.py [fasta_file] [msa_dir/]

# Prediction
python predict.py
```

If you want to use USPNet-fast to perform signal peptide prediction on your own protein sequences, please run:
```python
python predict_fast.py

```



