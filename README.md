## SYNOPSIS

```
$ tinderbox.py --help
tinderbox: a Python script to drive the binary package compilation process.

Usage:
  tinderbox [-h|--help] [-v|--version] <command>

Commands:
  tinderbox clean_targets   clean targets directory.
  tinderbox create_targets  create targets directory.
  tinderbox prepare         compile base packages for all targets.
  tinderbox compile         compile system and world packages for all targets.
  tinderbox all             all of the above.

Options:
    -h,  --help        display help.
    -v,  --version     display version.
```

## REQUIREMENTS
* docopt
* pyyaml

## CREDITS
adjust OS team <<platform.os@adjust.com>>

## LICENSE
Creative Commons Zero v1.0 Universal
