# Detect-web
Lib:

    opencv: sudo apt-get install libopencv-dev (for yolo)
    opencv 3.x (install from pip or conda)
    Cuda 10.1 
	python 3.6.10	
	bs4
	validators
	pillow 7.1.2
	matplotlib 3.0.0

Install Chrominum:

    https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/ (only step 3)

Run: 

	Edit Makefile 
		GPU=1
		CUDNN=1
		CUDNN_HALF=1
		OPENCV=1
		AVX=1
		OPENMP=1
		LIBSO=1
	run make
	download Model and copy to .../v3medium/backup folder: https://drive.google.com/file/d/11GXiOKokx3bCNyK0YOrurNrezDXrAdeF/view?usp=sharing
	Run file Classify_Web.py, input URL	
