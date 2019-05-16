from PIL import Image
import os
import multiprocessing
import subprocess
import random
import shutil

root = os.path.abspath("/home/retrontology/Downloads/4kPics/4k4xRetroTrain")
corecount = multiprocessing.cpu_count()
scale = 4
fcount = 6
suffix = "_tiles"

def downscaleWorker(oldfile, newfile):
    img = Image.open(oldfile)
    size = tuple([int(x/(scale/2)) for x in img.size])
    img = img.resize(size,Image.BICUBIC)
    img.save(newfile)
    print("Downscaling: " + oldfile + " >>> " + newfile)
    
def downscaleHR(dir):
    print("Downscaling HR to LR starting")
    pool = multiprocessing.Pool(corecount)
    for i in range(1,fcount):
        print("Downscaling: " + os.path.join(dir, str(i)))
        HR = os.path.join(os.path.join(dir, str(i)), "HR" + suffix)
        LR = os.path.join(os.path.join(dir, str(i)), "LR" + suffix)
        if not os.path.isdir(LR):
            os.mkdir(LR)
        for file in os.listdir(HR):
            pool.apply_async(downscaleWorker, (os.path.join(HR, file), os.path.join(LR, file), ))
    pool.close()
    pool.join()
    print("Downscaling HR to LR done")

def sample(dir):
    pool = multiprocessing.Pool(corecount)
    for i in range(1,fcount):
        HR = os.path.join(os.path.join(dir, str(i)), "HR" + suffix)
        LR = os.path.join(os.path.join(dir, str(i)), "LR" + suffix)
        HRsample = os.path.join(os.path.join(dir, str(i)), "HR" + suffix + "sample")
        LRsample = os.path.join(os.path.join(dir, str(i)), "LR" + suffix + "sample")
        if not os.path.isdir(HRsample):
            os.mkdir(HRsample)
        if not os.path.isdir(LRsample):
            os.mkdir(LRsample)
        files = os.listdir(HR)
        random.shuffle(files)
        for j in range(0,int(len(files)/10)):
            pool.apply_async(shutil.copyfile, (os.path.join(HR, files[j]),os.path.join(HRsample,files[j])))
            pool.apply_async(shutil.copyfile, (os.path.join(LR, files[j]),os.path.join(LRsample,files[j])))
    pool.close()
    pool.join()

def folderCount(dir):
    i = 1
    while os.path.isdir(os.path.join(dir, str(i))):
        i = i + 1
    return i

fcount = folderCount(root)
#downscaleHR(root)
sample(root)
