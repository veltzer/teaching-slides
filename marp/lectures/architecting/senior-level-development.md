---
tags:
- concepts:architecture
- practices:leadership
- practices:code-quality
level: advanced
category: architecture
audience:
- audiences:developers
- audiences:architects
- audiences:managers

---
# Correct Development
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Script everything

![title](svg/lectures/architecting/senior-level-development/title.svg)

---

## Script everything

* This means even things you do once every year
* The practice will make you better at it
* Use templating engines to tie systems together.
* Use secrets storage solutions to not put secrets in your code.

---
## Error Handling
* The sad Java checked exceptions story
* Never catch errors you don't understand
* Your real enemy are permanent bugs

---
## Writing code
* Reward developers who remove code more than those who add code
* Avoid "it's working so don't touch it" attitude
* Allow developers to rebuild everything, fast!
* Reward developers who manage to redesign your code - they are the true heroes.
* Above a certain size agile works, rewriting doesn't.
* Keep it simple, Stupid! (your codes architecture that is).
* Have good taste.
* Lint with tons of tools. Don't allow any unlinted code in.

---
## Documentation
* Use simple text or MD drawings to document your systems, avoid GUI tools.
* Use git to maintain the docs.
* Document the hard parts in your code, don't document the simple ones
* Must be synced to your code.
* Must be fast and easy to write otherwise it won't happen

---
## Debugging
* [do not use a debugger](https://lemire.me/blog/2016/06/21/i-do-not-use-a-debugger/)
* Heisenbugs.
* Alternatives to debugging
    * reading your code
    * infrastructure for visibility
    * configurable logging
* Debugging cycles should be fast (see building your code fast - see above).

---
## Do not use user interfaces
* Not reproducible
* Not scriptable
* Always changing
* GUI pull you to manual instead of automatic work
* Don't let fancy GUI tempt you to the dark side, the fancier the worst it is
* Disable GUI whenever you can

---
## Do not write code which is not your main business
* You are not good at it
* You don't want to maintain it
* Get open source alternatives or any other alternative
* Anything which is not your main business should be open sourced

---
## Your development environment
* Keep yourself agile regarding your tools
* Use as few tools as possible
* Be sure about why you use all of these tools
* Drop tools you no longer need to simplify your environment.
* Allow developers to enter password or MFA easily and keep security out of their way
* Dump as much as possible on automated cloud services
* Keep it simple, Stupid! (your development environment, that is)

---
## Configuring software that you use:
* Why keeping the default configuration is the best
* If you can't use the default, change the configuration as little as possible.
* Make sure your entire team uses the same configuration
* Keep it simple, Stupid! (your configuration that is)

---
## Allowing to run your software in many ways
* Allow to run it as library
* Allow to run as command line tool
* Allow auto-completion on the command line
* Allow to override any option with environment variables.
* Allow configuration files: per user, per system
* Always follow convention over configuration

---
## Separate systems that should be separate
* Prefer multi-process to multi-thread
* Micro-services
* Different code repos
* Everything in computing is about separation.

---
## Using source control correctly
* Don't use feature branches
* Correct tagging.

---
## Zero aural traditions
* No special URLs, users, passwords, tools, that people need to gather: everything in one clear page.
* The test of building and running your code from git
* Script bootstrapping your code
* Script installing all dependencies
* Script everything!

---
## Proper logging
* Every tool you run should be run quietly, and if the tool does not know how to be quiet, teach it.
* Long log files in the command line or from CI/CD are from the devil.
* Make it easy to see more info when you need to.
* Warnings should not be shown either because every warning should be treated as error.

---
## Test, test, test
* Test especially the things which failed in the past
* Developers should write tests, not QA people. Fire them!
* Reward new tests which pass, never settle for failing tests.

---
## Microservices
* You are doing it wrong
* The most important part of Micro-services is that they are **Independently Deployable** and *Independently Testable**.

---
## Stop using MS-Windows!
* Why Linux is better for developers and facilitates all of the above
* Why using windows is making your developers bad developers.

---
## Philosophy is more important than practical knowledge
* Don't remember all the details, you'll never remember them anyway.
* Being able to explain why you are using every tool you are using
* When studying tools, learn their philosophy
* When using each tool check if you are using it according to it's philosophy
* Avoid abusing tools - meaning stop using them against their philosophy or not in line with it.

---
## When to use outside help or consultants
* When you are afraid to do it yourself
* When you are using a new technology and you have no in-house people

---
## When not to use outside help or consultants
* When it has to do with your core business
* When you should have people that know this shit

---
## How to use your browser correctly
* Never use too many tabs
* Always use bookmarks to your favorite places, this is a tricky art.

---
## How to use docker correctly
* Always use one docker image! that's the whole point of docker!
* Don't abuse the technology.

[comment:] Not to use a lot of bookmarks
[comment:] not to use a lot of tabs
[comment:] not to use branches in git but work with trunk.
[comment:] how to correctly use microservices.
[comment:] how to simply use git.
