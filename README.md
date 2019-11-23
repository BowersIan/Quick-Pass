# Quick-Pass
Easy to use, local only, password manager

## How to use
Requires the Crypto, sqlite3, and clipboard python3 packages. Install them with pip3 if you don't already have them. Specify the database file as the positional command, use the -a command to add a record. Your password must not end with the `|` character (That's the one above the `\` character). If you try to add a record with a duplicate site and username, the old record will be replaced with the newly specified password. Use the -c command to automatically copy the password to the clipboard, otherwise it will be printed to standard output (Bad for security if anyone else is looking at your screen!). Command line options to automatically specify the site name and username coming when I can be bothered.

### Is it cryptographically secure?
Will it keep your family away from your passwords? Yes.

Will it keep the NSA out of your accounts? Probably not.
