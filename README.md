# TOC Project 2019

A Facebook messenger bot based on a finite state machine

## Setup

### Prerequisite
* Python 3
* Facebook Page and App
* HTTPS Server

#### Install Dependency
```sh
pip3 install -r requirements.txt
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)

#### Secret Data

`VERIFY_TOKEN` and `ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

**`ngrok` would be used in the following instruction**

```sh
./ngrok http 5000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

## Finite State Machine
![fsm](./fsm.png)

## Usage
The initial state is set to `user`.


* **user**
	* Input : "login"
		* go to state **login** and ask for the account
	* Input : "register"
		* go to state **register** and let user creat a new account

* **login**
	* user input his/her account 
		* `if account exist` : go to state **accountOK**
		* `else` : go to state **accountFail** and reply "wrong account!"
			       then back to state **login**


## Reference
[TOC-Project-2017](https://github.com/Lee-W/TOC-Project-2017) ❤️ [@Lee-W](https://github.com/Lee-W)
