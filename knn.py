from PIL import Image
import heapq as hp
import numpy as np

# CONSTANTS TO PLAY WITH :)
threshold = 255
train_percentage = 0.75
K = 6

# Used this to get our images to be the same size
# mogrify -path . -resize 16x16 -format png *.png
# Returns: 1x175 vector
def read_image(name):
  """
  Reads image into a training example. Might be good to threshold it.
  """
  im = Image.open(name)
  pix = im.load()
  example = []
  for x in range(16):
    for y in range(11):
      if pix[x, y] >= threshold:
        example.append(1)
      else:
        example.append(0)
      #example.append(pix[x,y])
  print example
  return example


def knnPred(train, test, K):
	preds = []
	# dimension of points
	(x, y) = train[0]
	D = len(x)

	for (X_te, ignore) in test:
		dist_heap =[]
		k_top_labels = []
		for (X_tr, label) in train:
			dist_calc = 0
			for i in range(D):
				dist_calc += pow(abs(X_tr[i] - X_te[i]), D)
			dist_calc = pow(dist_calc, (1./D))
			hp.heappush(dist_heap, (dist_calc, label))
		print dist_heap
		for i in range(K):
			(dist, label) = hp.heappop(dist_heap)
			k_top_labels.append(label)

		print "k_top_labels is"
		print k_top_labels
		# find the most popular label among top k closest labels
		label_counter = {}
		for label in k_top_labels:
			if label in label_counter:
				label_counter[label] += 1
			else:
				label_counter[label] = 1
		popular_labels = sorted(label_counter, key = label_counter.get, reverse=True)

		if label_counter[popular_labels[0]] == 6:
			preds.append(popular_labels[0])
		else:
			preds.append('tri')

		#preds.append(popular_labels[0])
	return preds

pics = []
train = []
test = []

for i in range(1,21):
  triangle = read_image("triangles/%d.png" % i)
  pics.append((triangle, "tri"))

  potato = read_image("potatoes/%d.png" % i)
  pics.append((potato, "pot"))

  star = read_image("stars/%d.png" % i)
  pics.append((star, "str"))


train_test_split = int(len(pics)*train_percentage)

train = pics[:train_test_split]
test  = pics[train_test_split:]

test_labels = []

for (te_x, te_label) in test:
	test_labels.append(te_label)

predicted = knnPred(train, test, K)

print "Predicted: ", predicted
print "Actual:    ", test_labels
