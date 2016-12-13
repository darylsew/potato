import os
import subprocess


# Run this from root repo directory

root = 'Dataset'
#destination top level directory
dst_tld = 'JPG-PNG-to-MNIST-NN-Format'

os.system("mkdir %s/training-images/" % dst_tld)
os.system("mkdir %s/test-images/" % dst_tld)

split = 0.75
classes = len(os.listdir(root))

for i in range(classes):
  os.system("mkdir %s/training-images/%d" % (dst_tld, i))
  os.system("rm %s/training-images/%d/*" % (dst_tld, i))
  os.system("mkdir %s/test-images/%d" % (dst_tld, i))
  os.system("rm %s/test-images/%d/*" % (dst_tld, i))

for label_ind, label_type in enumerate(os.listdir(root)):
  if "." in label_type:
    continue
  label_path = "%s/%s" % (root, label_type)
  train_index = int(split * len(os.listdir(label_path)))
  for img_ind, img_name in enumerate(os.listdir(label_path)):
    if "JPG" not in img_name.upper():
      continue
    src = "%s/%s" % (label_path, img_name)
    if img_ind < train_index:
      train_or_test = "training-images"
    else:
      train_or_test = "test-images"
    dst = "%s/%s/%d/%d.jpg" % (dst_tld, train_or_test, label_ind, img_ind)
    os.system("cp '%s' '%s'" % (src, dst))

os.system("./%s/resize-script.sh" % dst_tld)
os.system("cp %s/train-images-idx3-ubyte.gz caffe/data/mnist" % dst_tld)
os.system("cp %s/test-images-idx3-ubyte.gz caffe/data/mnist" % dst_tld)
os.system("cp %s/test-labels-idx1-ubyte.gz caffe/data/mnist" % dst_tld)
os.system("cp %s/train-labels-idx1-ubyte.gz caffe/data/mnist" % dst_tld)
