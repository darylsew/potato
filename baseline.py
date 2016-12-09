from sklearn import svm
from PIL import Image
import numpy as np

# Used this to get our images to be the same size
# mogrify -path . -resize 16x16 -format png *.png

def read_image(name):
  """
  Reads image into a training example. Might be good to threshold it.
  """
  im = Image.open(name)
  pix = im.load()
  example = []
  for x in range(16):
    for y in range(16):
      example.append(pix[x, y])
  return example


X = []
y = []
for i in range(1,21):
  potato = read_image("potatoes/%d.png" % i)
  X.append(potato)
  y.append(0)

  star = read_image("stars/%d.png" % i)
  X.append(star)
  y.append(1)

  triangle = read_image("triangles/%d.png" % i)
  X.append(triangle)
  y.append(2)
  

train_percentage = 0.75

train_test_split = int(len(X)*train_percentage)
X_train = X[:train_test_split]
X_test = X[train_test_split:]

train_test_split = int(len(y)*train_percentage)
y_train = y[:train_test_split]
y_test = y[train_test_split:]

clf = svm.SVC()
clf.fit(X, y)  

#print "Predicted: ", clf.predict(X_test)
#print "Actual: ", np.array(y_test)

#print "Accuracy: ", correct / len(X_test)
