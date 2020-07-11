import dlib
import cv2
import numpy as np

import models
import NonLinearLeastSquares
import ImageProcessing
import settings_storage
import FaceRendering
import utils

from drawing import *

import os
import time


def imageswap(cameraImg,detector, predictor, maxImageSizeForDetection, projectionModel,
               mean3DShape, idxs3D, idxs2D, blendshapes, renderer,save_image, output_image_path):

    shapes2D = utils.getFaceKeypoints(cameraImg, detector, predictor, maxImageSizeForDetection)

    if shapes2D is not None:
        for shape2D in shapes2D:
            # 3D model parameter initialization
            modelParams = projectionModel.getInitialParameters(mean3DShape[:, idxs3D], shape2D[:, idxs2D])

            # 3D model parameter optimization
            modelParams = NonLinearLeastSquares.GaussNewton(modelParams, projectionModel.residual,
                                                            projectionModel.jacobian, (
                                                                [mean3DShape[:, idxs3D], blendshapes[:, :, idxs3D]],
                                                                shape2D[:, idxs2D]), verbose=0)

            # rendering the model to an image
            shape3D = utils.getShape3D(mean3DShape, blendshapes, modelParams)
            renderedImg = renderer.render(shape3D)

            # blending of the rendered face with the image
            mask = np.copy(renderedImg[:, :, 0])
            renderedImg = ImageProcessing.colorTransfer(cameraImg, renderedImg, mask)
            cameraImg = ImageProcessing.blendImages(renderedImg, cameraImg, mask)

    if save_image == 1:
        cv2.imwrite(output_image_path + "//" + time.strftime("%Y%m%d-%H%M%S") + ".jpg",cameraImg)

    h, w = cameraImg.shape[0], cameraImg.shape[1]
    if w > 1000 or h > 600:
        w, h = w//2, h//2
    cameraImg = cv2.resize(cameraImg, (w, h))  # Resize image
    cv2.imshow('Face Swap', cameraImg)
    key = cv2.waitKey(0)

    if key == 27:
        return

    if cv2.getWindowProperty('Face Swap', cv2.WND_PROP_VISIBLE) < 1:
        return


def webcamswap(cap,detector, predictor, maxImageSizeForDetection, projectionModel,
               mean3DShape, idxs3D, idxs2D, blendshapes, renderer,mesh, save_video, output_video_path):

    writer = None
    drawOverlay = False
    lockedTranslation = False

    while True:
        ret, cameraImg = cap.read()

        if ret is False:  # checks for the last frame and quits
            break

        shapes2D = utils.getFaceKeypoints(cameraImg, detector, predictor, maxImageSizeForDetection)

        if shapes2D is not None:
            for shape2D in shapes2D:
                # 3D model parameter initialization
                modelParams = projectionModel.getInitialParameters(mean3DShape[:, idxs3D], shape2D[:, idxs2D])

                # 3D model parameter optimization
                modelParams = NonLinearLeastSquares.GaussNewton(modelParams, projectionModel.residual,
                                                                projectionModel.jacobian, (
                                                                [mean3DShape[:, idxs3D], blendshapes[:, :, idxs3D]],
                                                                shape2D[:, idxs2D]), verbose=0)

                # rendering the model to an image
                shape3D = utils.getShape3D(mean3DShape, blendshapes, modelParams)
                renderedImg = renderer.render(shape3D)

                # blending of the rendered face with the image
                mask = np.copy(renderedImg[:, :, 0])
                renderedImg = ImageProcessing.colorTransfer(cameraImg, renderedImg, mask)
                cameraImg = ImageProcessing.blendImages(renderedImg, cameraImg, mask)

                # drawing of the mesh and keypoints
                if drawOverlay:
                    drawPoints(cameraImg, shape2D.T)
                    drawProjectedShape(cameraImg, [mean3DShape, blendshapes], projectionModel, mesh, modelParams,
                                       lockedTranslation)

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

                writer = cv2.VideoWriter(output_video_path + "//" + time.strftime("%Y%m%d-%H%M%S") + ".avi",
                                         cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 15,
                                         (cameraImg.shape[1], cameraImg.shape[0]))

                if writer.isOpened():
                    print("Writer succesfully opened")
                else:
                    writer = None
                    print("Writer opening failed")
                save_video = 2

    cap.release()


def faceswap(source, path = None):

    source_image_path, output_image_path, dlib_model, output_video_path, save_image, save_video = \
        settings_storage.fetch_settings()

    #loading the keypoint detection model, the image and the 3D model
    predictor_path = os.getcwd()+"\\models\\"+dlib_model
    image_name = source_image_path

    #the smaller this value gets the faster the detection will work
    #if it is too small, the user's face might not be detected
    maxImageSizeForDetection = 320

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    mean3DShape, blendshapes, mesh, idxs3D, idxs2D = utils.load3DFaceModel("candide.npz")

    projectionModel = models.OrthographicProjectionBlendshapes(blendshapes.shape[0])

    if source == "video":
        cap = cv2.VideoCapture(path)
        cameraImg = cap.read()[1]
    elif source == "webcam":
        cap = cv2.VideoCapture(0)
        cameraImg = cap.read()[1]
    elif source == "image":
        cap = cv2.imread(path)
        cameraImg = cap

    try:
        textureImg = cv2.imread(image_name)
        textureCoords = utils.getFaceTextureCoords(textureImg, mean3DShape, blendshapes, idxs2D, idxs3D, detector, predictor)
        renderer = FaceRendering.FaceRenderer(cameraImg, textureImg, textureCoords, mesh, source)

        if source == "webcam" or source =="video":
            webcamswap(cap,detector, predictor, maxImageSizeForDetection, projectionModel,
                       mean3DShape, idxs3D, idxs2D, blendshapes, renderer,mesh, save_video, output_video_path)

        elif source == "image":
            imageswap(cameraImg, detector, predictor, maxImageSizeForDetection, projectionModel,
                          mean3DShape, idxs3D, idxs2D, blendshapes, renderer,save_image, output_image_path)

    except Exception as e:
        return "error"
