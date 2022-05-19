from mutagen.mp3 import MP3

# function to convert the seconds into readable format
def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600

    mins = seconds // 60
    seconds %= 60

    return seconds

# Create an MP3 object
# Specify the directory address to the mp3 file as a parameter
audio = MP3("temp.mp3")

# Contains all the metadata about the mp3 file
audio_info = audio.info    

length_in_secs = int(audio_info.length)

hours, mins, seconds = convert(length_in_secs)

print("Hours:", hours)
print("Minutes:", mins)
print("Seconds:", seconds)