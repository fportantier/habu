# How to contribute

I'm really glad you're reading this, because we need volunteer developers to help this project come to success!

# Non-standard python modules

When you need to use external modules, please, check this:

1. If the module is currently a habu dependency, it's ok, use it.
2. If habu currently uses a similar module, try to use that.
3. If you need to generate a new dependency, please, ask before continue with your development

## Testing

Please, test your new additions before make a pull request.

If you're code inserts new errors, you will be punished really hard (not, I'm joking, but please, test before pull request)

## Readme generation

The readme is generated with the script "readme_generate" on the project root. 

For the generation, the script executes each command with the "--help" parameter, so, if you created a new command, please, add a help!

Also, if any command fails, an error is printed and the README.rst file is not generated.

## Write code!

No more words, simply code and ask for help if you're in doubt! Thanks for contributing!
