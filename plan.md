Stage 1
The first functions to implement are the ones that deal with user authentication. It is the basis for many of the other functions since a token is required to identify the user. This shouldn’t take too long as functionally, they are very basic. We will start by working together to get this part of the implementation done in the quickest possible time.

Stage 2
Next, getting a basic implementation of the channels will allow us to get going with the message functions and the user profile functions. We can then split into 2 groups, one working on finishing this stage and the other can start work on stage 3 or 4.

Stage 3
We expect the message functions to take the longest since it contains the most number of functions as well as containing many ways for exceptions to be raised. 
We also expect the channel functions to take quite a while since it also has a reasonable amount of functions to implement. It also deals quite heavily with user permissions so making sure only users who have enough authorisation will have access to certain functions.

Stage 4
The user profile functions also shouldn’t take too long since it is mostly just verification that the information given is valid and then sending it to the server to save. All the functions only rely on stage 1 to be completed so this stage can be completed alongside stages 2 or 3.

Stage 5
The standup functions looks pretty difficult and requires for the channels and messages functions to be implemented. As a result, these functions will probably be implemented last and should be done by at least 2-3 members to ensure that the function is implemented correctly.

Once each individual section is done, rigorous testing should be undertaken so that when next functions are implemented, we will know that any error occuring will be from these functions and not from the previously implemented functions.

Testing that all the functions work and interact together as intended is also going to take a decent portion of our time. We need to make sure that even if a function looks like it works, it hasn’t created any problems in other functions. 







Stage 1: User Authentication:  
auth_login  
auth_logout  
auth_register  
auth_passwordreset_request  
auth_passwordreset_reset  
Estimated time: 3 days  

Stage 2: Channel Implementation  
channel_join  
channel_invite  
channel_leave  
channels_create  
channel_messages  

channel_details  
channel_addowner  
channel_removeowner  
channels_list  
Estimated time: 6 days

Stage 3: Message Functions  
message_sendlater  
message_send  
message_remove  
message_edit  
message_react  
message_unreact  
message_pin  
Message_unpin  
search  
Estimated time: 6 days

Stage 4: User profile functions  
user_profile  
user_profile_setname  
user_profile_setmail  
user_profile_sethandle  
User_profile_uploadphoto  
Estimated time: 3 days  

Stage 5: Standup functions  
standup_start  
standup_send  
Estimated time: 2 days

