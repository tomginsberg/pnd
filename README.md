# pnd

A simple cli password manager in pure python

[Usage](#-Usage)
[Installation](#-Installation)

# Usage

* `sudo pnd add` an interactive tool to add/generate new passwords
* `sudo pnd <name of password>` prints the password with a matching name to the console.
* `sudo pnd ls` prints of name of all saved passwords.
    * For [fzf](https://github.com/junegunn/fzf) users `sudo pnd ls | fzf` creates a simple fuzzy searcher over your
      saved passwords.
* `sudo pnd rm` an interactive tool to remove passwords.
* `sudo pnd encrypt` create an encrypted file named `/private/pass/vault` to store you passwords safely using Fernet
  encryption with a PBKDF2 derived key. This file is safe to back up to the cloud (e.g. google-drive or github)
* `sudo pnd decrypt` read the `/private/pass/vault` into a `json` format that can replace your existing `pnd` file in
  case of data loss.
* `pnd generate <length>` generate a secure password with a given length.
  Note that `pnd add` also gives you the option to automatically generate passwords.

## (For Mac Users) Set-up copy-to-clipboard

Mac users can place the following function into their `.bashrc/.zshrc` file

   ```bash
   pndc (){
     sudo pnd $1 | pbcopy
   }
   ```

This allows passwords to be directly copied to a users clipboard via `pndc <name of password>`

### Even more power !

To get the most out of `pnd` install fzf and add the following alias to your `.bashrc/.zshrc` file

```bash
alias pns="sudo pnd ls | fzf | xargs sudo pnd | pbcopy"
```

Now `pns` launches an interactive fuzzy search over all passwords and copies the selected one to your clipboard.

### (Recommended) Install [sudo-touchid](https://github.com/artginzburg/sudo-touchid)

Use `sudo-touchid` to replace traditional sudo authentication with the Mac touch-id sensor.

Installation is simple with homebrew

   ```shell
   brew install artginzburg/tap/sudo-touchid
   sudo brew services start sudo-touchid
   ```

# Installation

1. Install the `pnd` script and place it in a directory in your system PATH
    ```bash
    cd /usr/local/bin
    sudo wget https://raw.githubusercontent.com/tomginsberg/pnd/main/pnd
    # Give pnd admin rights
    chmod 700 pnd
    # install (optional) dependencies 
    pip install cryptography
    ```
   *Note: if the command `python3` is not available on your system update the first line of `/usr/bin/pnd` to the python
   executable of your choice (e.g. `#!<python 3 executable>`).*
2. Create a protected file to store your passwords
    ```bash
    cd /private
    sudo mkdir pass
    cd pass 
    sudo touch pnd
    sudo chmod 700 pnd
    ```