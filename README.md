# Password Manager PRO - Commandline interface

Python based command line interface for [Password Manager Pro](https://www.manageengine.com/products/passwordmanagerpro/help/restapi.html). This provides a command line interface which uses the REST API to provide a command line to:

 - Read individual passwords
 - Create temporary files with a set of passwords


# Setup

Python and pip must be installed on the machine you wish to use.

 1. Create a API user in [Password Manager Pro](https://www.manageengine.com/products/passwordmanagerpro/help/restapi.html)
 2. Set the PASSMANCLI_APIKEY enviroment variable based on the user
 3. Set the PASSMANCLI_URL enviroment variable based on your install of password manager pro
 4. Install utility (pip3 install PasswordManPro_CLI
 
# Usage

## Access single password

```
PasswordManPro_CLI get **RESOURSE_NAME** **PASSWORD_NAME**
```

## Generate password file

TODO
