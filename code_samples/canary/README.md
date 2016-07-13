Canary Coding Exercise
======================

Requirements
------------

The Canary product team has been hard at work coming up with new ideas. The latest one is a new bonus feature for all users - a URL shortener - and now they're handing it over to the engineering team to build it.

Here's how the shortener should work:

1. A user inputs a URL into a text field.

2. The system generates a shortened URL which, when visited, redirects to the original URL. So, for example if the user entered 'http://www.superlongdomain.com/plus/a/really/long/path?my=shortener' then a shortened URL could be 'http://cnry.to/zzsq1'.

3. Visiting 'http://cnry.to/zzsq1' redirects to 'http://www.superlongdomain.com/plus/a/really/long/path?my=shortener'.

4. There should be an admin page that allows an admin user to view all shortened URLs the system has generated.

Bonus!
------

**Get extra points!**
Everyone loves bonuses! While it's not necessary, the following items will help Canary to have a better understanding of your skills and allow us to find the right place in the company for you. Try to complete as many as possible (in no particular order)!

 - Canary is about programable interfaces! Provide an API to allow creating new shortened urls and retrieving information from existing ones.
 - Wow!! Our latest research shows that over a hundred thousand users should be *shortening* an average of 5 urls every day! How would you handle the load?
 - Provide an easy way to start the project to prove all criterias were met. It can be a script, vagrant image, etc. Use your creativity!
 - Don't you wish all apps were portable? *Dockerizing* apps is really interesting for us. ;)
 - have *git* ninja skills? having a commit history always come in handy for big projects like ours!
 - integrating with a CI server? Sure, why not!?


Instructions
------------

1. Using Django (or Flask / Rails / Sinatra), build a self-contained application that implements the above requirements. Feel free to use any additional third party libraries that you'd like.

2. Please provide a basic test suite for the required functionality.

3. Make any assumptions that you need to. This is an opportunity to showcase your skills, so if you want to, implement the shortener with any additional features you'd like to see.

4. Please include any instructions for getting your app up and running locally in a README in the project root directory.

5. Word! Elaborating on your design decisions is also a way to demonstrate your skills!

6. We are evaluating solutions based on the architecture and quality of the code. Show us just how beautiful, clean and pragmatic your code can be.


Now it's time to sit down with a cup of coffee, maybe put on some of your favorite music and most importantly, enjoy!
