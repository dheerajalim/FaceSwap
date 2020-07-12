# FaceSwap #

The FaceSwap app is inspired from the work of @MarekKowalski. This is built using eel to provide a fully functional User Interface
.The app is written in Python and uses face alignment, Gauss Newton optimization and image blending to swap the face of a person seen by the camera with a face of a person in a provided image.

## Running FaceSwap executable ##
Download the faceswap-setup.exe [[click to download]](https://bit.ly/38MSLVf).
(Currently supports Windows)

Once downloaded setup the application and play around.

## Demo ##
[![click to download](http://img.youtube.com/vi/grkg8GMlBGU/0.jpg)](https://youtu.be/grkg8GMlBGU)


## Running FaceSwap ##
$ pip install -r requirements.txt

$ python start_app.py

## How to use it ##
To start the program you will have to run a file named start_app.py , which will require:
  * Python 3 (worked on 3.6)
  * OpenCV 
  * Numpy
  * dlib (You might need to install cmake < pip install cmake >)
  * pygame 
  * PyOpenGL
  * eel
  * pymsgbox

You can download all of the libraries above either from PIP or from Christoph Gohlke's excellent website: http://www.lfd.uci.edu/~gohlke/pythonlibs/

You will also have to download the face alignment model from here: http://sourceforge.net/projects/dclib/files/dlib/v18.10/shape_predictor_68_face_landmarks.dat.bz2 and unpack it to the FaceSwap > models project directory.

**It is already present in the models directory**
## Process Flow ##

## How it works ##
The general outline of the method is as follows:

First we take the input image (the image of a person we want to see on our own face) and find the face region and its landmarks. Once we have that we fit the 3D model to those landmarks (more on that later) the vertices of that model projected to the image space will be our texture coordinates. 

Once that is finished and everything is initialized the camera starts capturing images. For each captured images the following steps are taken:

1. The face region is detected and the facial landmarks are located.
2. The 3D models is fitted to the located landmarks.
3. The 3D models is rendered using pygame with the texture obtained during initialization.
4. The image of the rendered model is blended with the image obtained from the camera using feathering (alpha blending) and very simple color correction.
5. The final image is shown to the user.

The most crucial element of the entire process is the fitting of the 3D model. The model itself consists of:
  * the 3D shape (set of vertices) of a neutral face,
  * a number of blendshapes that can be added to the neutral face to produce mouth opening, eyebrow raising, etc.,
  * a set of triplets of indices into the face shape that form the triangular mesh of the face,
  * two sets of indices which establish correspondence between the landmarks found by the landmark localizer and the vertices of the 3D face shape.

The model is projected into the image space using the following equation:

![equation](http://home.elka.pw.edu.pl/~mkowals6/lib/exe/fetch.php?media=faceswap_equation.png)

where *s* is the projected shape, *a* is the scaling parameter, *P* are the first two rows of a rotation matrix that rotates the 3D face shape, *S_0* is the neutral face shape, *w_1-n* are the blendshape weights, *S_1-n* are the blendshapes, *t* is a 2D translation vector and *n* is the number of blendshapes.

The model fitting is accomplished by minimizing the difference between the projected shape and the localized landmarks. The minimization is accomplished with respect to the blendshape weights, scaling, rotation and translation, using the [Gauss Newton method](https://en.wikipedia.org/wiki/Gauss%E2%80%93Newton_algorithm).


## Contact ##
Please feel free to contribute in enhancing the application.

[Dheeraj Alimchandani](mailto:dheeraj.alim@gmail.com?subject=[GitHub]%20FaceSwap%20Repo)