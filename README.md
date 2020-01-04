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

**1. Scrape Brickset:** Data was scraped using the requests and beautifulsoup libraries. Since there are thousands of sets available, the work was broken down by first getting the url of each set for each year. Then each url is visited, and it's data is scraped. The data fields available from this are: set-id, name, year, themes, minifig count, store price, used price, user rating, and set type. The next graph shows the set price distribution, with both the store price (the target variable), and the used price.

![](assets/set_price.png)

**2. Feature Engineering:** The kaggle data was joined with the basic data for additional features. Some of these features are readily availabe, while others were manufactured based on some guesses as to what factors might be contributing to establishing the store price. The new data fields are: total number of pieces, number of different pieces, primary color, secondary color, and number of different colors. 

**3. Algorithm Preparation:** First, some filtering was done on the rows, so that LEGO non-sets, such as clothing items, are removed from the data. Also, any rows without store price data are eliminated. The categorical columns (color, themes) were aggregated into more coarse-grain values and then one-hot encoded. Finally, all the columns are standardized with sklearn.preprocessing.StandardScaler.

**4. Linear Regression:** Linear regression was run with 3 different scenarios: baseline, ridge and lasso. Each algorithm was run with a grid search to tune the regularization hyper-parameter lambda. Each run was cross-validated with 5 folds. The next graph shows the CV test scores, where the error bars are the standard deviation of the CV tests.

![](assets/linear_algorithms.png)

**5. Support Vector Machine:** SVR was run with 2 different kernels, linear and RBF. The baseline R<sup>2</sup> was 0.85, and by tuning the RBF hyper-parameters, the R<sup>2</sup> was raised to 0.89.

**6. Interpretation:** Since no dimensionality reduction techniques were used, the model retained interpretability of the beta-coeficients. The linear regression yielded the following feature importances (which had to be massaged back together since some were one-hot encoded):

![](assets/feature_importance.png)

