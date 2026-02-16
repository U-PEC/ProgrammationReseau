# server/shell.py
import os
import socket
import subprocess

def execute_system_command(command, user_home):
    """
    Executes a command in a sandboxed environment for the user.
    """
    command = command.strip()
    if not command:
        return ""

    try:
        if command.startswith("cd "):
            target = command.split(" ", 1)[1]
            new_path = os.path.abspath(os.path.join(os.getcwd(), target))

            if not new_path.startswith(user_home):
                return "Error: Access denied (outside of your home directory)."
            
            os.chdir(new_path)
            rel_path = os.path.relpath(new_path, user_home)
            return f"Current directory: ~/{rel_path if rel_path != '.' else ''}"


        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return output.replace('', '')

    except Exception as e:
        return f"Error: {str(e)}".replace('', '')

def handle_session(chan, user_home):
    """
    Manages the interactive shell for a user.
    """
    # Change to the user's home directory at the start of the session
    os.chdir(user_home)

    chan.send(f"--- SSH Server (User: {os.path.basename(user_home)}) ---")
    chan.send("ssh-server> ")
    
    command_buffer = ""
    while True:
        try:
            data = chan.recv(1024)
            if not data:
                break
            
            char = data.decode('utf-8')

            if char == '
':
                chan.send("
")
                
                full_command = command_buffer.strip()
                
                if full_command.lower() in ['exit', 'quit']:
                    chan.send("Disconnecting...
")
                    break
                
                if full_command:
                    result = execute_system_command(full_command, user_home)
                    if result:
                        chan.send(result)
                    else:
                        chan.send("
")
                
                command_buffer = ""
                chan.send("ssh-server> ")

            elif char == '
':
                continue

            elif char in ['\x7f', '\x08']:  # Handle backspace
                if len(command_buffer) > 0:
                    command_buffer = command_buffer[:-1]
                    chan.send("\b \b")

            elif char.isprintable() or char == ' ':
                command_buffer += char
                chan.send(char)

        except (socket.error, EOFError):
            break
