from albumentations.augmentations.transforms import PadIfNeeded, ShiftScaleRotate
import numpy as np
import albumentations as albu

def augment_axial(image_dict):
    """ Takes a dict of ['image', 'mask'] and performs an augmentation on it,
    returning it in the same data structure that it came in as. 

    The augmentation is optimized for "axial plane" slices.

    @params:
    image_dict: a dict of ['image', 'mask']
    """
    # define the augmentation
    augmentation = albu.Compose([
        albu.ShiftScaleRotate(scale_limit = [0, 0.1], shift_limit=0.2, rotate_limit=5, p=1),
        albu.CenterCrop(320, 320),
        albu.HorizontalFlip(p=0.5)
        ])
    # (H x W) --> (H x W x 1) for albumentations package
    image = np.expand_dims(image_dict['ct'], axis=2)
    mask =  np.expand_dims(image_dict['spine'], axis=2)
    # do the augmentation
    aug_imgs = augmentation(image = image, mask = mask)
    # (H x W x 1) --> (H x W) for return data
    for item in aug_imgs:
        aug_imgs[item] = np.squeeze(aug_imgs[item])
    # rename keys back to original for return data
    aug_imgs['ct'] = aug_imgs.pop('image')
    aug_imgs['spine'] = aug_imgs.pop('mask')

    return aug_imgs     # dict(H x W)