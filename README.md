# Regression for Pricing of LEGO Sets

The goal of this project is to predict the store price of new LEGO sets. That is, based on properties of the set (number of pieces, colors, themes, etc), we will predict the price at which the company will release the set. 

This project was created under the FlatIron School's Data Science Bootcamp, for the Module 4 project.

[Non-Technical Presentation (Google Slides)](https://docs.google.com/presentation/d/1h-8MnhFCwu_dVXVftjegIf_1CB65Z5tXdPTkiSW0yjo/edit?usp=sharing)

## Project Roadmap

**Contributors:** Phillip Busko & Sorin Luca

**Data Sources**
- [brickset.com](https://brickset.com)
- [kaggle.com](https://www.kaggle.com/rtatman/lego-database)

**Tasks**
- Scrape and clean data from brickset website *(PB)*
- Join kaggle data and run feature engineering *(SL)*
- Run linear regression for store price *(PB)*
- Run support vector regression for store price *(SL)*


## Results

Both the linear regression and SVR (with linear kernel) models were able to fit the launch price with a R<sup>2</sup> of about 0.86. The SVR with an RBF kernel was slightly better with a R<sup>2</sup> of about 0.89.

The number of total parts and the number of different parts are the most important independent variables for this problem.






## Methodology

We have implemented two algorithms for the regression:

1. *Linear Regression* (the scikit-learn implementation).

2. *Support Vector Regression* (SVR, the scikit-learn implementation) with
both linear and radial basis function (RBF) kernels.

**Data** was obtained from two sources:



## Work breakdown

- **Data**: Phil scrapped the brickset website, while Sorin processed and
merged the kaggle dataset. Both cleaned and inspected the data.

- **Modeling**: Phil performed the linear regression analysis, while
Sorin performed the SVR analysis.
