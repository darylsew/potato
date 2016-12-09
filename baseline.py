from sklearn import svm
from PIL import Image

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
    for y in range(11):
      example.append(pix[x, y])
  return example


print read_image("potatoes/1.png")

"""
X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
clf.fit(X, y)  

potato = [1, 1]
print clf.predict([potato])
"""
