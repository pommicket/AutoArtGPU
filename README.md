# AutoArtGPU
AutoArt that uses OpenCL to run on your GPU

This is the GPU version of [AutoArt](https://github.com/pommicket/AutoArt).

**AutoArtGPU requires the following dependencies:**

AutoImages:
- Python
- PIL/Pillow
- Numpy
- PyOpenCL

AutoVideos:
- Python
- OpenCV
- Numpy
- PyOpenCL

AutoAudio:
- Python
- Numpy
- PyOpenCL

On Ubuntu/Debian you can get them using:  
`sudo apt-get install python python-pil python-numpy python-pyopencl python-opencv`

On other platforms, you can use pip, or visit the libraries' websites.

To run AutoImages:  
`python AutoImagesGPU2.py`  
To run AutoVideos:  
`python AutoVideosGPU2.py`  
To run AutoAudio:  
`python AutoAudioGPU.py`
