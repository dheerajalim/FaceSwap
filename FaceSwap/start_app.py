import eel
import faceswap
import cv2
import pygame
import wx
import settings_storage
import pymsgbox

eel.init('web')


def select_file(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Choose File', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = ""
    dialog.Destroy()
    return path


@eel.expose
def start_faceswap(source,path=None):
    err = faceswap.faceswap(source,path)
    if err == "error":
        pymsgbox.alert("Source image is either not selected or has some issue, please check settings", 'Face Swap Error')
    else:
        cv2.destroyAllWindows()
        pygame.display.quit()



@eel.expose
def faceswap_file(source):

    if source == "image":
        path = select_file("JPEG and JPG files (*.jpeg;*.jpg)|*.jpeg;*.jpg|PNG files ("
                           "*.png)|*.png")
    elif source == "video":
        path = select_file("Video files|*.avi;*flv;*.mkv;*.mov;*.mp4;*.webm;*.wmv")
    if path == "":
        return

    start_faceswap(source,path)


@eel.expose
def load_settings():
    source_image_path, output_image_path, dlib_model, output_video_path, save_image, save_video = \
        settings_storage.fetch_settings()

    return (source_image_path, output_image_path, dlib_model, output_video_path, save_image, save_video)


@eel.expose
def face_location_path():
    path = select_file("JPEG and JPG files (*.jpeg;*.jpg)|*.jpeg;*.jpg|PNG files ("
                       "*.png)|*.png")
    return path


@eel.expose
def output_dir():
    app = wx.App(None)
    style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
    dialog = wx.DirDialog(None, 'Choose output directory', "", style=style)

    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = ""
    dialog.Destroy()
    return path


@eel.expose
def save_settings(face_location_path_value, dlibmodel, image_output_dir_path_value, video_output_dir_path_value,
                  saveimage, savevideo):

    result = settings_storage.create_record(face_location_path_value, image_output_dir_path_value,dlibmodel,
                                            video_output_dir_path_value, saveimage, savevideo)

    if result:
        pymsgbox.alert("Settings Saved Successfully", 'Face Swap Settings')
        return True

    else:
        pymsgbox.alert("Unable to save settings, please retry", 'Face Swap Settings')
        return False

@eel.expose
def check_settings():

    result = settings_storage.create_table()

    if result:
        return True

    else:
        pymsgbox.alert("Some Error occured. Contact the Developer")
        return False


eel.start('index.html', size=(1000, 600))
