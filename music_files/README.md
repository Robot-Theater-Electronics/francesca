# You can put your .wav music files inside this directory.
## But to be able to have the alarm clocks play them it is important to upload them to the alarm clocks. You can do that as follows:

### In the terminal, naviagte to this directory (make sure you write your correct path to the folder):

`cd /your/path/francesca/music_files`

then:

`scp noise1.wav ubunut@radio3:/media/mnt/`

and press enter. You should see the progress of the upload.

In the example above we copied the file noise1.wav to radio3. You can repeat the command with different .wav files to
different radios by replacing the title of the file and the radio number. For example, to copy to radio2:

`scp noise1.wav ubunut@radio2:/media/mnt/`

# How to make the alarm clocks play new files #
[Qlan readme](qlab/README.md)
