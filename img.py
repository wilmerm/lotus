"""
Módulo para suplir de imágenes al programa.
"""

import wx
from var import *








class Image():
    """
    Objeto imagen para la manipulación de imágenes.

    Parámetros:
        path: ruta de la imagen.
    """

    def __init__(self, path):
        self.path = path 

    def GetBitmap(self, w=None, h=None):
        """
        Obtiene un objeto wxBitmap.

        Parámetros:
         - w (width). Ancho de la imagen en pixeles (opcional).
         - h (heigth). Alto de la imagen en pixeles (opcional)
        """
        return wx.Bitmap(self.path, width=w, heigth=h)





def Bitmap(path, w=None, h=None):
    """
    Obtiene un objeto wxBitmap.
    """
    img = wx.Image(path)

    if (w != None) and (h != None):
        img = img.Scale(w, h)
    return img.ConvertToBitmap()
