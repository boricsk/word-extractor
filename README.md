Usage: worext.py [OPTIONS]

  Word Extractor V 1.0.0

Options:
  -u, --url TEXT        URL of webpage to extract from\n
  -l, --length INTEGER  Minimum lenght of word (Default 0=no limit)
  -o, --outfile TEXT    Write outpot to file
  -c, --comments        Extract comments line from target
  --help                Show this message and exit.

  Examples:
  python3 --url http://target                                       Extract top words from target. You will see top ten only, if you want more need to save the output
  python3 --url http://target --outfile words.txt                   Save output to file
  python3 --url http://target --comments                            Show commented lines of target
  python3 --url http://target --comments --outfile comments.txt     Save comments output to file
