# photoshare-backend

## Steps To Setup
#### 1. Clone the project like so:
  ```bash
  git clone https://github.com/likhity/photoshare-backend.git
  ```

#### 2. `cd` into the newly created folder **photoshare-backend**.
  ```bash
  cd photoshare-backend/
  ```

#### 3. Start a python virtual environment using Python 3.10 or later.
  Download and install [Python](https://www.python.org/) in your system. After that, run this:
  ```bash
  python3 -m venv venv
  ```
  This creates a virtual environment that is local to only this project. So all packages that you install in the future using `pip` will only be installed locally for this project inside the `venv/` folder (whereas normally if you didn't do this virtual environment stuff, everytime you install packages, `pip` will install them globally for your entire system).

#### 4. Activate the virtual environment by running:
  ```bash
  source venv/Scripts/activate
  ```
  You must do this step every time you start working on this project again.
  
#### 5. Install every package in package.txt using `pip` (python's package manager, similar to `npm` for javascript).
  ```bash
  pip install flask
  pip install python-dotenv
  pip install psycopg2-binary
  ```
^ This list will probably grow as the project progresses. To make this easier, I created a bash script (packages.sh) that installs all the necessary packages in one go. Just run `bash packages.sh`.

**IMPORTANT**: Everytime you install a new package for this project, add it to the list of packages in packages.sh.

#### 6. Run `flask run` to start the server. It will start running on port 5000.
  ```bash
  flask run
  ```

As Step 4 says, everytime you start working on this project again, always first activate the virtual environment by running:
```bash
source venv/Scripts/activate
```

## Test The Project
So you made some changes to the code and want to test it. Currently, we don't have a front-end setup to test if the backend is working correctly.

You can use something like `curl` or `nc` to test the routes, but an easier way to do it is by using a tool called **Postman**.

Download and install the [**Postman**](https://www.postman.com/downloads/) desktop app and launch.

You'll see that this desktop app makes it really easy to specify the request method, the url, params, headers, body and everything and send requests and see the response in a nice, easy to understand format.

Before you start testing using Postman, first make sure the virtual environment is activated and that you actually started the server by running `flask run` in this project directory.

Here is an example of a test using Postman:
![Postman Test](https://i.imgur.com/TgcWx89.png)

You can also see that flask prints out a short summary of each request that is made to server in the terminal:
![Flask screenshot](https://i.imgur.com/Pw0cHcr.png)