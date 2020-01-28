# Quick-Pass
Easy to use, local only, password manager

## How to use
Requires the Crypto, sqlite3, and clipboard python3 packages. Install them with pip3 if you don't already have them. Specify the database file as the positional command, use the `-a` command to add a record. Your password must not end with the `|` character (That's the one on the `\` key). If you try to add a record with a duplicate site and username, the old record will be replaced with the newly specified password. Use the `-c` command to automatically copy the password to the clipboard (If the clipboard package is installed), otherwise it will be printed to standard output (Bad for security if anyone else is looking at your screen!).

See printout of help message below:

```
usage: quick-pass [-h] [-a] [-c] [--no-copy] [-u U] [-s S] [-p P] [-z] [-r]
                  [filepath]

positional arguments:
  filepath    Path to your passwords file. If not supplied will
              create/overwrite ./Data.db

optional arguments:
  -h, --help  show this help message and exit
  -a          Add or update password
  -c          Copy password to clipboard. Requires the clipboard module to be
              installed; if not installed, this argument is ignored
  --no-copy   Overides -c and prints password to standard out
  -u U        Specify the username for the specific site so you will not be
              asked if more than one record is found for the site. Ignored if
              there is only one record listed for the site.
  -s S        Specify the site to retrieve the password from so you will not
              be asked
  -p P        Specify the password to manage. If not specified, will be asked
              for. Not recommended to use as password will be stored in
              command history and visible to anyone watching.
  -z, -l      List known site and username combinations
  -r          Removes selected site and usernaname combination
  --upgrade   Upgrades your database for a newer version of Quick-Pass

```

### Is it cryptographically secure?
Will it keep your family away from your passwords? Yes.

Will it keep the NSA out of your accounts? Absolutely not.

Furthermore, I do not make nor imply any guarantee, warranty, or any such idea that this program works, works as intended, is secure, or any other such notion.

### Recommendations
Alias the script with the absolute path of your database file so that you don't have to worry about specifying each run.

Backup the database file for when you accidentally delete it or your hard drive fails.
