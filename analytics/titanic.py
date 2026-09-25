import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
print(f"all packages imported successfully")
df=sns.load_dataset("titanic")
print(df)
df.shape
df.info()
df.isnull().sum()
df.describe()
df.isna().mean()*100
df.to_csv("titanic.csv", index=False)
print(f"File successfully saved to: {"titanic.csv"}")
# Clean Missing Values #
df_clean = df.drop(columns=["deck"])
df_clean = df_clean.dropna(subset=["embarked", "embark_town"])
df_clean['age'] = df_clean['age'].fillna(df_clean['age'].median())
print(df_clean.info())
# histplot for both age and fare #
sns.histplot(data=df_clean, x="age", kde=True, y = "fare", color="skyblue")
plt.title("Distribution of Age (Histogram)")
plt.xlabel("Age (Years)")

plt.tight_layout()
plt.show()

# Box plot for both age and fare #
sns.boxplot(data=df_clean, x="age", y = "fare", color="lightgreen")
plt.title("Detection of Age Outliers (Box Plot)")
plt.xlabel("Age (Years)")

plt.tight_layout()
plt.show()

# IQR Calculation #
for col in ['age', 'fare']:
    q1 = df_clean[col].quantile(0.25)
    q3 = df_clean[col].quantile(0.75)
    iqr = q3 - q1
    outliers = df_clean[(df_clean[col] <  (q1 - 1.5*iqr)) |(df_clean[col] > (q3 + 1.5*iqr))]
    print(f"IQR Outliers for {col}: {len(outliers)}")

# mean, mode, meadian for fare #
print(f"The mean fare is: {df_clean['fare'].mean():.2f}")
print(f"The median fare is: {df_clean['fare'].median():.2f}")
print(f"The mode fare is: {df_clean['fare'].mode()[0]:.2f}")

# survival percentage by class and gender #
pclass_survival = df_clean.groupby('pclass')['survived'].mean() * 100
print("Survival Percentage by Class:")
print(pclass_survival.round(2).astype(str) + '%')
sex_survival = df_clean.groupby('sex')['survived'].mean() * 100
print("\nSurvival Percentage by Gender:")
print(sex_survival.round(2).astype(str) + '%')
combined_survival = df_clean.groupby(['pclass', 'sex'])['survived'].mean() * 100
print("\nSurvival Percentage by Class & Gender:")
print(combined_survival.round(2).astype(str) + '%')

# correlation matrix #
numeric_cols = ['survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']
df_clean_filtered = df_clean[numeric_cols]
correlation_matrix = df_clean_filtered.corr()
print("--- 6x6 Correlation Matrix ---")
print(correlation_matrix.round(3))

plt.figure(figsize=(8,6))
sns.boxplot(data=df_clean, x="survived", y = "age", hue = 'sex', color="red")
plt.title("Age Vs Survival by Sex")
plt.tight_layout()
plt.show()
sns.barplot(data=df_clean, x="pclass", y = "survived", hue = 'sex', color="yellow")
plt.title("Survival by pclass and sex")
plt.tight_layout()
plt.show()
sns.scatterplot(data=df_clean, x="age", y = "fare", hue = 'survived', color="brown")
plt.title("Age Vs fare by survival")
plt.tight_layout()
plt.show()
sns.barplot(data=df_clean, x="embarked", y = "survived", hue = 'class', color="pink")
plt.title("survival by Embarked and Class")
plt.tight_layout()
plt.show()
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
df1 = sns.load_dataset("titanic")
df1 = df1.dropna(subset=['embarked'])
X = df1[['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked']]
y = df1['survived']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
numeric_cols = ['age', 'fare', 'sibsp', 'parch', 'pclass']
cat_cols = ['sex', 'embarked']
