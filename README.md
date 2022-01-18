# Comics publisher

Script for posting [xkcd comics](https://xkcd.com) to vk group.  
Each time the script is run, a random comic will be placed in the specified group.  

### How to install

Python3 should be installed.  
Then type in the terminal:

    pip3 install -r requirements.txt

After that, create an .env file in the root of the project.  
Set up environment variables:  

    VK_ACCESS_TOKEN={Your vk access token}
    VK_GROUP_ID={Group for posting picture}
    VK_API_VERSION={Current version is 5.131}

You can get vk access token via implicit flow. [Read more here](https://vk.com/dev/implicit_flow_user).

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).