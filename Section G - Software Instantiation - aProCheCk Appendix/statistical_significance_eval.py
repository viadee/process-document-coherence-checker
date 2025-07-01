import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import AnovaRM
import statsmodels.formula.api as smf

# Define the iterations as a dictionary
iterations = {
    'iteration_1': [
        [0.47, 0.47, 0.8, 0.47, 0.8],
        [0.62, 0.75, 0.62, 0.62, 0.62],
        [0.67, 0.83, 0.67, 0.67, 0.83],
        [0.83, 0.83, 0.67, 0.83, 0.83],
        [0.83, 0.58, 0.75, 0.5, 0.67],
        [1, 0.5, 0.83, 0.67, 0.9],
        [0.4, 0.9, 0.6, 0.65, 0.72],
        [0.94, 0.72, 0.72, 0.72, 0.2],
        [0.6, 0.3, 0.8, 0.2, 0.9],
        [0.9, 0.9, 0.9, 0.9, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ],
    'iteration_2': [
        [0.87, 0.8, 0.93, 0.93, 0.67],
        [0.62, 0.62, 0.62, 0.62, 0.62],
        [0.75, 0.67, 0.75, 0.67, 0.67],
        [0.67, 0.83, 0.79, 0.83, 0.67],
        [0.75, 0.67, 0.67, 0.83, 0.5],
        [1, 1, 1, 0.67, 0.5],
        [0.8, 0.9, 0.9, 0.9, 0.9],
        [0.72, 0.83, 0.94, 0.92, 0.72],
        [0.6, 0.4, 0.8, 0.6, 0.8],
        [0.9, 1, 1, 0.9, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ],
    'iteration_3': [
        [0.6, 0.73, 0.6, 0.73, 0.73],
        [0.75, 0.75, 1, 0.75, 0.75],
        [0.83, 0.58, 0.67, 0.67, 0.92],
        [0.83, 0.75, 0.67, 0.88, 0.75],
        [0.67, 0.75, 0.75, 0.75, 0.67],
        [0.83, 0.5, 0.83, 0.67, 0.5],
        [0.9, 0.85, 0.8, 0.9, 0.85],
        [0.94, 0.94, 0.94, 0.97, 0.92],
        [0.8, 0.9, 0.6, 0.6, 0.6],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ],
    'iteration_4': [
        [0.87, 0.87, 0.8, 0.87, 0.8],
        [0.75, 0.75, 0.75, 0.75, 1],
        [0.83, 0.67, 0.88, 0.83, 0.67],
        [0.96, 0.79, 0.75, 0.79, 0.79],
        [0.83, 0.75, 0.67, 0.75, 0.67],
        [0.83, 0.67, 0.67, 1, 0.83],
        [0.8, 0.85, 0.8, 0.85, 0.8],
        [0.78, 0.78, 0.72, 0.78, 0.72],
        [0.8, 0.9, 1, 0.8, 0.8],
        [0.8, 0.9, 0.7, 0.8, 0.9],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
}

# Convert the dictionary to a long format DataFrame
data = []
for iteration, data_sources in iterations.items():
    for ds_index, measurements in enumerate(data_sources):
        for measurement in measurements:
            data.append([iteration, ds_index, measurement])

df = pd.DataFrame(data, columns=['Iteration', 'DataSource', 'Accuracy'])

# Aggregate the data by averaging the accuracy for each data source within each iteration
df_agg = df.groupby(['Iteration', 'DataSource'], as_index=False).mean()

# Convert categorical variables
df_agg['Iteration'] = df_agg['Iteration'].astype('category')
df_agg['DataSource'] = df_agg['DataSource'].astype('category')

# Repeated Measures ANOVA
def repeated_measures_anova(df):
    model = AnovaRM(df, 'Accuracy', 'DataSource', within=['Iteration'])
    rm_anova = model.fit()
    print("Repeated Measures ANOVA Results:\n")
    print(rm_anova)
    print("\n")

# Linear Mixed-Effects Model
def linear_mixed_effects_model(df):
    model = smf.mixedlm("Accuracy ~ Iteration", df, groups=df["DataSource"])
    mixed_lm_result = model.fit()
    print("Linear Mixed-Effects Model Results:\n")
    print(mixed_lm_result.summary())
    print("\n")

# Execute the tests
repeated_measures_anova(df_agg)
linear_mixed_effects_model(df_agg)
