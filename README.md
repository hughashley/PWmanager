# COM430 software engineering term project.
# contains several known bugs:
  -upon first startup, database is created.  The first password recorded to the database is not recallable.
  
  -if a pin is incorrectly entered to recall the application must be completely closed to attempt to recall again
  
  -numeric zero pin will not work
  
  -each update will address the bugs with major versions adding new features.

# The purpose of program is to securely store complex, difficult to remember passwords with as little as a pin, it can manage multiple users and the passwords are hashed and stored with no reference to the account they belong to.  When storing a password you must create a pin.  the same pin can be used for all passwords but do not forget it, there is no way to retrieve the password without it.  When creating a new user, password is optional.  there is no way to retrieve it so keep this in mind.
