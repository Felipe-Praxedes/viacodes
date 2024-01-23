import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import load_iris

from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

data = load_iris()
iris = pd.DataFrame(data['data'], columns=data.feature_names)
target = data.target
svc = SVC(gamma="auto")
cv_result = cross_val_score(svc, iris, target, cv=10, scoring="accuracy")
print("Acurácia com cross validation:", cv_result.mean()*100)

svc.fit(iris, target)
svc.predict([[6.9,2.8,6.1,2.3]])

plt.scatter(iris['sepal length (cm)'], iris['petal width (cm)'], c=target)
plt.title('Iris')
plt.show()