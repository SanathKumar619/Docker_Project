# Docker_Project
Creating a python app using Docker containers : 

1. Create a Python app (without using Docker)

  * Copy and paste this entire command into the terminal. The result of running this command will create a file named app.py.

    echo 'from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "hello world!"

    if __name__ == "__main__":
        app.run(host="0.0.0.0")' > app.py
  
    This is a simple Python app that uses Flask to expose an HTTP web server on port 5000. (5000 is the default port for flask.) Don't worry if you are not too familiar with Python or Flask. These concepts can be applied to an               application written in any language.

  * Optional: If you have Python and pip installed, run this app locally. If not, download the requirements by running following commands..
    $ python3 --version
    Python 3.6.1
    $ pip3 --version
    pip 9.0.1 from /usr/local/lib/python3.6/site-packages (python 3.6)
    $ pip3 install flask
    $ python3 app.py
  
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    Then just visit that link to make sure that your app is running.

2. Create and build the Docker image.

     If you don't have Python installed locally, don't worry because you don't need it. One of the advantages of using Docker containers is that you can build Python into your containers without having Python installed on your host.

   * Create a file named Dockerfile using the touch command. This will create an empty Dockerfile. A Dockerfile is basically a text document that contains all the commands a user could call on the command line to assemble an image.

     touch Dockerfile

   * Add the following content to the Dockerfile . Click Editor button in the instance window to see the Dockerfile. Select the Dockerfile below the root folder and add the add the following content within it

     FROM python:3.6.1-alpine
     RUN pip install --upgrade pip
     RUN pip install flask
     CMD ["python","app.py"]
     COPY app.py /app.py
     
   * Let's understand the commands in the Dockerfile line by line.
     FROM python:3.6.1-alpine
     This is the starting point for your Dockerfile. Every Dockerfile typically starts with a FROM line that is the starting image to build your layers on top of. In this case, you are selecting the python:3.6.1-alpine base layer             because it already has the version of Python and pip that you need to run your application. The alpine version means that it uses the alpine distribution, which is significantly smaller than an alternative flavor of Linux. A             smaller image means it will download (deploy) much faster, and it is also more secure because it has a smaller attack surface.

     Here you are using the 3.6.1-alpine tag for the Python image. Look at the available tags for the official Python image on the Docker Hub. It is best practice to use a specific tag when inheriting a parent image so that changes to        the parent dependency are controlled. If no tag is specified, the latest tag takes effect, which acts as a dynamic pointer that points to the latest version of an image.

     For security reasons, you must understand the layers that you build your docker image on top of. For that reason, it is highly recommended to only use official images found in the Docker Hub, or noncommunity images found in the          Docker Store. These images are vetted to meet certain security requirements, and also have very good documentation for users to follow. You can find more information about this Python base image and other images that you can use on      the Docker store.

     For a more complex application, you might need to use a FROM image that is higher up the chain. For example, the parent Dockerfile for your Python application starts with FROM alpine, then specifies a series of CMD and RUN commands      for the image. If you needed more control, you could start with FROM alpine (or a different distribution) and run those steps yourself. However, to start, it's recommended that you use an official image that closely matches your         needs.

     RUN pip install flask
     The RUN command executes commands needed to set up your image for your application, such as installing packages, editing files, or changing file permissions. In this case, you are installing Flask. The RUN commands are executed at       build time and are added to the layers of your image.

     CMD ["python","app.py"]
     CMD is the command that is executed when you start a container. Here, you are using CMD to run your Python applcation.

     There can be only one CMD per Dockerfile. If you specify more than one CMD, then the last CMD will take effect. The parent python:3.6.1-alpine also specifies a CMD (CMD python2). You can look at the Dockerfile for the official           python:alpine image.

     You can use the official Python image directly to run Python scripts without installing Python on your host. However, in this case, you are creating a custom image to include your source so that you can build an image with your          application and ship it to other environments.

     COPY app.py /app.py
     This line copies the app.py file in the local directory (where you will run docker image build) into a new layer of the image. This instruction is the last line in the Dockerfile. Layers that change frequently, such as copying           source code into the image, should be placed near the bottom of the file to take full advantage of the Docker layer cache. This allows you to avoid rebuilding layers that could otherwise be cached. For instance, if there was a           change in the FROM instruction, it will invalidate the cache for all subsequent layers of this image. You'll see this little later in this lab.

     It seems counter-intuitive to put this line after the CMD ["python","app.py"] line. Remember, the CMD line is executed only when the container is started, so you won't get a file not found error here.
     And there you have it: a very simple Dockerfile. See the full list of commands that you can put into a Dockerfile. Now that you've defined the Dockerfile, you'll use it to build your custom docker image.

   * Click on Save and close the Editor window.

   * Return to terminal in the instance window and type the command given below. You can verify the contents of the Dockerfile within the terminal window.

     vi Dockerfile
     
   * Now enter the command below  and press <Enter>  to close the Dockerfile opened within the terminal.
     :wq
     
   * Now that you've defined the Dockerfile, you'll use it to build your custom docker image.

   * Build the Docker image. Pass in the -t parameter to name your image python-hello-world
     Docker build -t sanath-world .
   * verify the image by running 
     Docker images

3. Run the Docker image
   * Now that you have built the image, you can run it to see that it works.

     Run the Docker image:

     $ docker run -p 5001:5000 -d sanath-world
     0b2ba61df37fb4038d9ae5d145740c63c2c211ae2729fc27dc01b82b5aaafa26
     The -p flag maps a port running inside the container to your host. In this case, you're mapping the Python app running on port 5000 inside the container to port 5001 on your host. Note that if port 5001 is already being used by          another application on your host, you might need to replace 5001 with another value, such as 5002.

     Navigate to http://localhost:5001 in a browser to see the results.

     You should see "hello world from Sanath Kumar!" in your browser.
   
   * Check the log output of the container.

     If you want to see logs from your application, you can use the docker container logs command. By default, docker container logs prints out what is sent to standard out by your application. Use the command docker container ls to          find the ID for your running container.

     $ docker logs [container id] 
  
     The Dockerfile is used to create reproducible builds for your application. A common workflow is to have your CI/CD automation run docker image build as part of its build process. After images are built, they will be sent to a            central registry where they can be accessed by all environments (such as a test environment) that need to run instances of that application. In the next section, you will push your custom image to the public Docker registry, which       is the Docker Hub, where it can be consumed by other developers and operators.

4. Push to a central registry

   * Navigate to Docker Hub and create a free account if you haven't already.

     Here we will use the Docker Hub as your central registry. Docker Hub is a free service to publicly store available images. You can also pay to store private images.
     Most organizations that use Docker extensively will set up their own registry internally. To simplify things, you will use  Docker Hub, but the following concepts apply to any registry.

   * Log in to the Docker registry account by entering docker login on your terminal:

     $ docker login
     Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
     Username: 
    
    * Tag the image with your username.

      The Docker Hub naming convention is to tag your image with [dockerhub username]/[image name]. To do this, tag your previously created image python-hello-world to fit that format.

      $ docker tag sanath-world [dockerhub username]/sanath-world
    * After you properly tag the image, use the docker push command to push your image to the Docker Hub registry:
      $ docker push [dockerhub username]/sanath-world
      
    * Check your image on Docker Hub in your browser.

      Navigate to Docker Hub and go to your profile to see your uploaded image.

      Now that your image is on Docker Hub, other developers and operators can use the docker pull command to deploy your image to other environments.
      Remember: Docker images contain all the dependencies that they need to run an application within the image. This is useful because you no longer need to worry about environment drift (version differences) when you rely on                dependencies that are installed on every environment you deploy to. You also don't need to follow more steps to provision these environments. Just one step: install docker, and that's it.

5. Deploy a change

   * Update app.py by replacing the string "Hello World" with "Hello Beautiful World!" in app.py.

     Your file should have the following contents:

     from flask import Flask

     app = Flask(__name__)

     @app.route("/")
     def hello():
        return "Hello World from sanath kumar and his puppy!"


     if __name__ == "__main__":
         app.run(host='0.0.0.0')
    
     Now that your application is updated, you need to rebuild your app and push it to the Docker Hub registry.

   * Rebuild the app by using your Docker Hub username in the build command:
     $docker build -t sanath-world .
   * Push it to docker hub
     $ docker push [dockerhub username]/sanath-world
   * We can get details about layers of image by the below command :
     $ docker history sanath-world
     
6. Remove the containers
   * Get a list of the containers running by running the command docker ps
   * Run docker container stop [container id] for each container in the list that is running
   * Remove the stopped containers by running docker system prune

Note : Main python code and Dockerfile codes are attached to this repo.
       Here is the docker image link to view : https://hub.docker.com/r/sanathkumar0939/hello-sanath
