Hey doobers:
Here's what you should do after you checkout this repo for the first time:
0. install python3 if you haven't already

1. `C:> pyvenv lang_gen_venv` This will set up a virtual environment for this
   project. DO IT. You can call it something besides `lang_gen_venv`, but just
   fucking do it, ok?

2. `C:> lang_gen_venv/Scripts/activate.bat` This will 'activate' your virtual
   environment, so you can use the proper packages and python version without
   having to think about it

3. `C:> python3 nltk/setup.py` This will install NLTK 3.0a3, the latest version
   of NLTK 3, which is Py3k compatible. `pip3 install nltk` won't cut it, since
   they haven't released a stable version of NLTK 3 on PyPi yet.

If you guys could have this done by Saturday, that'd be great! GO TEAM!

Here is what you do if you are a use windows.  

1. 	install python 3 like normal

2.  Add python to the Environmental variables,
	Right click on 'This computer', click on advanced system settings, 
	on the 'Advanced' tab click on 'Environment Variables...'
	Under 'System Variable' scroll down to path, 
	click edit and add ';C:\python33;C:\python33\Scripts' (or where ever you put python, this is default)
	This will allow command line to use 'python' and any added script as a function

3. 	Install PIP, Easy_install nltk-3.0a3, setuptools
	*I put the files in the github repot for you*
	in command line, go to the folder where the files are located 'cd C:\Documents\GitHub\language_generator'
	and the use the command to open the py document 'python get-pip.py'
	this will install each file, for the zips, you must unzip do the same for the 'setup.py' for each
	
4.	Install virtualenv
	at command line 'easy_install virtualenv==1.01.1'
	this should install the correct version for you to have it work
	
5. 	run virtualenv
	in command line 'virtualenv lang_gen_env' or whatever you want