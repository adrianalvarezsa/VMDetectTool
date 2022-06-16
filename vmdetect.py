import subprocess as sb
import os
import json
from datetime import datetime
import cpuinfo
import sys
import argparse

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
	  "-If you select option 2 you can add new check manually (on develop).\n"
	  "-If you select option 3 you can see available checks for each vendor.\n")
	print("\n")
	print("\033[0;36m")
	print("[1] Check virtual environment \n")
	print("[2] See available checking methods \n")
	print("[3] Add new checking method \n")
	print("[4] Exit \n")
	print("\033[0;35m")
	option = -1
	while option < 1 or option > 4:
		   print("Choose an option: ", end="")
		   print("\033[0;37m")
		   option = int(input(""))
		   print("\033[0;35m") 
		   print("Choosen option is ", option, "\n")
		   print("\033[0;37m")
		   

		   if option > 0 and option < 5:
			   if option == 1: 
			   	menu_check()
			   elif option == 2:
			   	menu_available_methods()
			   elif option == 3: 
			   	menu_add_new_method()
			   elif option == 4: 
			   	return 0
		   else: 
		   	print("\033[0;35m") 
		   	print("Please, select a valid option")
   
def menu_check(): 
	path = ""
	option = 0
	env = ""
	choose_file = False
	use_file = False	
	print_banner()
	print("\033[0;32m")
	print("Select the hypervisor vendor you want to check:")
	print("\033[0;36m")
	print("[1] Check VirtualBox \n")
	print("[2] Check VMware \n")
	print("[3] Exit to menu \n")
	print("\033[0;35m")
	option = -1
	while option < 1 or option > 3:
		   print("Choose an option: ", end="")
		   print("\033[0;37m")
		   option = int(input(""))
		   print("\033[0;35m") 
		   print("Choosen option is ", option, "\n")

		   if option > 0 and option < 4:
			   if option == 1: 
			   	print("Check in VBox")
			   	env = "VirtualBox"
			   elif option == 2:
			   	print("Check in VMware")
			   	env = "VMware"
			   elif option == 3: 
			   	menu()
		   else: 
		   	print("Please, select a valid option")
	 
	while choose_file == False:
		if option == "y" or option == "yes": 
			use_file = True
			print("Type the full path of the methods dir to use:")
			print("\033[0;37m")
			path = input("")
			print("\033[0;35m") 
			choose_file = True
		elif option == "n" or option == "no": 
			use_file = False
			choose_file = True
		else: 
			print("Do you want to use a personal method file? If not, predetermined methods will be check (y - n): ")
			print("\033[0;37m")
			option = input("")
			print("\033[0;35m")
	if use_file == True: 
		print("Check in ", env, " with the next method file: ", path)
	else:
		print("Check in ", env, " with predetermined methods")
	check(env, use_file, path, False)

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
		if "VMDETECT_METHOD_PATH" in env_var:
			path = env_var["VMDETECT_METHOD_PATH"]
		elif use_file == True:
			path = path
		else: 
			path = "/usr/share/vmdetect/methods"
	
		checks = {}
		
		print("\033[0;32m")
		print("The path with checking methods is: ", path)
		print("\n")
		
		files = os.listdir(path)

		for i in files: 
			with open(path + "/" + i) as f: 
				method = json.load(f)
				if method['hypervisor'] == "Generic" or method['hypervisor'] == env: 
					exit_code = sb.call(method['path'])
					checks[method['name']] = [exit_code, method['level']]
					if exit_code == 0: 
						print("\033[0;37m" + method['name'] + "........................... " + "\033[0;32m" + "[DETECTED]") 
					else: 
						print("\033[0;37m" + method['name'] + "........................... " + "\033[0;31m" + "[NOT DETECTED]")
			
		print("\033[0;37m")	
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
		
		if use_args == False:
			print("\033[0;32m")
			print("Do you want to go back menu? (y - menu, n - exit)" + "\033[0;37m")

			option = input("")
			if option == "y": 
				menu()
			elif option == "n": 
				return 0
			else: 
				menu()
			
def menu_available_methods(): 
	option = 0
	env = ""
	
	print_banner()
	print("\033[0;32m")
	print("Select the hypervisor vendor you want to check:")
	print("\033[0;36m")
	print("[1] Check VirtualBox \n")
	print("[2] Check VMware \n")
	print("[3] Exit to menu \n")
	
	print("\033[0;35m")
	option = -1
	while option < 1 or option > 3:
		   print("Choose an option: ", end="")
		   print("\033[0;37m")
		   option = int(input(""))
		   print("\033[0;35m") 
		   print("Choosen option is ", option, "\n")

		   if option > 0 and option < 4:
			   if option == 1: 
			   	print("Check in VBox")
			   	env = "VirtualBox"
			   elif option == 2:
			   	print("Check in VMware")
			   	env = "VMware"
			   elif option == 3: 
			   	menu()
		   else: 
		   	print("Please, select a valid option")
		   	
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
		with open(path + "/" + i) as f: 
			method = json.load(f)
			if method['hypervisor'] == env or method['hypervisor'] == "Generic":
				print("")
				print("\033[0;36m" + "File: " + "\033[0;37m" + i)
				print("\033[0;36m" + "Name: " + "\033[0;37m" + method['name'])
				print("\033[0;36m" + "Description: " + "\033[0;37m" + method['description'])
				print("\033[0;36m" + "Type: " + "\033[0;37m" + method ['type'])
				print("\033[0;36m" + "Hypervisor: " + "\033[0;37m" + method ['hypervisor'])
				print("\033[0;36m" + "Script Path: " + "\033[0;37m" + method ['path'])
				level = method['level']
				if level == "LOW": 
					print("\033[0;36m" + "Level: " + "\033[0;32m" + "LOW")
				elif level == "MEDIUM": 
					print("\033[0;36m" + "Level: " + "\033[0;33m" + "MEDIUM")
				elif level == "HIGH": 
					print("\033[0;36m" + "Level: " + "\033[0;31m" + "HIGH")
				print("\033[0;35m")
				print("--------------------------------------------------------------------------------")
	
	print("\033[0;32m")
	print("Do you want to go back menu? (y - menu, n - exit)" + "\033[0;37m")

	option = input("")
	if option == "y": 
		menu()
	elif option == "n": 
		return 0
	else: 
		menu()
		
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
	  "From start it just detect Linux, but with expectations to upgrade it to detect Windows.\n"
	  "This proyect is open source and code free so you can check it on https://www.github.com/VMdetect\n")
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
		

