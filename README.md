# Data Profile
## Final Proect of CS576, University of Rochester. Teammate： Moshiul Azam

Aim to generate basic information for each data table in the open data lake, focus on sensitive attributes, race, gender, country, age, .etc

Sherlock is used to predict header to filter out sensitive attributes. Currently, I just add MUP, Maximal Uncoverd Pattern, to the result table, future I might visualize the output. MUP is the defined as same as Assessing and Remedying Coveragefor a Given Dataset, Abolfazl Asudeh, Zhongjun Jin, H. V. Jagadish, 2019.
Here a value combination of sensitive attributes is said to be uncovered, if count of it is <=25, since the paper above indicates that usually appearance of a tuple from 20 to 40 times, a learning algorithm can fetch out features.

# Future work:
A web presentation that with visualization.
A search fucntion that can help users find their target datasets and provide information of these datasets.
A information combination among different data tables.

# Sherlock: data and deployment scripts.

Sherlock is a deep-learning approach to semantic data type detection which is important for, among others, data cleaning and schema matching. This repository provides data and scripts to guide the deployment of Sherlock.


### Installation of package
This project is not installable through PyPI yet. For now, you can install Sherlock by cloning this repository, navigating to the root directory of this repository and run `pip install .`.


### Demonstration of usage
A notebook can be found in `notebooks/` which shows how to download the raw and preprocessed data files, and demonstrates the usage of Sherlock.


### Data
Data can be downloaded using the `download_data()` function in the `helpers` module.
This will download 3.6GB of data into the `data` directory.


### Making predictions for new dataset
To use the pretrained model for generating predictions for a new dataset, features can be extracted using the `features.preprocessing` module. Please note that extracting features can take quite long due to the unoptimized code.
With the resulting feature vectors, the pretrained Sherlock model can be deployed on the dataset.

To retrain Sherlock, you are currently restricted to using 78 classes to comply with the original model architecture. The code of the neural network behind Sherlock will be added soon.


### Retraining Sherlock
Sherlock can be retrained by using the code in the `deploy.train_sherlock` module.



## Project Organization
    ├── data   <- Placeholder directory to download data into.

    ├── docs   <- Files for https://sherlock.media.mit.edu landing page.

    ├── models  <- Trained models.
        ├── sherlock_model.json
        └── sherlock_weights.h5

    ├── notebooks   <- Notebooks demonstrating the deployment of Sherlock using this repository.
            └── adult.csv, a commone dataset as test input file
            └── adult.xlsx, the output file of adult.csv input
            └── info.xlsx, the output file of data tables in open data lake, not complete information of all tables
            └── processed.txt, track which tables have been processed
            └── report, the folder containing the report output file of metadata generator, some of files are > 100 MB, which cannot be uploaded to Github
            
            └── Metadata_Generation_Twang.ipynb, metadata generation process of data tables
                └── profiling.py, necessary file to realize functions in 576_Twang.ipynb
            
            └── Dataset Nutrition Label_Mazam.ipynb, nutrition label generation process
                └── ObtainEquivalences.py
                └── Prune.py
                └── GetFDs.py
                └── binaryRepr.py
                └── Apriori_Gen.py
                └── testf.py
            └── ex.html, output of Nutrition label generator 
            └── ex.txt, output of Nutrition label generator
            └── readme.txt, readme for Nutrition label generator

    ├── sherlock  <- Package files.
        ├── deploy  <- Files and modules to (re)train models on new data and generate predictions.
            └── classes_sherlock.npy
            └── model_helpers.py
            └── predict_sherlock.py
            └── train_sherlock.py
        ├── features     <- Files to turn raw data, storing raw data columns, into features.
            ├── feature_column_identifiers   <- Directory with feature names categorized by feature set.
               └── char_col.tsv
               └── par_col.tsv
               └── rest_col.tsv
               └── word_col.tsv
            └── bag_of_characters.py
            └── bag_of_words.py
            └── par_vec_trained_400.pkl
            └── paragraph_vectors.py
            └── preprocessing.py
            └── word_embeddings.py
        ├── helpers.py     <- Supportive modules.

------------
