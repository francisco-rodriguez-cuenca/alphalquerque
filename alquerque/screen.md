f you won't be logging out of the terminal, you can run it this way:

./script.fcgi --socket /tmp/fcgi-socket && chmod a+w /tmp/fcgi-socket &

If you are going to log off, then its better to start the script under a terminal multiplexer like screen or tmux.

I am not very familiar with tmux, but this is how you can do it with screen:

Start a screen, using the screen command. In the new 'screen' shell, start:

./script.fcgi --socket /tmp/fcgi-socket && chmod a+w /tmp/fcgi-socket

Hit enter

Detach from the screen by pressing ctrl + a followed by ctrl + d

You can connect back to the screen after you come back using:

screen -r

Running this script under screen, will run the script in the background. You will be able to connect back to that shell when you re-attach to the screen.