import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_csv('analysis.csv')
data['WC'] = data['WC'].fillna('none')
data = data.join(data.groupby('year')['combined ACPL'].mean(), on='year', rsuffix='_by_year')
wc_order = data.sort_values(by='combined ACPL_by_year')['WC'].drop_duplicates()
data['opening trunc'] = data['opening'].str[:16] # 23
print(data.sample(10))

plt.figure(figsize=(19, 9))
ax = sns.boxplot(data, x='year', y='combined ACPL', dodge=False, hue='WC', hue_order=wc_order)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_title('Combined ACPL by year')
ax.set_xlabel('Year')
ax.set_ylabel('Combined ACPL')
ax.legend(title='World champion')

plt.figure(figsize=(14, 6))
ax = sns.barplot(data, x='year', y='combined ACPL')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_title('Combined ACPL by year')
ax.set_xlabel('Year')
ax.set_ylabel('Combined ACPL')

plt.figure(figsize=(19,9))
sns.regplot(data, x='year', y='combined ACPL', scatter=False)
sns.scatterplot(data, x='year', y='combined ACPL', hue='WC')
ax.set_title('Combined ACPL by year')
ax.set_xlabel('Year')
ax.set_ylabel('Combined ACPL')


plt.figure(figsize=(14,6))
sns.regplot(data, x='year', y='white num moves')
ax.set_title('Number of moves by year')
ax.set_xlabel('Year')
ax.set_ylabel('Number of white moves')

plt.figure(figsize=(14,6))
sns.regplot(data, y='combined ACPL', x='white num moves', scatter=False)
ax = sns.scatterplot(data, x='combined ACPL', y='white num moves', hue='year')
ax.set_title('Number of moves by combined ACPL')
ax.set_xlabel('Combined ACPL')
ax.set_ylabel('Number of white moves')

plt.figure(figsize=(17, 8))
#ax = sns.countplot(data, x='opening trunc', order=data['opening trunc'].value_counts().iloc[:25].index)
ax = sns.countplot(data, x='opening', order=data['opening'].value_counts().iloc[:30].index)
ax.set_xticklabels([label.get_text()[:27] for label in ax.get_xticklabels()], rotation=80, fontsize=8)
ax.set_xlabel('Opening')
ax.set_title('Opening popularity')
ax.figure.tight_layout()


plt.show()