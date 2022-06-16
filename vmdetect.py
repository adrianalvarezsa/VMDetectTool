import subprocess as sb
import os
import json
from datetime import datetime
import cpuinfo
import sys
import argparse
from InquirerPy import inquirer

class Method: 
	def __init__(self): 
		self.name = ""
		self.description = ""
		self.hypervisor = ""
		self.type = ""
		self.path = ""
		self.level = ""	
	
	
def get_string_cpu_info(): 
	cpu_info = "\n" + "Brand: " + cpuinfo.get_cpu_info()['brand_raw'] + "\n" + "Arch: " + cpuinfo.get_cpu_info()['arch_string_raw'] + "\n" + "Vendor: " + cpuinfo.get_cpu_info()['vendor_id_raw'] + "\n" + "CPU cores: " + str(cpuinfo.get_cpu_info()['count']) + "\n"
	return cpu_info
	
def start_report(checks): 
	date = datetime.today()
	report = "------------------------------------------------ \n"
	report = report + "Report generated at: " + str(date) + "\n"
	report = report + get_string_cpu_info() + "\n"
	counter_found = 0
	counter_not_found = 0
	for i in checks: 
		report = report + "-" + i + ":" + "\n"
		if checks[i][0] == 0: 
			report = report + "Evidences were found" + "\n"
			report = report + "Severity: " + checks[i][1] + "\n"
			counter_found += 1
		else: 
			report = report + "Evidences were not found" + "\n"
			report = report + "Severity: " + checks[i][1] + "\n"
			counter_not_found += 1
		report = report + "\n"	
	return report
	

def menu(): 
	print_banner()
	print("\033[0;32m")
	print("-If you select option 1 you display a menu to select the vendor you want the tool to analyze.\n"
	  "-If you select option 2 you can display all the methods available.\n"
	  "-If you select option 3 you will exit the program.\n")
	  
	print("\033[0;36m")
	option = inquirer.select(message="Select an option:", choices=["Check virtual environment", "See available checking methods", "Exit"]).execute()
	if option == "Check virtual environment": 
		menu_check()
	elif option == "See available checking methods":
		menu_available_methods()
	elif option == "Exit": 
		exit(0)
	return 0
	print("\033[0;35m")
   
def menu_check(): 
	path = ""
	option = 0
	env = ""
	choose_file = False
	use_file = False	
	print_banner()
	print("\033[0;32m")
	option = inquirer.select(message="Select the virtualization vendor:", choices=["VirtualBox", "VMware", "Exit"]).execute()
	if option == "VirtualBox": 
	   	print("Check in VBox")
	   	env = "VirtualBox"
	elif option == "VMware":
		print("Check in VMware")
		env = "VMware"
	elif option == "Exit": 
	   	menu()
	   	
	option2 = inquirer.select(message="Do you want to use a personal method file?:", choices=["Yes", "No", "Exit"]).execute()
	choose_file = False
	if option2 == "Yes": 
		use_file = True
		print("Type the full path of the methods dir to use:")
		print("\033[0;37m")
		path = input("")
		print("\033[0;35m") 
		choose_file = True
	elif option2 == "No":
		use_file = False
		choose_file = True
	elif option2 == "Exit": 
	   	menu()
	
	if use_file == True: 
		print("Check in ", env, " with the next method file: ", path)
	else:
		print("Check in ", env, " with predetermined methods")
	check(env, use_file, path, False)
	print("\033[0;35m")
	
	

def check(env, use_file, path, use_args):
	if use_args == False:
		print_banner()
	if use_file == True and os.path.exists(path) == False:
		print("The path introduced (" + path + ") was not found")
		if use_args == True: 
			exit()
		else: 
			print("\033[0;32m")
			print("Do you want to go back menu? (y - menu, n - exit)" + "\033[0;37m")

			option = input("")
			if option == "y": 
				menu()
			elif option == "n": 
				return 0
			else: 
				menu()
	else: 
		env_var = os.environ.copy()
		if use_file == True:
			path = path
		elif "VMDETECT_METHOD_PATH" in env_var:
			path = env_var["VMDETECT_METHOD_PATH"]
		else: 
			path = "/usr/share/vmdetect/methods"
	
		checks = {}
		
		print("\033[0;32m")
		print("The path with checking methods is: ", path)
		print("\n")
		
		files = os.listdir(path)
		
		for i in files: 
			method = Method()
			try:
				with open(path + "/" + i) as f: 
					data = json.load(f)
					method.name = data["name"]
					method.hypervisor = data["hypervisor"]
					method.path = data["path"]
					method.level = data["level"]
					if method.hypervisor == "Generic" or method.hypervisor == env: 
						exit_code = sb.call(method.path)
						checks[method.name] = [exit_code, method.level]
						if exit_code == 0: 
							print("\033[0;37m" + method.name + "........................... " + "\033[0;32m" + "[DETECTED]") 
						else: 
							print("\033[0;37m" + method.name + "........................... " + "\033[0;31m" + "[NOT DETECTED]")
			except: 
				print("There was a problem while executing methods")
				exit(1)
			
		print("\033[0;37m")	
		
		if use_args == True:
			print("\n" + "Starting report... This will take a while...")
			print("\n")
			report = start_report(checks)
			print(report)
			now = datetime.now()
			time = str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)
			report_name = "/usr/share/vmdetect/reports/"+"report" + "_" + str(now.date()) + "_" + time + ".txt"
			r = open(report_name, "w" ,encoding='utf-8')
			r.write(report)
			r.close()
			print("\033[0;32m")
			
		elif use_args == False:
			option2 = inquirer.select(message="Do you want to print a report?:", choices=["Yes", "No"]).execute()
			if option2 == "Yes": 
				print("\n" + "Starting report... This will take a while...")
				print("\n")
				report = start_report(checks)
				print(report)
				now = datetime.now()
				time = str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)
				report_name = "/usr/share/vmdetect/reports/"+"report" + "_" + str(now.date()) + "_" + time + ".txt"
				r = open(report_name, "w" ,encoding='utf-8')
				r.write(report)
				r.close()
				print("\033[0;32m")
				option3 = inquirer.select(message="Do you want to go back to menu?:", choices=["Go menu", "Exit"]).execute()
				if option3 == "Go menu": 
					menu()
				elif option3 == "Exit": 
					exit(0)
			
def menu_available_methods(): 
	option = 0
	env = ""
	print_banner()	   	
	option = inquirer.select(message="Select the virtualization vendor:", choices=["VirtualBox", "VMware", "Exit"]).execute()
	
	if option == "VirtualBox": 
	   	print("Check in VBox")
	   	env = "VirtualBox"
	elif option == "VMware":
		print("Check in VMware")
		env = "VMware"
	elif option == "Exit": 
	   	menu()
	
	print("\033[0;35m")
		   	
	print_banner()
	
	env_var = os.environ.copy()
	if "VMDETECT_METHOD_PATH" in env_var:
		path = env_var["VMDETECT_METHOD_PATH"]
	else: 
		path = "/usr/share/vmdetect/methods"
	
	print("\033[0;32m")
	print("The path with checking methods is: ", path)
	print("\033[0;37m")
	
	files = os.listdir(path)
	
	print("")
	print("\033[0;35m")
	print("--------------------------------------------------------------------------------")
	for i in files: 
		method = Method()
		try:
			with open(path + "/" + i) as f: 
				data = json.load(f)
				method.name = data["name"]
				method.description = data["description"]
				method.hypervisor = data["hypervisor"]
				method.type = data["type"]
				method.path = data["path"]
				method.level = data["level"]
				if method.hypervisor == env or method.hypervisor == "Generic":
					print("")
					print("\033[0;36m" + "File: " + "\033[0;37m" + i)
					print("\033[0;36m" + "Name: " + "\033[0;37m" + method.name)
					print("\033[0;36m" + "Description: " + "\033[0;37m" + method.description)
					print("\033[0;36m" + "Type: " + "\033[0;37m" + method.type)
					print("\033[0;36m" + "Hypervisor: " + "\033[0;37m" + method.hypervisor)
					print("\033[0;36m" + "Script Path: " + "\033[0;37m" + method.path)
					if method.level == "LOW": 
						print("\033[0;36m" + "Level: " + "\033[0;32m" + "LOW")
					elif method.level == "MEDIUM": 
						print("\033[0;36m" + "Level: " + "\033[0;33m" + "MEDIUM")
					elif method.level == "HIGH": 
						print("\033[0;36m" + "Level: " + "\033[0;31m" + "HIGH")
					print("\033[0;35m")
					print("--------------------------------------------------------------------------------")
		except:
			("There was a problem while obtaining methods information")
			exit(1)
		
	print("\033[0;32m")
	option2 = inquirer.select(message="Do you want to go back to menu?:", choices=["Go menu", "Exit"]).execute()
	if option2 == "Go menu": 
		menu()
	elif option2 == "Exit": 
		exit(0)
		
def print_banner():

	sb.run("clear")
	print("\033[1;33m")

	print("	 ██╗░░░██╗███╗░░░███╗██████╗░███████╗████████╗███████╗░█████╗░████████╗ \n"
	  "	 ██║░░░██║████╗░████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗╚══██╔══╝\n"
	  " 	 ╚██╗░██╔╝██╔████╔██║██║░░██║█████╗░░░░░██║░░░█████╗░░██║░░╚═╝░░░██║░░░\n"
	  "	 ░╚████╔╝░██║╚██╔╝██║██║░░██║██╔══╝░░░░░██║░░░██╔══╝░░██║░░██╗░░░██║░░░\n"
	  "	 ░░╚██╔╝░░██║░╚═╝░██║██████╔╝███████╗░░░██║░░░███████╗╚█████╔╝░░░██║░░░\n"
	  "	 ░░░╚═╝░░░╚═╝░░░░░╚═╝╚═════╝░╚══════╝░░░╚═╝░░░╚══════╝░╚════╝░░░░╚═╝░░░\n")


	print("			████████╗░█████╗░░█████╗░██╗░░░░░ \n"
	  "			╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░ \n"
	  "			░░░██║░░░██║░░██║██║░░██║██║░░░░░ \n"
	  "			░░░██║░░░██║░░██║██║░░██║██║░░░░░ \n"
	  "			░░░██║░░░╚█████╔╝╚█████╔╝███████╗ \n"
	  "			░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝ \n")

	print("\n")
	print("                                                Author -> Adrián Álvarez Sánchez")

	print("\033[4;34m")
	print("Version 1.0.0")
	print("\n")

	print("\033[0;31m")
	print("This is a tool to detect Virtual Environments in differents virtualization vendors. \n"
	  "From start it just detect Linux systems, but with expectations to upgrade it to detect Windows.\n"
	  "This proyect is open source and code free so you can check it on:\n"
	  "https://github.com/adrianalvarezsa/vmdetectTool\n")
	print("\033[0;37m")




if __name__ == '__main__':
	if len(sys.argv) == 1:
		menu()
	else:
		parser = argparse.ArgumentParser(description = "This is a tool to detect Virtual Environments in differents virtualization vendors.")
		parser.add_argument('--check', '-c',dest='env',help='Check if your system is working on VirtualBox (vbox) or VMware (vmware)',required=True)
		parser.add_argument('--file', '-f',dest='file',help='Check if your system is working on VirtualBox (vbox) or VMware (vware)',required=False)
		args = parser.parse_args()
		
		if (args.env.lower() == "vbox") or (args.env.lower() == "vmware"):
			if args.file:
				check(args.env, True, args.file, True)
			else: 
				check(args.env, False, "", True)
		else: 
			print("The -c or --check value introduced was wrong. Please, try again with vbox or vmware")
		

