This repository contains a community builder web application. 
The requirements, mockup screens and MVP report can be found in the wiki pages.

Deployment:
In Google Cloud Platform Virtual Machine is created to serve the site. Also static IP address is attached to the VM. Inside the VM, docker is installed. With docker compose, the website is always in running state. 
You can reach the site with the external ip address and the port. In Github Actions Environment Variables, you can find the static ip address and the port.

Below, you can find necessary commands to start the server from local machine.
How to run the application:
1. Clone the repo
2. Run "docker compose build" command to build image
3. Run "docker compose up" command to run the server
4. Go to http://0.0.0.0:8000/
