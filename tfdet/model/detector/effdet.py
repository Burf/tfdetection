import tensorflow as tf
import functools

from .retina import retinanet
from ..backbone.effnet import effnet_b0, effnet_b1, effnet_b2, effnet_b3, effnet_b4, effnet_b5, effnet_b6
from ..backbone.effnet import effnet_lite_b0, effnet_lite_b1, effnet_lite_b2, effnet_lite_b3, effnet_lite_b4
from ..neck import FeatureAlign, bifpn, FeaturePyramidNetwork

def conv(filters, kernel_size, strides = 1, padding = "same", use_bias = True, kernel_initializer = "he_normal", **kwargs):
    return tf.keras.layers.Conv2D(filters, kernel_size, strides = strides, padding = padding, use_bias = use_bias, kernel_initializer = kernel_initializer, **kwargs)

def separable_conv(filters, kernel_size, strides = 1, padding = "same", use_bias = True, depthwise_initializer = tf.keras.initializers.VarianceScaling(), pointwise_initializer = tf.keras.initializers.VarianceScaling(), **kwargs):
    return tf.keras.layers.SeparableConv2D(filters, kernel_size, strides = strides, padding = padding, use_bias = use_bias, depthwise_initializer = depthwise_initializer, pointwise_initializer = pointwise_initializer, **kwargs)

def neck(n_feature = 224, n_sampling = 2, pre_sampling = True, neck = bifpn, neck_n_depth = 7, convolution = conv, normalize = tf.keras.layers.BatchNormalization, **kwargs):
    return FeatureAlign(n_feature = n_feature, n_sampling = n_sampling, pre_sampling = pre_sampling, neck = neck, neck_n_depth = neck_n_depth, convolution = convolution, normalize = normalize, **kwargs)

def effdet(x, n_class = 21, image_shape = [1024, 1024], n_feature = 224, n_depth = 4,
           scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True,
           neck = functools.partial(neck, n_feature = 224, neck_n_depth = 7, neck = functools.partial(bifpn, n_feature = 224)),
           cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.swish, 
           box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.swish):
    out = retinanet(x, n_class = n_class, image_shape = image_shape, n_feature = n_feature, n_depth = n_depth,
                    scale = scale, ratio = ratio, auto_scale = auto_scale,
                    neck = neck,
                    cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                    box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out

def effdet_d0(x, n_class = 21,
              n_feature = 64, n_depth = 3,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              neck = functools.partial(neck, n_feature = 64, neck_n_depth = 3, neck = functools.partial(bifpn, n_feature = 64)),
              cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.swish, 
              box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.swish):
    #image_shape = [512, 512]
    feature = effnet_b0(x, weights = weights, indices = [-3, -2, -1])
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 neck = neck,
                 cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                 box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out
                    
def effdet_d1(x, n_class = 21,
              n_feature = 88, n_depth = 3,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              neck = functools.partial(neck, n_feature = 88, neck_n_depth = 4, neck = functools.partial(bifpn, n_feature = 88)),
              cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.swish, 
              box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.swish):
    #image_shape = [640, 640]
    feature = effnet_b1(x, weights = weights, indices = [-3, -2, -1])
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 neck = neck,
                 cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                 box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out
                    
def effdet_d2(x, n_class = 21,
              n_feature = 112, n_depth = 3,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              neck = functools.partial(neck, n_feature = 112, neck_n_depth = 5, neck = functools.partial(bifpn, n_feature = 112)),
              cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.swish, 
              box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.swish):
    #image_shape = [768, 768]
    feature = effnet_b2(x, weights = weights, indices = [-3, -2, -1])
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 neck = neck,
                 cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                 box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out
                    
def effdet_d3(x, n_class = 21,
              n_feature = 160, n_depth = 4,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              neck = functools.partial(neck, n_feature = 160, neck_n_depth = 6, neck = functools.partial(bifpn, n_feature = 160)),
              cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.swish, 
              box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.swish):
    #image_shape = [896, 896]
    feature = effnet_b3(x, weights = weights, indices = [-3, -2, -1])
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 neck = neck,
                 cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                 box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out
                    
def effdet_d4(x, n_class = 21,
              n_feature = 224, n_depth = 4,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              neck = functools.partial(neck, n_feature = 224, neck_n_depth = 7, neck = functools.partial(bifpn, n_feature = 224)),
              cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.swish, 
              box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.swish):
    #image_shape = [1024, 1024]
    feature = effnet_b4(x, weights = weights, indices = [-3, -2, -1])
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 neck = neck,
                 cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                 box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out
                    
def effdet_d5(x, n_class = 21,
              n_feature = 288, n_depth = 4,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              neck = functools.partial(neck, n_feature = 288, neck_n_depth = 7, neck = functools.partial(bifpn, n_feature = 288)),
              cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.swish, 
              box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.swish):
    #image_shape = [1280, 1280]
    feature = effnet_b5(x, weights = weights, indices = [-3, -2, -1])
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 neck = neck,
                 cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                 box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out
                    
def effdet_d6(x, n_class = 21,
              n_feature = 384, n_depth = 5,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              neck = functools.partial(neck, n_feature = 384, neck_n_depth = 8, neck = functools.partial(bifpn, n_feature = 384, weighted_add = False)),
              cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.swish, 
              box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.swish):
    #image_shape = [1280, 1280] > d6
    #image_shape = [1536, 1536] > d7
    feature = effnet_b6(x, weights = weights, indices = [-3, -2, -1])
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 neck = neck,
                 cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                 box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out

effdet_d7 = effdet_d6

def effdet_d7x(x, n_class = 21,
               n_feature = 384, n_depth = 5,
               scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
               neck = functools.partial(neck, n_feature = 384, neck_n_depth = 8, neck = functools.partial(bifpn, n_feature = 384, weighted_add = False)),
               cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.swish, 
               box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.swish):
    #image_shape = [1536, 1536]
    feature = effnet_b7(x, weights = weights, indices = [-3, -2, -1])
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 neck = neck,
                 cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                 box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out

def effdet_lite(x, n_class = 21, image_shape = [384, 384], n_feature = 88, n_depth = 3,
                scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True,
                neck = functools.partial(neck, n_feature = 88, neck_n_depth = 4, neck = functools.partial(bifpn, n_feature = 88, weighted_add = False, activation = tf.nn.relu6)),
                cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.relu6, 
                box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.relu6):
    out = retinanet(x, n_class = n_class, image_shape = image_shape, n_feature = n_feature, n_depth = n_depth,
                    scale = scale, ratio = ratio, auto_scale = auto_scale,
                    neck = neck,
                    cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                    box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out

def effdet_lite_d0(x, n_class = 21,
                   n_feature = 64, n_depth = 3,
                   scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                   neck = functools.partial(neck, n_feature = 64, neck_n_depth = 3, neck = functools.partial(bifpn, n_feature = 64, weighted_add = False, activation = tf.nn.relu6)),
                   cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.relu6, 
                   box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.relu6):
    #image_shape = [320, 320]
    feature = effnet_lite_b0(x, weights = weights, indices = [-3, -2, -1])
    out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                      scale = scale, ratio = ratio, auto_scale = auto_scale,
                      neck = neck,
                      cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                      box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out

def effdet_lite_d1(x, n_class = 21,
                   n_feature = 88, n_depth = 3,
                   scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                   neck = functools.partial(neck, n_feature = 88, neck_n_depth = 4, neck = functools.partial(bifpn, n_feature = 88, weighted_add = False, activation = tf.nn.relu6)),
                   cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.relu6, 
                   box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.relu6):
    #image_shape = [384, 384]
    feature = effnet_lite_b1(x, weights = weights, indices = [-3, -2, -1])
    out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                      scale = scale, ratio = ratio, auto_scale = auto_scale,
                      neck = neck,
                      cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                      box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out
                    
def effdet_lite_d2(x, n_class = 21,
                   n_feature = 112, n_depth = 3,
                   scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                   neck = functools.partial(neck, n_feature = 112, neck_n_depth = 5, neck = functools.partial(bifpn, n_feature = 112, weighted_add = False, activation = tf.nn.relu6)),
                   cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.relu6, 
                   box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.relu6):
    #image_shape = [448, 448]
    feature = effnet_lite_b2(x, weights = weights, indices = [-3, -2, -1])
    out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                      scale = scale, ratio = ratio, auto_scale = auto_scale,
                      neck = neck,
                      cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                      box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out
                    
def effdet_lite_d3(x, n_class = 21,
                   n_feature = 160, n_depth = 4,
                   scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                   neck = functools.partial(neck, n_feature = 160, neck_n_depth = 6, neck = functools.partial(bifpn, n_feature = 160, weighted_add = False, activation = tf.nn.relu6)),
                   cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.relu6, 
                   box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.relu6):
    #image_shape = [512, 512]
    feature = effnet_lite_b3(x, weights = weights, indices = [-3, -2, -1])
    out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                      scale = scale, ratio = ratio, auto_scale = auto_scale,
                      neck = neck,
                      cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                      box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out
                    
def effdet_lite_d3x(x, n_class = 21,
                    n_feature = 200, n_depth = 4,
                    scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                    neck = functools.partial(neck, n_feature = 200, neck_n_depth = 6, neck = functools.partial(bifpn, n_feature = 200, weighted_add = False, activation = tf.nn.relu6)),
                    cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.relu6, 
                    box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.relu6):
    #image_shape = [640, 640]
    feature = effnet_lite_b3(x, weights = weights, indices = [-3, -2, -1])
    out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                      scale = scale, ratio = ratio, auto_scale = auto_scale,
                      neck = neck,
                      cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                      box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out
                    
def effdet_lite_d4(x, n_class = 21,
                   n_feature = 224, n_depth = 4,
                   scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                   neck = functools.partial(neck, n_feature = 224, neck_n_depth = 7, neck = functools.partial(bifpn, n_feature = 224, weighted_add = False, activation = tf.nn.relu6)),
                   cls_convolution = separable_conv, cls_normalize = tf.keras.layers.BatchNormalization, cls_activation = tf.nn.relu6, 
                   box_convolution = separable_conv, box_normalize = tf.keras.layers.BatchNormalization, box_activation = tf.nn.relu6):
    #image_shape = [640, 640]
    feature = effnet_lite_b4(x, weights = weights, indices = [-3, -2, -1])
    out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth,
                      scale = scale, ratio = ratio, auto_scale = auto_scale,
                      neck = neck,
                      cls_convolution = cls_convolution, cls_normalize = cls_normalize, cls_activation = cls_activation, 
                      box_convolution = box_convolution, box_normalize = box_normalize, box_activation = box_activation)
    return out