# BAKSpider

BAKSpider is an easy-to-use python script that spiders a target for backup files left on the server.

Below is an screenshot taken when BAKSpider is used on a live production website (URL removed for security):

<img align="center" src="/img/demo.png?raw=true" alt="demo image">


## Getting Started

Simply clone the git repository to your computer and run bakspider.py with your arguments.

### Prerequisites

BAKSpider requires Python 3.X which can be downloaded from:

```
https://www.python.org/downloads/
```

## Before You Start

Please read the below information to ensure you are using the features of BAKSpider correctly.

### Limitations:

BAKSpider only works on websites that show the filename and extension in the URL. It is unusable on websites that implement mod_rewrite as it is unable to find the original file to check for backups.

#### Valid URL Format:

* https://www.example.com/article.php?id=123

#### Invalid URL Format:

* https://www.example.com/article/123

### Wordlists

There are 3 wordlists provided in the repository, however you can use your own wordlists if you prefer. The ones provided are:

**dic/common-extensions.txt:**

* This wordlist contains a small list of common backup file extensions, these extensions are appended directly to the filepath url allowing you to create custom suffixs for the files.

**dic/whitelist-extensions.txt:**

* This wordlist contains the whitelisted file extensions that will be checked for backups, by default this includes the most common web extensions. This prevents the spider from checking for backup files for un-needed extensions (e.g. pdf, zip)

**dic/dirs.txt:**

* Although this wordlist is not used by default, it is provided in the repository as it often increases the chance for backup discovery. At the beginning of the scan, BAKSpider will check the target for these directories; for every file that is later checked for backups, it checks in each of these discovered directories. Depending on the amount of discovered directories, this can greatly increase the time it takes for the scan to finish.

## Usage

BAKSpider has been created to be simple yet powerful. The script usage is fairly self-explanatory and can be seen below:

```
optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     File containing additional directories to check for
                        backups, this option can increase scan time
                        dramatically.
  -b BAKEXT, --bakext BAKEXT
                        File containing backup extensions to search for.
                        (Default: dic/common-extensions.txt)
  -e EXT, --ext EXT     Whitelist extensions, only URLs with this extension
                        will be checked for backups.
  -t THREAD_COUNT       Maximum number of concurrent threads (Default: 8)
  --debug               Enables verbose output, useful for debugging.

required arguments:
  -u URL, --url URL     The Target URL (e.g. http://www.example.com/)
```

## Contributors

* **Matthew Croston** - *Original Developer* - [mt-code](https://github.com/mt-code) - [https://mtcode.co.uk/](https://mtcode.co.uk/)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details
