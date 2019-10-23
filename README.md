# Regression for Pricing of LEGO Sets
FIS Mod4 Project

*by Phillip Busko & Sorin Luca*

**Project Presentation**
[Google Docs](https://docs.google.com/presentation/d/1h-8MnhFCwu_dVXVftjegIf_1CB65Z5tXdPTkiSW0yjo/edit?usp=sharing)

## Summary

Predict the launching price of various LEGO sets based on available information such as:

- launch year
- number of total pieces
- number of different pieces
- the colors of the pieces
- the theming of the set

## Methodology

We have implemented two algorithms for the regression:

1. *Linear Regression* (the scikit-learn implementation).

2. *Support Vector Regression* (SVR, the scikit-learn implementation) with
both linear and radial basis function (RBF) kernels.

**Data** was obtained from two sources:

1. [brickset.com](https://brickset.com)

2. [kaggle.com](https://www.kaggle.com/rtatman/lego-database)

## Results

Both the linear regression and SVR (with linear kernel) models were able
to fit the launch price with a $R^2$ of about 0.86. The SVR with
an RBF kernel was slightly better with an $R^2$ of about 0.89.

The number of total parts and the number of different parts are the most
important independent variables for this problem.

## Work breakdown

- **Data**: Phil scrapped the brickset website, while Sorin processed and
merged the kaggle dataset. Both cleaned and inspected the data.

- **Modeling**: Phil performed the linear regression analysis, while
Sorin performed the SVR analysis.
