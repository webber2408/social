import redis
import time
import ast
import pprint , pickle
import os
import signal

try:
	conn = redis.StrictRedis(
       host='localhost',
       port= 6379,
       db= 0)
	print conn
	conn.ping()
	print 'Connected!'
except Exception as ex:
	print 'Error:',ex
	exit('Failed to connect , terminating .')

	# basic database model for users 
users = {

	"root":{
	 	 "password":"12345",
	 	 "skillset":[],
	 	 "year":0,
	 	 "batch":"",
	 	 "contactno":0,
	 	 "type":{
	 	    "project":{
	 	       "author":"ram",
	 	       "description":"this is my project!",
	 	       "teammembers":['ram','shyam'],
	 	       "likes":0,
	 	       "comments":['Nice Project!']
	 	    },
	 	    "startup":{
	 	        "ceo":"ram",
	 	       "description":"this is my startup!",
	 	       "teammembers":['ram','shyam'],
	 	       "likes":0,
	 	       "comments":['Nice Startup!'],
	 	       "skills":[],
	 	       "flag_intern":0,
	 	       "applicant_request":[]
	 	    }
	 	 }
	}


}

def load(users):
	output = open('data.pkl','wb')
	pickle.dump(users,output)
	output.close()
	unpack = open('data.pkl','rb')
	un = pickle.load(unpack)
	unpack.close()
	pack = pickle.dumps(un)
	conn.set("use",pack)

def unload():
	# ans = conn.get("use")
	# print ans
	user= pickle.loads(conn.get("use"))
	return user

def likes(username):
	print "Enter name of the user whose post you want to like "
	name = raw_input()
	users=unload()
	if name in users:
		print "Enter project or startup name you want to like ?"
		ans = raw_input()
		if ans in users[name]["type"]:
			# print ans
			# print users[name]["type"][ans]["likes"]
			users[name]["type"][ans]["likes"] = users[name]["type"][ans]["likes"] +1
			load(users)
		else:
			print "Sorry project not found ! Redirecting to dashboard ....."
			dashboard(username)
	else:
		print "Sorry user not found ! Redirecting to dashboard ...."
		dashboard(username)


def comments(username):
	print "Enter name of the user whose post you want to add comment to  "
	name = raw_input()
	users=unload()
	if name in users:
		print "Enter project or startup name you want to add comment in ?"
		ans = raw_input()
		if ans in users[name]["type"]:
			print "Enter comment !"
			comment = raw_input()
			users[name]["type"][ans]["comments"].append(comment)
			load(users)
		else:
			print "Sorry project not found ! Redirecting to dashboard ....."
			dashboard(username)
	else:
		print "Sorry user not found ! Redirecting to dashboard ...."
		dashboard(username)

#end of users model 
def dashboard(username):
	
	print "***********************************************"
	print "YOU ARE VIEWING DASHBOARD !"
	print "***********************************************"
	users=unload()
	printall(users)
	print "\n"
	print "***********************************************"
	print "Want to like or comment a post ? (1/0) . Reply 2 for Not !"
	print "***********************************************"
	choice = raw_input()
	if choice == '1':
		likes(username)
	elif choice == '0':
		comments(username)
	else:
		print "Opted Nothing !"



def logout():
	
	print "You are going to be logged out in 5 seconds "
	for i in range(1,5):
		print i
		time.sleep(1)
	os.kill(os.getppid(), signal.SIGHUP)

def panel(username):
	print "***********************************************"
	print "WELCOME TO THE SOCIAL PANEL !"
	print "***********************************************"
	print "Enter Choice 1)Upload Project 2)Upload StartUp 3)View Profile 4)View Dashboard   5)Logout  6)AskforIntern Panel 7)Interns Panel\n"

	choice = raw_input("Choice?")
	if choice == '5':
		logout()
	else:
		update(choice,username)
		print "***********************************************\n"


def printall(users):
	for k, v in users.iteritems():
		if isinstance(v, dict):
			if k == "type":
				print "*****Project / Startup Details****"
				printall(v)
				print "**********************************\n"
			else:
				print "<=======",k,"========>"
				printall(v)
		else:
			if not k == "password":
				print "{0} : {1}".format(k, v)

# under construction
def askintern(users,username):
	load(users)
	users=unload()
	print "**********************************************"
	print "*          Ask For Interns Panel             *"
	print "**********************************************"
	print users
	print "Enter for which startup you want interns :"
	ans1 = raw_input()
	if ans1 in users[username]["type"]:
		print "Do you want to post your internship or withdraw ?(1/0)"
    	choice=raw_input('Choice ?')
    	if choice == '1':
    		if users[username]["type"][ans1]["flag_intern"]==1:
    			print "You have already posted !"
    			panel(username)
    		elif users[username]["type"][ans1]["flag_intern"]==0:
    			users[username]["type"][ans1]["flag_intern"] = 1
    			load(users)
    			print users[username]["type"][ans1]["flag_intern"]
    			print "Successfully asked for interns !"
    			panel(username)
    	elif choice == '0':
    		if users[username]["type"][ans1]["flag_intern"]==1:
    			users[username]["type"][ans1]["flag_intern"] = 0
    			print "Successfully withdrawn !!"
    			panel(username)
    		elif users[username]["type"][ans1]["flag_intern"]==0:
    			print "Cant Withdraw ! No internship post for this startup/project !"
    			panel(username)
	else:
		print "Sorry , startup not found !"
		panel(username)


    	
def internPanel(users,username):
	load(users)
	users=unload()
	printall(users)
	print "**********************************************"
	print "*               Interns Panel                *"
	print "**********************************************"
	for k, v in users.iteritems():
		if isinstance(v,dict):
			print "\nStartup of ==> ",k,""
			for k2,v2 in users[k].iteritems():
				if isinstance(v2,dict) and k2 == "type":
					for k3,v3 in users[k][k2].iteritems():
						if "startup" in k3 and isinstance(v3,dict):
							print "Internship opportunity for ==> ",k3
							for k4,v4 in users[k][k2][k3].iteritems():
								if k4 == "flag_intern" and v4 == 1:
									for k5,v5 in users[k][k2][k3].iteritems():
										if k5 == "skills" and v5:
											print "Skills required are : ",v5	
										elif k5 == "skills" and v5 is None:
											print "Sorry ! No internship posted for this startup ! Keep Looking !"

	print "**************************************************"
	print "Want to apply ? (1/0) "
	ans = raw_input()
	if ans == '1':
		print "Enter name of the person whose startup you want to apply for :"
		fun = raw_input()
		for k,v in users.iteritems():
			if k == fun:
				print "Enter startup name you want to apply for :"
				fun1 = raw_input()
				for k1,v1 in users[k]["type"].iteritems():
					if k1 == fun1:
						users[k]["type"][k1]["applicant_request"].append(username)
						load(users)
						print "Your request has been successfully sent !"
	elif ans=='0':
		panel(username)




# def checkInternResponse():


def editpass(username):
	users=unload()
	newpassword=raw_input("Enter new password :")
	users[username]["password"]=newpassword
	load(users)
	time.sleep(1)
	print "Password Successfully Changed !\n"
	panel(username)

def update(ans,username):
	
	users=unload()
	if ans == '1':
		print "**** POST INCOMPLETE PROJECT ****"
		projectname=raw_input("Enter project name prefixed by word project ")
		author = raw_input('Author ?')
		description = raw_input('Description ?')
		teammembers = raw_input('Enter team members separated by comma (,) :')
		teammembers=teammembers.split(",");
		likeinproject=0
		commentinproject = []
		
		print "Adding Your Project ....... \n"
		print users[username]

		users[username]["type"].update({projectname:{
			 "author":author,
			 "description":description,
			 "teammembers":teammembers,
			 "likes":likeinproject,
			 "comments":commentinproject
			}})
		
		load(users)
		time.sleep(1)
		print "Project successfully added !"
		panel(username)

        	    
	elif ans== '2':
		print "**** POST STARTUP IDEA ****"
		startupname=raw_input("Enter startup name prefixed by word startup ")
		ceo = raw_input('Ceo ?')
		description = raw_input('Description ?')
		teammembers = raw_input('Enter team members separated by comma (,) :')
		teammembers=teammembers.split(",");
		skills=raw_input('Enter what skills you want in your intern separated by comma (,) ?')
		skills=skills.split(",")
		likeinstartup=0
		commentinstartup = []
		
		print "Adding Your Startup idea ....... \n"
		users[username]["type"].update({startupname:{
			 "ceo":ceo,
			 "description":description,
			 "teammembers":teammembers,
			 "likes":likeinstartup,
			 "comments":commentinstartup,
			 "skills":skills,
			 "flag_intern":0,
			 "applicant_request":[]
			}})
		
		load(users)
		time.sleep(1)
		print "Startup idea successfully added !\n"
		panel(username)
        
	elif ans == '3':
		print "****",username,"'s Profile !! **** \n"
		
        
		print " Your Project and Startup idea Details along with password details are \n "
		for key, value in users.iteritems():
			if username in key:
				for k,v in users[username].iteritems():
					if isinstance(v, dict):
						for k,v in users[username]["type"].iteritems():
							print "{0} => {1}".format(k, v)
					else:
						print "{0} => {1}".format(k, v)


					
		
		print "Edit password ?\n"
		passans = raw_input("1/0 ?")
		if passans == '1':
			editpass(username)
		else:
			panel(username)
			

	elif ans=='4':
		print "Redirecting to dashboard............\n"
		time.sleep(1)
		dashboard(username)
		panel(username)
	elif ans=='6':
		# print "Under Construction !"
		# panel(username)
		askintern(users,username)
		panel(username)
	elif ans=='7':
		internPanel(users,username)
		panel(username)
	else:
		print "Invalid choice!"
		panel(username)






def signin():
	print "***********************************************"
	print "WELCOME TO THE SIGN-IN !"
	print "***********************************************"
	print "Enter username: \n"
	username = raw_input()
	print "Enter password : \n"
	password = raw_input()
	
	users=unload()
	
	if username in users:
		print username
		if password == users[username]["password"]:
			print "You have Successfully signed up !\n"
			panel(username)
		else:
			print "Incorrect Password ! Please Login again !\n"
			signin()
	else:
		print "Not Registered ! Go for Signup !\n"
		signup()

	


def signup():
	print "***********************************************"
	print "WELCOME TO THE SOCIAL PANEL !"
	print "***********************************************"
	print "WELCOME TO THE SIGNUP !"
	print "***********************************************"
	print "Enter username:"
	username = raw_input()
	print "Enter password :"
	password = raw_input()
	print "Enter your skills separated by comma (,) !"
	skills_set = raw_input()
	skills_set = skills_set.split(",")
	print "Enter year :"
	year = input()
	print "Enter batch :"
	batch = raw_input()
	print "Enter contact number :"
	contact = input()
	users=unload()
	
	
	users.update({username:{}})
	
	
	users[username]["type"]={}
	
	users[username]["password"]=password
	users[username]["skillset"]=skills_set
	users[username]["contactno"]=contact
	users[username]["batch"]=batch
	users[username]["year"]=year
	print "Signing Up...\n"
	time.sleep(1)
	
	
	
	load(users)
	print "Signed Up successfully !!\n"
	print "Going for signin !\n"

	signin()


def start():
	print "***********************************************"
	print "WELCOME TO THE SOCIAL !"
	print "***********************************************"
	print "Already registered (1) or New User (0) ?"
	ans = raw_input()
	if ans == '1':
		signin()
	elif ans == '0':
		signup()
	else:
		print "Invalid Option!"


start()
