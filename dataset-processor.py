import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import random as rnd
sns.set(style="ticks", color_codes=True)

# Create directories
os.makedirs('plots/matplotlib', exist_ok=True)
os.makedirs('plots/seaborn', exist_ok=True)

# Treatment for the arguments
parser = argparse.ArgumentParser(description='Script to analyze and visualize data')
parser.add_argument('file_path', type=str, help='File path of the dataset')
parser.add_argument('header_names', type=str, help='File path of header column names')
args = parser.parse_args()

file_path = args.file_path
header_path = args.header_names

if not os.path.isfile(file_path):
    print('Invalid file, I\'ll crash')

if not os.path.isfile(header_path):
    print('Invalid header file, I\'ll crash')

# Header: create the 30 column names adding the suffix: -mean, -se, -worst
list_header = ['id', 'diagnosis']
column_names = []
with open(header_path) as file_handler:
    for line in file_handler:
        line_values = line.split(',')
        for value in line_values:
            column_names.append(value.strip())
        for l in ('-mean', '-se', '-worst'):
            for item in line_values:
                list_header.append(item.strip() + l)

list_header_mean = [x for x in list_header if '-mean' in x]
list_header_se = [x for x in list_header if '-se' in x]
list_header_worst = [x for x in list_header if '-worst' in x]

# Load the dataframe
df = pd.read_csv(file_path, names=list_header)
df.pop('id')

df['encoded_diagnosis'] = df['diagnosis'].map({'B': 0, 'M': 1})
list_header_mean.append('encoded_diagnosis')
list_header_se.append('encoded_diagnosis')
list_header_worst.append('encoded_diagnosis')

df_mean = df[list_header_mean]
df_se = df[list_header_se]
df_worst = df[list_header_worst]

# **********************************************************************
# ************* Correlation Heatmap ************************************
# **********************************************************************

# with Matplotlib
correlation = df_mean.corr().round(2)
fig, axes = plt.subplots(1, 1, figsize=(20, 20))
im = axes.imshow(correlation)
cbar = axes.figure.colorbar(im, ax=axes)
cbar.ax.set_ylabel('Correlation', rotation=-90, va="bottom")
numrows = len(correlation.iloc[0])
numcolumns = len(correlation.columns)
axes.set_xticks(np.arange(numrows))
axes.set_yticks(np.arange(numcolumns))
axes.set_xticklabels(correlation.columns)
axes.set_yticklabels(correlation.columns)
plt.setp(axes.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
for i in range(numrows):
    for j in range(numcolumns):
        text = axes.text(j, i, correlation.iloc[i, j], ha='center', va='center', color='w')
axes.set_title('Heatmap of Correlation of Dimensions - Mean')
fig.tight_layout()
plt.savefig(f'plots/matplotlib/1-heatmap-mean.png')
plt.close()


correlation = df.corr().round(2)
fig, axes = plt.subplots(1, 1, figsize=(20, 20))
im = axes.imshow(correlation)
cbar = axes.figure.colorbar(im, ax=axes)
cbar.ax.set_ylabel('Correlation', rotation=-90, va="bottom")
numrows = len(correlation.iloc[0])
numcolumns = len(correlation.columns)
axes.set_xticks(np.arange(numrows))
axes.set_yticks(np.arange(numcolumns))
axes.set_xticklabels(correlation.columns)
axes.set_yticklabels(correlation.columns)
plt.setp(axes.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
for i in range(numrows):
    for j in range(numcolumns):
        text = axes.text(j, i, correlation.iloc[i, j], ha='center', va='center', color='w')
axes.set_title('Heatmap of Correlation of Dimensions - All')
fig.tight_layout()
plt.savefig(f'plots/matplotlib/1-heatmap-all.png')
plt.close()

#with Seaborn
sns.set()
fig, ax = plt.subplots(figsize=(14, 14))
sns.heatmap(df_mean.corr(), annot=True, cmap='Blues', linewidths=0.5)
ax.set_xticklabels(df.columns, rotation=45)
ax.set_yticklabels(df.columns, rotation=45)
plt.savefig('plots/seaborn/1-heatmap-mean.png')
plt.close()


# **********************************************************************
# ************* Pairplot Hist  *****************************************
# **********************************************************************

sns.pairplot(df_mean, hue='encoded_diagnosis', diag_kind='hist', palette='pastel', markers=["s", "D"])
plt.suptitle('Pair Plot of Breast cancer - mean', size=12)
plt.savefig(f'plots/seaborn/1-pairplot-hist-mean.png')
plt.close()

sns.pairplot(df_se, hue='encoded_diagnosis', diag_kind='hist', palette='muted', markers=["o", "D"])
plt.suptitle('Pair Plot of Breast cancer - se', size=12)
plt.savefig(f'plots/seaborn/1-pairplot-hist-se.png')
plt.close()

sns.pairplot(df_worst, hue='encoded_diagnosis', diag_kind='hist', palette='husl', markers=["o", "s"])
plt.suptitle('Pair Plot of Breast cancer - worst', size=12)
plt.savefig(f'plots/seaborn/1-pairplot-hist-worst.png')
plt.close()

sns.pairplot(df, hue='encoded_diagnosis', diag_kind='hist')
plt.suptitle('Pair Plot of Breast cancer - All', size=12)
plt.savefig(f'plots/seaborn/1-pairplot-hist-all.png')
plt.close()

# **********************************************************************
# ************* Pairplot KDE  ******************************************
# **********************************************************************

sns.pairplot(df_mean, diag_kind='kde')
plt.suptitle('Pair Plot of Breast cancer - mean', size=12)
plt.savefig(f'plots/seaborn/2-pairplot-kde-mean.png')
plt.close()

sns.pairplot(df_se, diag_kind='kde')
plt.suptitle('Pair Plot of Breast cancer - se', size=12)
plt.savefig(f'plots/seaborn/2-pairplot-kde-se.png')
plt.close()

sns.pairplot(df_worst, diag_kind='kde')
plt.suptitle('Pair Plot of Breast cancer - worst', size=12)
plt.savefig(f'plots/seaborn/2-pairplot-kde-worst.png')
plt.close()

# **********************************************************************
# ************* Pairplot REG  ******************************************
# **********************************************************************

sns.pairplot(df_mean, kind='reg')
plt.suptitle('Pair Plot of Breast cancer - mean', size=12)
plt.savefig(f'plots/seaborn/3-pairplot-reg-mean.png')
plt.close()

sns.pairplot(df_se, kind='reg')
plt.suptitle('Pair Plot of Breast cancer - se', size=12)
plt.savefig(f'plots/seaborn/3-pairplot-reg-se.png')
plt.close()

sns.pairplot(df_worst, kind='reg')
plt.suptitle('Pair Plot of Breast cancer - worst', size=12)
plt.savefig(f'plots/seaborn/3-pairplot-reg-worst.png')
plt.close()


# **********************************************************************
# ************* Pairgrid  **********************************************
# **********************************************************************
g = sns.PairGrid(df_mean, diag_sharey=False)
g.map_lower(sns.kdeplot)
g.map_upper(sns.scatterplot)
g.map_diag(sns.kdeplot, lw=3)
plt.savefig(f'plots/seaborn/4-pairgrig-mean.png')
plt.close()

g = sns.PairGrid(df_se, diag_sharey=False)
g.map_lower(sns.kdeplot)
g.map_upper(sns.scatterplot)
g.map_diag(sns.kdeplot, lw=3)
plt.savefig(f'plots/seaborn/4-pairgrig-se.png')
plt.close()

g = sns.PairGrid(df_worst, diag_sharey=False)
g.map_lower(sns.kdeplot)
g.map_upper(sns.scatterplot)
g.map_diag(sns.kdeplot, lw=3)
plt.savefig(f'plots/seaborn/4-pairgrig-worst.png')
plt.close()

# # **********************************************************************
# # ************* Plot 3 columns : mean, se, worst - 1D ******************
# # **********************************************************************
for name_base in column_names:
    fig, axes = plt.subplots(4, 1, figsize=(14, 8))
    fig.suptitle(f'Differents plots for {name_base} : mean, se, worst', fontsize=16)
    #
    names = [x for x in list_header if name_base in x]
    colors = ['royalblue', 'orange', 'limegreen', 'violet', 'r', 'yellow']
    #
    for col_id in df[names].columns:
        sns.distplot(df[col_id], bins=10, kde=False, ax=axes[0])
        axes[0].set_xlabel(name_base)
        axes[0].set_ylabel("Frequency")
        #
        sns.distplot(df[col_id], ax=axes[1], label=col_id)
        axes[1].set_xlabel(name_base)
        axes[1].set_ylabel("Frequency")
        #
        sns.boxplot(data=df[col_id], orient="h", ax=axes[2], color=rnd.choice(colors))
        axes[2].set_xlabel(name_base)
        axes[2].set_ylabel("")
        #
        sns.violinplot(data=df[col_id], orient="h", ax=axes[3], color=rnd.choice(colors))
        axes[3].set_xlabel(name_base)
        axes[3].set_ylabel('')
    plt.tight_layout()
    plt.savefig(f'plots/seaborn/5-ManyPlots-{name_base}-mean-se-worst.png')
    plt.close()


# # **********************************************************************
# # ************* Plot Statistical relationships   ***********************
# # **********************************************************************

for index1, column1 in enumerate(df[list_header_mean].columns):
    for index2, column2 in enumerate(df[list_header_mean].columns):
        if index1 < index2:
            fig, axes = plt.subplots(1, 2, figsize=(10, 5))
            sns.boxplot(x='encoded_diagnosis', y=column2, data=df_mean, ax=axes[0])
            axes[0].set_title(f'Boxplot between diagnosis and {column2}')
            axes[0].set_xlabel(column1)
            axes[0].set_ylabel(column2)
            sns.scatterplot(x=column1, y=column2, hue='encoded_diagnosis', data=df_mean, ax=axes[1])
            axes[1].set_title(f'Scatter between {column1} and {column2}')
            axes[1].set_xlabel(column1)
            axes[1].set_ylabel(column2)
            plt.tight_layout()
            plt.savefig(f'plots/seaborn/6-scatterplot-{column1}-{column2}.png', format='png')
            plt.clf()
            plt.close()

for index1, column1 in enumerate(df[list_header_mean].columns):
    for index2, column2 in enumerate(df[list_header_mean].columns):
        if index1 < index2:
            for jointplot_kind in ['reg', 'hex', 'kde']:
                fig, axes = plt.subplots(figsize=(5, 5))
                sns.jointplot(x=column1, y=column2, data=df_mean, kind=jointplot_kind)
                axes.set_xlabel(column1)
                axes.set_ylabel(column2)
                plt.tight_layout()
                plt.savefig(
                    f'plots/seaborn/7-jointplot-{jointplot_kind}-between-{column1}-{column2}.png')
                plt.clf()
                plt.close()

# Columns : texture-mean, perimeter-mean,smoothness-mean, compactness-mean, concavity-mean, fractal_dimension-mean
