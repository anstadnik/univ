import subprocess
import sys

class Output:
    """Class for displaying the result to the user"""
    def __init__(self, text):
        self.text = text

    def output(self):
        bashCommand = "echo \"{}\" | lolcat-c".format(self.text)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        p1 = subprocess.Popen(["echo", self.text], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["lolcat-c"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output, err = p2.communicate()
        # print(str(output).decode('utf-8'))
        sys.stdout.buffer.write(output)
