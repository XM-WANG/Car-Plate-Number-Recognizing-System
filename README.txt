#0.There is report.pdf in the folder. Please check the overview in this pdf file.


#1.Description：
	
	My project is deploy a car plate number recognizing model based on deep learning on a Flask server for user to use.
The GUI based on Telegram and my server offer services to user via Telegram bot. 
	
	This system can deploy with a car parking lot camera together to monitor the car coming in or out automatically. But 
I do not have a camera so I regard the Telegram bot as a camera and when user send a picture to bot, it means a car coming.
The server would recognize the car number firstly and the check the number in the database. If there is no same number in 
the database, we can consider that the car is coming in and insert this number into database. If there is a same number in 
the database, we can consider that the car is coming out and delete this car's record from the database.

#2.Function:
	
	There are 3 API for user to use:
	
	-User can send my Telegram bot a picture with a Chinese car and the bot would send back the car number to user.
		-If this car number is the first time seen by the bot, the bot would reply "XXXXX In".
		-If this car number is the second time seen by the bot, the bot would reply "XXXXX Out".
	
	-User can send "/getnumber" command to check how many place in the car parking available. I assume there are 100
	 place originally and the bot would send the real-time number back.
	
	-User can send "/left" command to check which cars are still in the car parking. I design this function for manager
	 but now every one can try it on Telegram.

#3.Model:
	
	-Work Flow:
		-Detect the approximate location of the car number by HAAR Cascade, a function in OpenCV library.
		-Extend the location to a rectangle region.
		-Do image binarization and fitting the upper bound and lower bound of the car number by RANSAC.
		-Find the left bound and right bound of the car number by CNN Regression.
		-Use CNN sliding window to split numbers and words.
		-Use CNN to recognize numbers and words.
	
	-Python Dependency:
		-Keras (>2.0.0)
		-Theano(>0.9) or Tensorflow(>1.1.x)
		-Numpy (>1.10)
		-Scipy (0.19.1)
		-OpenCV(>3.0)
		-Scikit-image (0.13.0)
		-PIL
	
	-Package Install
		pip install hyperlpr
		
	-Fast Test 
		You can use the code bellow to have a try :)
		
		from hyperlpr import *
		import cv2
		
		image = cv2.imread("demo.jpg")
		print(HyperLPR_PlateRecogntion(image))
		
#4. Communication:
	
	The server and bot communicate with each other by HTTP and the architecture is similar as assignment2.
	For more details please check my report.
	
		
	
