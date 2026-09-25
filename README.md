# AI_ML_CapstoneProject
Module 2

This module performs exploratory data analysis, classification modeling, imbalance handling, hyperparameter tuning, and regression using the Titanic dataset.
The dataset is downloaded from the kaggle and loaded using Seaborn in the VS Code.

Dataset Profiling:
> Dataset Dimensions
> Data types
> Summery statisticks
> Missing value percentages

Missing Value Treatment:
The Project follows these rules
> Less than 5% missing: drop the affected rows
> Between 5% and 30% missing:  impute the values
> Very high missingness: drop the column or create a "missing" category, with the decision explained

Univariate Analysis & Outliers:
> IQR Outlier Analysis
> Skewness Analysis

Survival Rates and Correlation Heatmap:
* By sex
* By pclass
* By sex and pclass
* Strongest correlation1 on pclass and fare
* Strongest correlation2 on survived and pclass

Multivariate Data Storytelling:
* Survival by pclass and sex
* Age Vs survival by sex
* Age Vs fare scatter
* Survival by embarked and pclass

