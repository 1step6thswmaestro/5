# coding=utf-8


class LdenParser:
    """
    lden의 기능에 맡게 help와 커맨드 파싱을 하는 클래스이다.
    lden 프로그램 전체의 help가 있고 커맨드 별로 help가 있다.
    """

    def __init__(self, argv_list):
        self.argv = argv_list
        self.result = []
        self.commands = ["all", "notify"]
        self.command_help = [
                "all [<options>]\n",
                "notify <expression> [<options>]\n"
        ]
        self.command_options_help = [
            [
                """    -a, --address <ip address>  set server ip address to show data
                                (default: 192.168.225.1)\n""",
                """    -p, --port <port number>    set port
                                (default: 9200)\n"""
            ],
            [
                """    -t, --time <timeout>                set timeout
                                        (default: infinity)\n""",
                """    -s, --script <shell script>         execute user-defined shell script\n"""
            ]
        ]
        self.command_options = [
            {
                "-a": ["-a", "a", "address", 0],
                "--address": ["-a", "a", "address", 0],
                "address": ["-a", "a", "address", 0],
                "-p": ["-p", "p", "port", 1],
                "--port": ["-p", "p", "port", 1],
                "port": ["-p", "p", "port", 1]
            },
            {
                "-t": ["-t", "t", "time", 1],
                "--time": ["-t", "t", "time", 1],
                "time": ["-t", "t", "time", 1],
                "-s": ["-s", "s", "script", 2],
                "--script": ["-s", "s", "script", 2],
                "script": ["-s", "s", "script", 2]
            }
        ]

        if len(self.argv) == 1 \
                or self.argv[1] == "help" \
                or self.argv[1] == "--help" \
                or self.argv[1] == "-h":
            self.print_help()
        elif self.argv[1] == "all":
            self.result = [0,
                           {
                               "address": None,
                               "port": None
                           }
                           ]
            self.do_command(0)
        elif self.argv[1] == "notify":
            self.result = [1,
                           {
                               "expression": None,
                               "time": None,
                               "script": None
                           }
                           ]
            self.do_command(1)
        else:
            print "lden: \'" + self.argv[1] + "\' is not a lden-command. See \'lden --help\'"
            exit()

    def print_help(self):
        print """
 usage: lden [help, -h, --help] COMMAND [ARGS]
 (This program must be executed with "permission of superuser")

 The most commonly used lden commands are:
   all      Trace all events and visualize their data on Kibana
   notify   Trace events user selected according to condition expression,
            notify when condition is set and execute script user defined

 See 'lden COMMAND --help' for more information on a specific command.
"""
        exit()

    def do_command(self, command):
        if len(self.argv) == 2:
            if command == 0:
                return
            else:
                self.print_command_help(command)
        elif self.argv[2] == "help" \
                or self.argv[2] == "help" \
                or self.argv[2] == "--help" \
                or self.argv[2] == "-h":
            self.print_command_help(command)
        else:
            if command == 1:
                self.result[1]["expression"] = self.argv[2]
            for i in range(2, len(self.argv)):
                if command == 0 and (i & 1) == 1:
                    continue
                if command == 1 and (i & 1) == 0:
                    continue
                if self.argv[i] in self.command_options[command]:
                    self.get_value(command, i, self.command_options[command][self.argv[i]])
                else:
                    if self.argv[i][:2] == "--":
                        chosen_option = "option \'" + self.argv[i][2:] + "\'"
                    elif self.argv[i][:1] == "-":
                        chosen_option = "switch \'" + self.argv[i][1:] + "\'"
                    else:
                        chosen_option = "option \'" + self.argv[i] + "\'"
                    print "  Error: " + "unknown " + chosen_option
                    self.print_command_help(command)

    def print_command_help(self, command, option=None):
        print "\n usage: lden " + self.command_help[command]
        if option is None:
            for i in self.command_options_help[command]:
                print i
        else:
            print self.command_options_help[command][option]

        if command == 1:
            print " See README.md to know how to query expression exactly\n"
        exit()

    def get_value(self, command, index, check_list):
        if len(self.argv) <= index + 1:
            if self.argv[index] == check_list[0]:
                chosen_option = "switch \'" + check_list[1] + "\'"
            else:
                chosen_option = "option \'" + check_list[2] + "\'"
            print "  Error: " + chosen_option + " requires a value"
            self.print_command_help(command, check_list[3])
        else:
            self.result[1][check_list[2]] = self.argv[index + 1]

