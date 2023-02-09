# photoshare-backend

### Steps To Setup
1. Clone the project like so:
  ```bash
  git clone https://github.com/likhity/photoshare-backend.git
  ```

2. `cd` into the newly created folder **photoshare-backend**.
  ```bash
  cd photoshare-backend/
  ```

3. Start a python virtual environment using Python 3.10 or later.
  ```bash
  python3 -m venv venv
  ```
  This creates a virtual environment that is local to only this project. So all packages that you install in the future using `pip` will only be installed locally for this project inside the `venv/` folder (whereas normally if you didn't do this virtual environment stuff, everytime you install packages, `pip` will install them globally for your entire system).

4. Activate the virtual environment by running:
  ```bash
  source venv/Scripts/activate
  ```
  You must do this step every time you start working on this project again.
  
5. Install the necessary packages using `pip` (python's package manager, similar to `npm` for javascript).
  ```bash
  pip install flask
  pip install python-dotenv
  ```
^ This list will probably grow as the project progresses.

6. Run `flask run` to start the server. It will start running on port 5000.
  ```bash
  flask run
  ```

As Step 4 says, everytime you start working on this project again, always first activate the virtual environment by running:
```bash
source venv/Scripts/activate
```