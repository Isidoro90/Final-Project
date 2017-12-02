import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import statsmodels.formula.api as smf

df = pd.read_csv("mega_data.csv", index_col = "id")
df = df.rename(columns = {"TRIP DURATION": "duration","FROM STATION ID":"station_id"})

## Plot of probability desity
sns.distplot(df["probability"])
plt.title("Histogram of Probability Density")
plt.savefig("probability_histogram.png")
plt.show()

## Plot of Outliers
sns.boxplot(y = df["probability"])
plt.title("Outliers in probability of trips taken")
plt.savefig("outliers_boxplot.png")
plt.show()

## Scatter Plot probability vs months
sns.regplot(x = df["month"], y = df["probability"], x_bins = 30, fit_reg = False)
plt.title("Probability of trips vs Months")
plt.savefig("scatter_prob_month.png")
plt.show()

## Regression
ols = smf.ols(formula = "probability ~ med_income_tract + high_income_tract + male + age + miles + duration + \
                          high_income_tract + office_early + office_afternoon + nighters + C(month)",
                    data = df)
model = ols.fit()
print(model.summary())

## Plot of residuals vs fitted values
sns.regplot(x = pd.Series(model.fittedvalues, name = "Fitted"), \
                y = pd.Series(model.resid, name = "Residual"), scatter_kws = {"alpha" : 0.1}, order = 2, x_bins = 60)
plt.title("Residuals vs Fitted Values")
plt.savefig("resid_fitt_graph.png")
plt.show()
