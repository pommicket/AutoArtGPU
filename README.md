# AutoArtGPU
AutoArt that uses OpenCL to run on your GPU

This is the GPU version of [AutoArt](https://github.com/pommicket/AutoArt).

For a live version of AutoVideos that creates them as they play, go to https://github.com/pommicket/AutoVideosLive.

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

Don't worry if when you run it, it gives the following message:  
`/usr/lib/python2.7/dist-packages/pyopencl/__init__.py:61: CompilerWarning: Non-empty compiler output encountered. Set the environment variable PYOPENCL_COMPILER_OUTPUT=1 to see more. "to see more.", CompilerWarning)`

Also don't worry if AutoArt closes at, say, 10/15, prints `Segmentation Fault`, and re-opens saying 0/5, all 15 images will be made.
