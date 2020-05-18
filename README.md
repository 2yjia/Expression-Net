# Expression-Net
(https://github.com/fengju514/Expression-Net)

This page contains a deep convolutional neural network (DCNN) model and python code for robust estimation of the 29 degrees-of-freedom, 3DMM face expression coefficients, directly from an unconstrained face image and without the use of face landmark detectors. The method is described in the paper: 

_F.-J. Chang, A. Tran, T. Hassner, I. Masi, R. Nevatia, G. Medioni, "[ExpNet: Landmark-Free, Deep, 3D Facial Expressions](https://arxiv.org/abs/1802.00542)", in the 13th IEEE Conference on Automatic Face and Gesture Recognition, 2018_ [1].

This release bundles up our **ExpressionNet** (ExpNet) with **FacePoseNet** (FPN) from Chang _et al._ [2], and **3DMM face identity shape network** from Tran _et al._ [3], which are available separately from the [FacePoseNet project page](https://github.com/fengju514/Face-Pose-Net) and the [Face Identity Shape Net project page](https://github.com/anhttran/3dmm_cnn), respectively. 

The code provided here bundles all three components for holistic 3D face modeling and produces a 3D model (.ply mesh file).

**Important** This is an ongoing project. Please check here for updates, corrections and extensions. In particular, mid level facial details can be added to this shape using our [extreme 3D reconstruction project](https://github.com/anhttran/extreme_3d_faces). At the moment facial details estimation is not supported by the code offered here, but we plan to add this in the future. 

## Features
* Estimating **29D 3DMM face expression coefficients**
* **3DMM face identity shape** [3] + **6DoF 3D head pose** [2] are also included ([facial details estimation](https://github.com/anhttran/extreme_3d_faces) is a planned extension)
* Does not depend on fragile landmark detectors, therefore...
* ...robust under image conditions where landmark detectors struggle such as low resolutions and occlusions
* Extremely fast expression estimation
* Provides better expression estimation than the ones using state-of-the-art landmark detectors [1]

## Dependencies

* conda create -n Expression-Net python=2.7
* conda activate Expression-Net
* conda install tensorflow-gpu==1.14.0
* conda install opencv
* conda install matplotlib
* conda install pyqt5-tools
* conda install pillow
* pip install rustface

The code has been tested on Linux with Python 2.7.12. On Linux you can rely on the default version of python, installing all the packages needed from the package manager or on Anaconda Python and install required packages through `conda`. 


## Usage

**Important:** Please download the following learned deep models:

* ExpressionNet from https://www.dropbox.com/s/frq7u7z5kgxnz9e/Expression_Model.tar.gz?dl=0
* Identity shape model from https://www.dropbox.com/s/ej80o9lnj0k49qu/Shape_Model.tar.gz?dl=0, and
* FacePoseNet from https://www.dropbox.com/s/r38psbq55y2yj4f/fpn_new_model.tar.gz?dl=0. 
Make sure that the ExpNet, shape, and FacePoseNet models are stored in the folder `Expression_Model`, `Shape_Model`, and `fpn_new_model` respectively.

### Run it

Our code use a list of images as an input. The software will run ExpNet, ShapeNet, and PoseNet to estimate the expression, shape, and pose to get the .ply 3D mesh files for the images in this list.

```bash
$ python gui.py
```

## Sample Results
Please see the input images ([images](images)), cropped images ([tmp](tmp)), and the output 3D shapes ([output_ply](output_ply)). 
Note: Rendered 3D results appearing here were not rendered to the same scale as the face in the input views, though the pose estimation does provide this information.

## Citation

This project is described in our paper [1]. If you use our expression model, please cite this paper using the bibtex below. If you also use the 3DMM face identity shape network [3] and FacePoseNet [2], please add references to those papers as well.

``` latex
@inproceedings{chang17expnet,
      title={ExpNet: Landmark-Free, Deep, 3D Facial Expressions},
      booktitle = {13th IEEE Conference on Automatic Face and Gesture Recognition},
      author={
      Feng-Ju Chang
      and Anh Tran 
      and Tal Hassner 
      and Iacopo Masi 
      and Ram Nevatia
      and G\'{e}rard Medioni},
      year={2018},
    }
```

## References
[1] F.-J. Chang, A. Tran, T. Hassner, I. Masi, R. Nevatia, G. Medioni, "[ExpNet: Landmark-Free, Deep, 3D Facial Expressions](https://arxiv.org/abs/1802.00542)", in the 13th IEEE Conference on Automatic Face and Gesture Recognition, 2018

[2] F.-J. Chang, A. Tran, T. Hassner, I. Masi, R. Nevatia, G. Medioni, "[FacePoseNet: Making a Case for Landmark-Free Face Alignment](https://arxiv.org/abs/1708.07517)", in the 7th IEEE International Workshop on Analysis and Modeling of Faces and Gestures, ICCV Workshops, 2017

[3] A. Tran, T. Hassner, I. Masi, G. Medioni, "[Regressing Robust and Discriminative 3D Morphable Models with a very Deep Neural Network](https://arxiv.org/abs/1612.04904)", in CVPR, 2017