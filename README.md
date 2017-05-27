# check_defacement
Monitoring Web pages content 

A Web page, is any document that is part of a site on the Internet, usually in HTML format and with hypertext bindings that allow navigation for the remaining content of the site. The malicious and purposeful alteration of web pages content and consequent disfiguration of websites is a fairly used attack by hackers with different motivations, known as defacement. Defacement essentially violates two of the main properties of information security, namely integrity and authenticity.
For this reason, it has become a major concern for Internet security, ideally to ensure that the content of Web pages is integral and authentic, and in the event of a possible compromise, administrators will be prompted immediately.
This Nagios plugin monitors the content of the Web page passed by URL as an argument, in search of potentially hazardous words, returning the critical state if a detection is made. By default, a set of words are defined, which can optionally be ignored, or to them concatenated others according to the user's needs.

Mandatory arguments: The following argument must be specified when the module is executed:

-U or --url used to specify the URL that will be monitored.

Optional arguments The following arguments are optionally invoked, as user needs:

-V or --version used to query the module version.
-A or --author used to query the author's data.
-i or --ignore used to skip the list of dangerous words preinstalled.
-I or --Ignore used to specify one or more existing words in the preinstalled list to be ignored.
-K or --keyword used to specify the words to be searched in Web content.

Command-Line Execution example:

./check_defacement.py -U https://exchange.nagios.org/directory/Plugins/Security -K hacker,hacked
