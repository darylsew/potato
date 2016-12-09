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
    for y in range(16):
      example.append(pix[x, y])
  return example


print read_image("potatoes/1.png")


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
  

clf = svm.SVC()
clf.fit(X, y)  

maybe_potatoes = [read_image("potatoes/20.png")]
print clf.predict(maybe_potatoes)


"""
X = [[0, 0], [1, 1]]
y = [0, 1]
"""
