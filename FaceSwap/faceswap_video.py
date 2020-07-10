import dlib
import cv2
import numpy as np

import models
import NonLinearLeastSquares
import ImageProcessing

from drawing import *

import FaceRendering
import utils

import settings_storage
import wx
import tkinter
import tkinter.filedialog as fd
import os
import time

# print ("Press T to draw the keypoints and the 3D model"
# print "Press R to start recording to a video file"

def faceswap():

    source_image_path, destination_image_path, dlib_model, output_video_path, save_image, save_video = \
        settings_storage.fetch_settings()
    #loading the keypoint detection model, the image and the 3D model
    predictor_path = os.getcwd()+"\\models\\"+dlib_model
    image_name = source_image_path
    #the smaller this value gets the faster the detection will work
    #if it is too small, the user's face might not be detected
    maxImageSizeForDetection = 320

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    mean3DShape, blendshapes, mesh, idxs3D, idxs2D = utils.load3DFaceModel("../candide.npz")

    projectionModel = models.OrthographicProjectionBlendshapes(blendshapes.shape[0])

    modelParams = None
    lockedTranslation = False
    drawOverlay = False
    # cap = cv2.VideoCapture('http://192.168.29.156:4747/video')
    cap = cv2.VideoCapture(0)
    writer = None
    cameraImg = cap.read()[1]

    textureImg = cv2.imread(image_name)
    textureCoords = utils.getFaceTextureCoords(textureImg, mean3DShape, blendshapes, idxs2D, idxs3D, detector, predictor)
    renderer = FaceRendering.FaceRenderer(cameraImg, textureImg, textureCoords, mesh)

    while True:
        cameraImg = cap.read()[1]
        shapes2D = utils.getFaceKeypoints(cameraImg, detector, predictor, maxImageSizeForDetection)

        if shapes2D is not None:
            for shape2D in shapes2D:
                #3D model parameter initialization
                modelParams = projectionModel.getInitialParameters(mean3DShape[:, idxs3D], shape2D[:, idxs2D])

                #3D model parameter optimization
                modelParams = NonLinearLeastSquares.GaussNewton(modelParams, projectionModel.residual, projectionModel.jacobian, ([mean3DShape[:, idxs3D], blendshapes[:, :, idxs3D]], shape2D[:, idxs2D]), verbose=0)

                #rendering the model to an image
                shape3D = utils.getShape3D(mean3DShape, blendshapes, modelParams)
                renderedImg = renderer.render(shape3D)

                #blending of the rendered face with the image
                mask = np.copy(renderedImg[:, :, 0])
                renderedImg = ImageProcessing.colorTransfer(cameraImg, renderedImg, mask)
                cameraImg = ImageProcessing.blendImages(renderedImg, cameraImg, mask)


                #drawing of the mesh and keypoints
                if drawOverlay:
                    drawPoints(cameraImg, shape2D.T)
                    drawProjectedShape(cameraImg, [mean3DShape, blendshapes], projectionModel, mesh, modelParams, lockedTranslation)

        if writer is not None:
            writer.write(cameraImg)

        cv2.imshow('Face Swap', cameraImg)
        key = cv2.waitKey(1)

        if key == 27:
            if save_video == 2:
                print("Stopping video writer")
                writer.release()
            break

        if cv2.getWindowProperty('Face Swap', cv2.WND_PROP_VISIBLE) < 1:
            if save_video == 2:
                print("Stopping video writer")
                writer.release()
            break

        if key == ord('t'):
            drawOverlay = not drawOverlay
        # if key == ord('r'):
        if save_video == 1:
            if writer is None:
                # print "Starting video writer"
                writer = cv2.VideoWriter(output_video_path+"//"+time.strftime("%Y%m%d-%H%M%S")+".avi", cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10, (cameraImg.shape[1], cameraImg.shape[0]))

                if writer.isOpened():
                    print("Writer succesfully opened")
                else:
                    writer = None
                    print("Writer opening failed")
                save_video = 2
            # else:
            #     print("Stopping video writer")
            #     writer.release()
            #     writer = None

