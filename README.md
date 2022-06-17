# Atom Cloud Music

## Project Structure

```
Atom Cloud Music  (root directory)
├── .gitignore    (configuration file: gitignore)
├── LICENSE       (open source license)
├── back-end      (back-end directory)
├── docs          (instructive docs directory)
├── documentation (corresponding documentation: including system document, user document, and reflections)
└── front-end     (front-end directory)
```

## Preview

Our project has been deployed to our server, so you can browse our site via the below url directly.

http://csi420-01-vm3.ucd.ie/

## Set up

If you want to test our project locally, please follow these steps

### Back-end（approach 1: use global Python interpreter）

```shell
$ cd back-end # Enter the back-end directory.
$ pip install -r requirements.txt # Automatically download the packages of related dependencies.
$ flask run # Run back-end program in Flask mode. Be sure to run this command in the back-end directory!
```
### Back-end（approach 2: use local Python virtual environment）

<img src="docs/images/Pycharm build venv.png" style="zoom:50%;" />

1. If you are using Pycharm，please add a new virtual environment by going to `Project->Python Interpretor->Virtualenv Environment` in the settings, as shown in the following figure, then select your local Python interpreter as the base.
2. Restart the command line session, enter the virtual environment, use `pip` to download the related dependency packages in the back-end directory, and then run the flask (similar to the previous approach, not repeat again).

### Front-end

The front end part of the project is built on the top of Vue framework. Before using it, please make sure that `node.js` and `npm` have been installed on the your machine.

```shell
$ node -v # Check whether the node.js is installed.
$ npm -v # Check whether the npm is installed.
$ npm install npm@6.14.10 -g # Be sure to update npm to a stable version, otherwise it will fail.
$ cd front-end # Enter the front-end directory.
$ npm install # Authomatically download the packages of related dependencies according to package.json.
$ npm run serve # Run front-end program. Be sure to run this command in the front-end directory and keep back-end running (open another terminal to type commands)!
```

### Something should be noted while setting up the project

- If you find red lines under app module of back-end Python code, you need to `mark as sources root` for back-end directory in PyCharm. It will adds the back-end directory to the `PYTHONPATH` environment variables，`PYTHONPATH` holds Python's default search path while importing modules, which allows Python to find app module.

- If the network timeout occurs while downloading dependencies using `npm`.
  ```shell
  $ npm install -g cnpm --registry=http://registry.npm.taobao.org # Replace the original download source by the Taobao mirror source in China.
  $ npm config get registry # Display the current mirror source.
  ```
  
- When Vue prompts that it must conform to the hump name: add the setting below to **vue.config.js**.
  ```
  lintOnSave: false
  ```
  
- If the back-end reports an error while signing in：module 'jwt' has no attribute 'encode': the system installed the wrong dependency. The project should use PyJWT, whereas the default one is JWT. As a result, you need to manually uninstall and install.
  ```shell
  $ pip uninstall PyJWT
  $ pip uninstall JWT
  $ pip install PyJWT
  ```
  
- If Vue is not defined in main.js: The system is named differently because main.js comes from two different project creations. The unified specification here is App.
  
- How to call the NetEase Cloud API?
  ```shell
  # First of all, create a new local folder and install the NetEase Cloud API.
  $ git clone https://github.com/Binaryify/NeteaseCloudMusicApi.git # Download the NetEase Cloud API.
  $ npm install # Install the related dependency packages of the NetEase cloud API.
  $ node app.js # Run the server, be careful not to run this command in Flask virtual environment.
  ```
  
- Further Instructions for Music Recognition

  Please call the recognizeAudio(path) method in app.MusicRecognizeModel.utils, if there is a recognize result, then return [music_name, match_count]. See test.py for more details.

- Extra dependencies for music recording:

  ```shell
  npm i js-audio-recorder
  ```
  
- Data visualisation:

  ```shell
  npm install echarts --save
  ```

## Documentation

The documents are in the `documentation` folder under the root directory, there are three documents in the PDF format now:

* User document: customer-focus. It introduces how to use our size step by step
* System document: developer-oriented. It gives the technical implementation details for peers to further develop and maintain this project.
* Reflection: Team members' reflections on the project.
