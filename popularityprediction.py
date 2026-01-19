import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sklearn
df = pd.read_csv("tracks.csv")

#adjust columns for easy analysis
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['since_release'] = (pd.Timestamp.today() - df['release_date']).dt.days
df['album_type'] = (df['album_type'] != "single").astype(int) #0=single 1=album
df['explicit'] = df['explicit'].astype(int) #0=not 1=explicit
df['log_followers'] = np.log10(df['artist_followers'])
df['log_duration'] = np.log10(df['duration_ms'])

#exploratory data analysis
sns.pairplot(df, kind='scatter', plot_kws={'alpha': 0.4})
plt.show()

#split data
from sklearn.model_selection import train_test_split
x = df[['log_followers', 'explicit', 'album_type', 'duration_ms', 'since_release']]
y = df['popularity']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42) 

#train model
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(
    n_estimators=300,
    max_depth=None,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
rf.fit(x_train, y_train)
predictions = rf.predict(x_test)

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import math
print("MAE:", mean_absolute_error(y_test, predictions)) 
print("RMSE:", math.sqrt(mean_squared_error(y_test, predictions))) 
print("R2:", r2_score(y_test, predictions))
