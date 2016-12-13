from sklearn import svm
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.cross_validation import train_test_split
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# Used this to get our images to be the same size
# mogrify -path . -resize 16x16! -format png *.png

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
#root = 'betterquality/'
root = ''
for i in range(1,21):
  triangle = read_image(root + "triangles/%d.png" % i)
  X.append(triangle)
  y.append(2)

  potato = read_image(root + "potatoes/%d.png" % i)
  X.append(potato)
  y.append(0)

  star = read_image(root + "stars/%d.png" % i)
  X.append(star)
  y.append(1)

train_percentage = 0.75
num_classes = 3
yb = label_binarize(y, classes=[i for i in range(num_classes)])
X_train, X_test, y_train, y_test = train_test_split(X, yb, test_size=(1-train_percentage))

clf = OneVsRestClassifier(svm.SVC(kernel='rbf', probability=False))
clf.fit(X_train, y_train)

y_score = clf.fit(X_train, y_train).decision_function(X_test)

precision = {}
recall = {}
avg_precision = {}


# add to precision recall curves for each class
for i in range(num_classes):
    precision[i], recall[i], _ = precision_recall_curve(y_test[:, i], y_score[:, i])
    avg_precision[i] = average_precision_score(y_test[:, i], y_score[:, i])

# Compute micro-average ROC curve and ROC area
precision["micro"], recall["micro"], _ = precision_recall_curve(y_test.ravel(),
    y_score.ravel())
avg_precision["micro"] = average_precision_score(y_test, y_score,
                                                     average="micro")

# Plot Precision-Recall curve
plt.clf()
plt.plot(recall[0], precision[0], label='Precision-Recall curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('Precision-Recall example: AUC={0:0.2f}'.format(avg_precision[0]))
plt.legend(loc="lower left")
#plt.show()

# Plot Precision-Recall curve for each class
plt.clf()
plt.plot(recall["micro"], precision["micro"],
         label='micro-average (area = {0:0.2f})'
               ''.format(avg_precision["micro"]))
for i in range(num_classes):
    plt.plot(recall[i], precision[i],
             label='Class {0} (area = {1:0.2f})'
                   ''.format(i, avg_precision[i]), linewidth=4)


plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Extension of Precision-Recall curve to multi-class')
plt.legend(loc="lower right")
plt.show()


#predicted = clf.predict(X_test)
predicted = clf.fit(X_train, y_train).decision_function(X_test)
classes_total = [0, 0, 0]
classes_correct = [0.0, 0.0, 0.0]
for i in range(len(X_test)):
  types = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
  for j in range(len(types)):
    if all(y_test[i] == types[j]):
      classes_total[j] += 1
      if all(predicted[i] == types[j]):
        classes_correct[j] += 1

print "predicted: ", predicted
print "actual: ", y_test
print "classes correct: ", classes_correct
print "total: ", classes_total
print "accuracy: ", np.array(classes_correct) / np.array(classes_total)
