SE Principles

<b>General</b>

- --All helper functions are put into a helper file. It allows the function to follow the Single Responsibility and DRY principles. It helped locate and fix error quicker based on the traceback on the Terminal since we knew exactly where the error was occurring
- --Switched from using &quot;sys.path.append(&#39;./server&#39;)&quot; to using absolute imports. This made it easier to identify where each module was coming from. It raised our Pylint score as one of the issues was Pylint was not able to import the modules due to not knowing where the files were located
- --Switched from using wildcard imports to explicitly stating which functions are being imported. This was recommended by Pylint as by using the wildcard import, it is unclear about which functions are going to be used and whether they come from the file the function is being called in or from the imported file
- --When Value/Access errors were being thrown, they were all within if/elif/else&quot;statements. This was changed to only use if statements because throwing an error would automatically terminate the program, making the elif/else statements redundant. This was also caught by Pylint
- --Added a docstring to every function to give a more detailed explanation of what the function does. Even though most were self-explanatory, it saves having to read the logic of the function to understand what it is doing and what it returns
- --Reordered the import statements so that importing standard libraries and modules written by other people were placed before the importing of our own functions to create less confusion about what we were importing
- --We used pre-made libraries to help abstract away and encapsulate the implementation of functions and save time since we didn&#39;t have to implement it. One such was the datetime library which made it really easy to process the unix timestamps passed in by the frontend and also send timestamps to the frontend. The &quot;threading&quot; library was also used for the standup functions as they are needed to keep the application running while a standup is active
- --Originally stored all message data within User and Channel data structures. Amended, creating a separate data structure for Messages storing message ID, user ID, channel ID, timestamps and all other message data. This lended to making our code more readable and easier to understand as originally the interactions of the messages within other structures made logic unclear. Hence, this lends to the KISS principle in basic SE Principles.
- --Separated functions into prefix subcategories; Channels, Messages, User, Auth. Made it easier for the group to collaborate as rather than all members working on one document, changes can be made to separate functions with less difficulty in terms of pushing and pulling and merge conflicts. Made it much easier to identify and fix issues in visual frontend testing stages as we knew exactly what was going wrong at any given point.
- --Similarly compiled all testing files into prefix categories so that coverage tests could be done with much less difficulty, testing each individual file.
- --Return values for functions that were supposed to return empty dictionaries were moved to function files rather than being done only in server.py. This made testing easier allowing for us to easily assert that each function has the correct return value.
- --Originally stored the perm_ids as magic numbers but changed to global variables for clarity.

<b>Auth funcs</b>

- --Helper functions were implemented for often used processes including repetitive actions such as check\_email, generate\_token, get\_user\_from\_id, etc. The implementation of these functions lended to the DRY principle, as these processes were repeated many times throughout the auth functions of development. Implementation of these functions drastically improved readability and also saved time during development.
- --Added comments and removed wildcard imports after pylinting
- --Moved all the numbers relating to the permission ids to variables which allowed us to track what permission ids are being checked. Also made it easier to read
- --Pylint score: 9.75

<b>Channel funcs</b>

- --During the development of channel funcs, it came to our attention that we would have to amend the way that we stored messages. Originally being stored within channel and being linked to users data structures, made coding functions related to messages very difficult to understand and overall logic messy. Hence, we decided to include a new data structure just for messages. This made implementing functions such as for the pinning and reacting of messages much easier and readable, as indicators within the  messages structure were made for pin and react status, as well as all other relevant message details. This decision also lended to making message functions much easier to implement than if we had stuck with the original data system.
- --Added docstrings, comments and removed wildcard imports, only importing used functions instead.

<b>Message funcs</b>

- --If the parameter given by the frontend is called &quot;message&quot; such as message/send or message/edit, the variable passed to the function that carries out the operation is now called &quot;message\_str&quot; instead of &quot;message&quot;. This is to reduce confusion where if we want to locate a specific message dictionary, the variable is also called &quot;message&quot;
- --Logic such as checking whether a user was in the channel the message was sent and retrieving the message was repeatedly used so they got moved to functions in the helper file to reduce long lines of repetition and help the calling function to better follow having a single responsibility
- --Added more comments in areas where the logic may not be very obvious

<b>User funcs</b>

- --Added docstrings, comments and removed wildcard imports, only importing used functions instead.