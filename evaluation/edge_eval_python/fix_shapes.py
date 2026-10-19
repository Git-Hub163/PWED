import os
import glob
import numpy as np
import scipy.io as sio
from PIL import Image

def find_2d_shape(obj):
    """递归遍历并安全提取 MATLAB 复杂嵌套结构体中的真实图片尺寸"""
    if isinstance(obj, np.ndarray):
        if obj.ndim == 2 and obj.shape[0] > 10 and obj.shape[1] > 10:
            return obj.shape
        for item in obj.flatten():
            res = find_2d_shape(item)
            if res: return res
    elif isinstance(obj, np.void):
        for name in obj.dtype.names:
            res = find_2d_shape(obj[name])
            if res: return res
    return None

rcf_dir = "../RCF_mat"
gt_dir = "../GroundTruths_mat"
fixed = 0

# 兼容不同版本的 PIL
try:
    resample_method = Image.Resampling.BILINEAR
except AttributeError:
    resample_method = Image.BILINEAR

for pred_path in glob.glob(os.path.join(rcf_dir, "*.mat")):
    name = os.path.basename(pred_path)
    gt_path = os.path.join(gt_dir, name)
    
    if not os.path.exists(gt_path):
        continue
        
    pred_data = sio.loadmat(pred_path)
    pred = pred_data['result']
    
    gt_data = sio.loadmat(gt_path)
    true_shape = find_2d_shape(gt_data['groundTruth'])
    
    if true_shape and pred.shape != true_shape:
        # 1. 检查是否仅仅是长宽反了
        if pred.shape[::-1] == true_shape:
            pred_fixed = pred.T
        else:
            # 2. 如果尺寸对不上，强制 Resize 回 Ground Truth 的尺寸
            im = Image.fromarray(pred)
            # PIL 的 resize 接收的参数顺序是 (Width, Height)
            im = im.resize((true_shape[1], true_shape[0]), resample_method)
            pred_fixed = np.array(im)
        
        pred_data['result'] = pred_fixed
        sio.savemat(pred_path, pred_data, do_compression=True)
        print(f"Fixed {name}: {pred.shape} -> {true_shape}")
        fixed += 1

print(f"=== Shape Alignment Complete. Fixed {fixed} mismatched files. ===")
