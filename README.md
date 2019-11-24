# Quick-Pass
Easy to use, local only, password manager

## How to use
Requires the Crypto, sqlite3, and clipboard python3 packages. Install them with pip3 if you don't already have them. Specify the database file as the positional command, use the -a command to add a record. Your password must not end with the `|` character (That's the one above the `\` character). If you try to add a record with a duplicate site and username, the old record will be replaced with the newly specified password. Use the -c command to automatically copy the password to the clipboard (If the clipboard package is installed), otherwise it will be printed to standard output (Bad for security if anyone else is looking at your screen!).

See printout of help message below:

```usage: Quick-Pass.py [-h] [-a] [-c] [-u U] [-s S] [-z] [filepath]

positional arguments:
  filepath    Path to your passwords file. If not supplied will
              create/overwrite Data.db

optional arguments:
  -h, --help  show this help message and exit
  -a          Add or update password
  -c          Copy password to clipboard. Requires the clipboard module to be
              installed
  -u U        Specify the username for the specific site so you will not be
              asked if more than one record is found for the site. Ignored if
              there is only one record listed for the site.
  -s S        Specify the site to retrieve the password from so you will not
              be asked
  -z          List known site and username combinations
```

### Is it cryptographically secure?
Will it keep your family away from your passwords? Yes.

Will it keep the NSA out of your accounts? Absolutely not.
