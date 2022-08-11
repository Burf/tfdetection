import functools

import numpy as np
import tensorflow as tf

from tfdet.core.util import pipeline, py_func, dict_function

@dict_function(extra_keys = ["y_true", "bbox_true", "mask_true"])
def dict_py_func(function, *args, Tout = tf.float32, **kwargs):
    return py_func(function, *args, Tout = Tout, **kwargs)

def pipe(function, x_true, y_true = None, bbox_true = None, mask_true = None, dtype = None, tf_func = False,
         pre_batch_size = 0, pre_shuffle = False, pre_shuffle_size = None, pre_prefetch = False, pre_prefetch_size = None,
         batch_size = 0, epoch = 1, shuffle = False, prefetch = False, num_parallel_calls = None, cache = None, shuffle_size = None, prefetch_size = None,
         py_func = dict_py_func,
         **kwargs):
    args = [arg for arg in [x_true, y_true, bbox_true, mask_true] if arg is not None]
    args = args[0] if len(args) == 1 else tuple(args)
    pre_pipe = pipeline(args, batch_size = pre_batch_size, shuffle = pre_shuffle, prefetch = pre_prefetch, num_parallel_calls = num_parallel_calls, shuffle_size = pre_shuffle_size, prefetch_size = pre_prefetch_size)
    func = None
    if tf_func:
        func = functools.partial(function, **kwargs)
    elif callable(function):
        if dtype is None:
            if isinstance(x_true, tf.data.Dataset):
                dtype = tuple(pre_pipe.element_spec.values()) if isinstance(pre_pipe.element_spec, dict) else pre_pipe.element_spec
            else:
                if isinstance(x_true, dict):
                    sample_result = function(**{k:v[0] for k, v in x_true.items()}, **kwargs)
                else:
                    sample_args = [v[0] for v in [x_true, y_true, bbox_true, mask_true] if v is not None]
                    sample_result = function(*sample_args, **kwargs)
                dtype = [tf.convert_to_tensor(r).dtype for r in (sample_result if isinstance(sample_result, tuple) else (sample_result,))]
                dtype = dtype[0] if len(dtype) == 1 else tuple(dtype)
        elif np.ndim(dtype) == 0:
            if isinstance(x_true, tf.data.Dataset):
                if isinstance(x_true.element_spec, tuple) or isinstance(x_true.element_spec, dict):
                    dtype = [dtype] * len(x_true.element_spec)
            else:
                dtype = [dtype] * len(x_true if isinstance(x_true, dict) else [arg for arg in [x_true, y_true, bbox_true, mask_true] if arg is not None])
                dtype = dtype[0] if len(dtype) == 1 else tuple(dtype)
        func = functools.partial(py_func, function, Tout = dtype, **kwargs) if callable(function) else None
    return pipeline(pre_pipe, map = func, batch_size = batch_size, epoch = epoch, shuffle = shuffle, prefetch = prefetch, num_parallel_calls = num_parallel_calls, cache = cache, shuffle_size = shuffle_size, prefetch_size = prefetch_size)