# VMDetectTool

This is a tool to execute a set of methods for detecting Virtual Environments in differents virtualization vendors. From start it just detect Linux systems, but with expectations to upgrade it to detect Windows. This proyect is open source and code free. 

By default, it uses all the methods contained in the folder /methods, but you can execute an analysis with a personal method file.

## Getting Started

To install this tool you just have to:

```
git clone https://github.com/adrianalvarezsa/VMDetectTool 
cd VMDetectTool
```

An then just execute the included script for installing the tool in /usr/share and downloading the dependences in requirements.txt:

```
sudo bash install.sh
```
### Prerequisites

All the dependences used by this tool are in the requirements.txt: 

* py-cpuinfo
* psutil
* InquirerPy


## Running the tool

There are two ways to execute VMDetectTool: 

* Interactive style: 
```
sudo python3 vmdetect.py
```
* Arguments style:
```
sudo python3 vmdetect.py --check (VMware or VirtualBox) --file (the file of methods you want to use) 
```

##  Example of execution


![VMware analysis](https://github.com/adrianalvarezsa/VMDetectTool/blob/master/images/test_vmware.PNG)

## Developed with: 

* [Python 3](https://www.python.org/downloads/)- The language I used to develop the tool

