# chainlitQAFlow
You can use this chainlit interface to  chat with your uploaded files in Pinecone

## Installation

1- Clone this git repository by running the command: 
```shell
  git clone https://github.com/etienne113/chainlitQAFlow.git
```
  
2- Open the cloned repository in a IDE of your choice, we recommand PyCharm

  Click of this link to download the PyCharm IDE: https://www.jetbrains.com/pycharm/download/?section=windows#section=windows
  
3- Open the terminal in Pycharm: 

  ![image](https://github.com/etienne113/chainlitUploadToPinecone/assets/96786848/7f313354-27f0-4f6e-934c-51815132ea60)
  
4- Download and install  Python (if not already installed) : visit the website https://www.python.org/downloads/

5- run the command:
  ```shell
   python -m venv venv
  ```
And then:
  * On Windows:
    ```shell
      . venv/Scripts/activate
    ```
  * On MacOS:
    ```shell
      . venv/bin/activate
    ```  
6- Now install the required dependencies by running the command:
```shell
  pip install -r requirements.txt
```
7- Create a .env file from the .env.example file by running the command:
  ```shell
    cp .env.example .env
  ```
and then fill the empty fields.

8- Now you can run your programm by running the command:
```shell
    . venv/bin/activate
```
and then: 
```shell
    chainlit run chainlitQAFlow.py -w
```

  Thank you for your visit! 
