# set up Python environment: numpy for numerical routines, and matplotlib for plotting
import numpy as np
import matplotlib.pyplot as plt
import caffe
import os

caffe_root = '/Users/daryl/potato/caffe/'
#caffe_root = '/home/dns55/potato/caffe/'
# display plots in this notebook

# set display defaults
plt.rcParams['figure.figsize'] = (10, 10)        # large images
plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap

caffe.set_mode_cpu()

model_def = caffe_root + 'examples/mnist/lenet.prototxt'
#model_weights = '/Users/daryl/potato/models/lenet_iter_10000.caffemodel'
model_weights = '/Users/daryl/potato/models/realfood10000.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# load the mean ImageNet image (as distributed with Caffe) for subtraction
#mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
#mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
#print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
#transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
#transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
#transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(1,        # batch size
                          1,         # 3-channel (BGR) images
                         28, 28)  # image size is 28x28


def classify(name, expected):
  image = caffe.io.load_image(name)
  image = transformer.preprocess('data', image)
  #import pdb; pdb.set_trace()
  #import pdb; pdb.set_trace()
  #transformed_image = transformer.preprocess('data', image)
  #plt.imshow(image[:1,:,:])
  # copy the image data into the memory allocated for the net
  #net.blobs['data'].data[...] = transformed_image
  ### perform classification
  #import pdb; pdb.set_trace()

  img = np.empty((28,28))
  for i in range(3):
    for j in range(28):
      for k in range(28):
        img[j,k] += image[j,k,i]
  for i in range(28):
    for j in range(28):
      img[i,j] /= float(3)

  #import pdb;pdb.set_trace()

  output = net.forward_all(data=np.asarray([img]))
  # the output probability vector for the first image in the batch
  output_prob = output['prob'][0]
  label = output_prob.argmax()
  #import pdb; pdb.set_trace()
  #d = {0: 'potato', 1: 'star', 2: 'triangle'}
  print "got %s, expected %s" % (label, expected)

  #if label == 0:
  #  return "potato"
  #else:
  #  return "not potato"

test_images = '/Users/daryl/potato/JPG-PNG-to-MNIST-NN-Format/test-images/%d'
# filter out ds store
num_classes = len([i for i in os.listdir(test_images[:-2]) if '.' not in i])
for i in range(num_classes):
  test_image_class = test_images % i
  count = 0
  for f in os.listdir(test_image_class):
    count += 1
    if f.lower().endswith('.jpg') or f.lower().endswith('.png'):
      classify('%s/%s' % (test_image_class, f), i)
    if count > 5:
      break

  #print "Should be not potato: ", classify('%d.jpg' % i)
