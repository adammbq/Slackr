Auth_login  
The token provided changes each time the user logs in as to increase security  
User isn’t already logged in  

auth_logout  
Assume the user is already logged in  

Auth_register  
Password does not only consist of whitespace  

auth_passwordreset_request  
Email is sent in a reasonable time since the request was made  

Channel_invite  
Invitations expire after a certain time  

channel_details  
An existing channel must have a channel owner  

channel_messages  
Assume the messages are in order  

channel_leave  
When everyone has left a channel, that channel is deleted  
A channel owner can only leave once he transfers ownership  

Channel_join  
Any user is able to join any amount of channels  
channel_addowner  


channel_removeowner  
There will always be at least 1 owner  

Channels_list  
That if no channels exist, returns an empty list  

Channels_listall  
That if no channels exist, returns an empty list  

channels_create  
That two channels can have the same name but different channel id  
That a channel name cannot be left blank 

Message_sendlater  
That the date inputted isn't in the past  

message_send  
Messages appear on the channel very shortly after they were sent  
Every message that is going to be sent contains only valid unicode characters  

message_remove  
If a message is pinned then removed, the pinned message is also removed   

message_react  
Messages can be reacted more than once  

Message_pin  
That message isn’t already pinned 

message_unpin  
That message is pinned  

user_profile  
That if the profile doesn’t exist, nothing is returned  


User_profile_setname  
That valid string is entered  
  
user_profile_uploadphoto  
When uploading a profile picture, the x and y end will not be very large  
Profile photos do not show anything explicit or sensitive information  

standup_send  
That a standup period is currently active  

search  
That if no messages match the query, nothing is returned  
There is a max length on the query string  

Admin_userpermission_change  
That the existing user permission doesn’t match permission level to be changed to  
That the user has sufficient permissions to perform the command  


Whenever ‘token’ is passed as a parameter, this token is valid and represents a user
