# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 16:00:13 2021

@author: a0981
"""

import pandas as pd


df = pd.read_csv('cookie_cats.csv')
print(df.head(5))

# Counting the number of players in each AB group.
print(df.groupby('version').count())

# Counting the number of players for each number of gamerounds 
plot_df = df.groupby('sum_gamerounds')['userid'].count()

# Plotting the distribution of players that played 0 to 100 game rounds
ax = plot_df.head(n=100).plot(x="sum_gamerounds", y="userid")
ax.set_xlabel("Game Rounds")
ax.set_ylabel("User Count")


#1-day retention by AB-group
# The % of users that came back the day after they installed
df['retention_1'].sum() / df['retention_1'].count()

# Calculating 1-day retention for each AB-group
df.groupby('version')['retention_1'].sum() / df.groupby('version')['userid'].count()

# Repeatedly re-sample our dataset (with replacement) and calculate 1-day retention for those samples
# Creating an list with bootstrapped means for each AB-group
boot_1d = []
for i in range(500):
    boot_mean = df.sample(frac=1, replace=True).groupby('version')['retention_1'].mean()
    boot_1d.append(boot_mean)
    
# Transforming the list to a DataFrame
boot_1d = pd.DataFrame(boot_1d)
    
# A Kernel Density Estimate plot of the bootstrap distributions
boot_1d.plot(kind='kde')

# Adding a column with the % difference between the two AB-groups
boot_1d['diff'] = (boot_1d['gate_30'] - boot_1d['gate_40']) / boot_1d['gate_40'] * 100
# Ploting the bootstrap % difference
ax = boot_1d['diff'].plot(kind = 'kde')
ax.set_xlabel("% difference in means")

##we can see that the most likely % difference is around 1% - 2%, and that most of the distribution is above 0%
# Calculating the probability that 1-day retention is greater when the gate is at level 30
prob = len(boot_1d[boot_1d['diff'] > 0]) / len(boot_1d)
# Pretty printing the probability
'{:.1%}'.format(prob)

#The bootstrap analysis tells us that there is a high probability that 1-day retention is better when the gate is at level 30.


#7-day retention by AB-group
# Calculating 7-day retention for both AB-groups
df.groupby('version')['retention_7'].sum() / df.groupby('version')['userid'].count()

# Creating a list with bootstrapped means for each AB-group
boot_7d = []
for i in range(500):
    boot_mean = df.sample(frac=1, replace=True).groupby('version')['retention_7'].mean()
    boot_7d.append(boot_mean)
    
# Transforming the list to a DataFrame
boot_7d = pd.DataFrame(boot_7d)

# Adding a column with the % difference between the two AB-groups
boot_7d['diff'] = (boot_7d['gate_30'] - boot_7d['gate_40']) /  boot_7d['gate_30'] * 100

# Ploting the bootstrap % difference
ax = boot_7d['diff'].plot(kind = 'kde')
ax.set_xlabel("% difference in means")

# Calculating the probability that 7-day retention is greater when the gate is at level 30
prob = len(boot_7d[boot_7d['diff'] > 0]) / len(boot_7d)

# Pretty printing the probability
'{:.1%}'.format(prob)

#The bootstrap result tells us that there is strong evidence that 7-day retention is higher when the gate is at level 30 than when it is at level 40.

print('Conclusion: If we want to keep retention high — both 1-day and 7-day retention — we should not move the gate from level 30 to level 40')



