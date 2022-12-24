# Backup Missing iPhone Pictures on Windows with Python

On Windows, identify which photos on your iPhone are not already in your local directory and then copy them over into a target folder. 

Currently the script is configured to check which of the iPhone photos are already in the "check" folder "D:\Photos" in lines 7-15, and then copies over missing photos into "target" folder "This PC\Data (D:)\Photos\temp" in lines 27-52.

After changing the "check" folder and the "target" folders to your personal file setup, simply run the code as below.
	
	python backup_phone.py



The only requirements to run the code is pywin32 and tqdm, which you can install below. 

	pip install pywin32==305
	pip install tqdm==4.64.1


## Acknowledgmenets
Huge thanks to Jack Chang on Stack Exchange, who (as far as I can tell as of 12/24/2022) posted the only public code to help solve the issue of how to copy and paste iPhone photos [here](https://stackoverflow.com/a/72842087), which was inspired from Stephen Brodie's post here [here](https://stackoverflow.com/a/65825617)
