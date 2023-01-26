# pnd

A simple cli password manager in pure python

# Installation

Run the interactive installer

```shell
git clone --depth 1 https://github.com/tomginsberg/pnd.git ~/.pnd
~/.pnd/install
```

# Usage

* `sudo pnd add` an interactive tool to add/generate new passwords

* `sudo pnd <name of password>` prints the password with a matching name to the console.

* `sudo pnd ls` prints of name of all saved passwords.

* `sudo pnd rm` an interactive tool to remove passwords.

* `sudo pnd encrypt` create an encrypted file named `~/.pnd/vault` to store your passwords safely using Fernet
  encryption with a PBKDF2 derived key. This file is safe to back up to the cloud (e.g. google-drive or github)

* `sudo pnd decrypt` read the `~/.pnd/vault` into a `json` format that can replace your existing `pnd` file in
  case of data loss.

* `pnd generate <length>` generate a secure password with a given length.
  Note that `pnd add` also gives you the option to automatically generate passwords.

## Set-up copy-to-clipboard

Mac users can place the following function into their `.bashrc/.zshrc` file

   ```bash
   pndc (){
     sudo pnd $1 | pbcopy
   }
   ```

Linux users should replace `pbcopy` with `xclip`
This allows passwords to be directly copied to a users clipboard via `pndc <name of password>`

### Even more power !

To get the most out of `pnd` install fzf and add the following alias to your `.bashrc/.zshrc` file

```bash
alias pnds="sudo pnd ls | fzf | xargs sudo pnd | pbcopy"
```

Now `pnds` launches an interactive fuzzy search over all passwords and copies the selected one to your clipboard.

### (Recommended) Install [sudo-touchid](https://github.com/artginzburg/sudo-touchid)

Use `sudo-touchid` to replace traditional sudo authentication with the Mac touch-id sensor.

Installation is simple with homebrew

   ```shell
   brew install artginzburg/tap/sudo-touchid
   sudo brew services start sudo-touchid
   ```

# Uninstall
    
  ```shell  
  sudo rm /usr/local/bin/pnd
  sudo rm -rf ~/.pnd
  ```