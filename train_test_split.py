import os

root = 'bestquality'
dst = 'JPG-PNG-to-MNIST-NN-Format'


num_images = 40

split = 0.75
train_index = int(split * num_images)

classes = 3

for i in range(classes):
  os.system("mkdir %s/training-images/%d" % (dst, i))
  os.system("rm %s/training-images/%d/*" % (dst, i))
  os.system("mkdir %s/test-images/%d" % (dst, i))
  os.system("rm %s/test-images/%d/*" % (dst, i))

os.system("mkdir ")

for i in range(1, train_index+1):
  os.system("cp %s/potatoes/%s.png %s/training-images/0/%s.png" % (root, i, dst, i))
  os.system("cp %s/stars/%s.png %s/training-images/1/%s.png" % (root, i, dst, i))
  os.system("cp %s/triangles/%s.png %s/training-images/2/%s.png" % (root, i, dst, i))

for i in range(train_index+1, num_images+1):
  os.system("cp %s/potatoes/%s.png %s/test-images/0/%s.png" % (root, i, dst, i))
  os.system("cp %s/stars/%s.png %s/test-images/1/%s.png" % (root, i, dst, i))
  os.system("cp %s/triangles/%s.png %s/test-images/2/%s.png" % (root, i, dst, i))
