# MusicEmotionsClassifier

A simple web app to organize your song library by emotion, and quickly listen to any song depending on your mood!

Uses Javascript & HTML/CSS for the front end and Flask for the backend.

To classify the song emotion, I retrained the inceptionV3 model with spectrogram images of each song (data was hand picked and then preprocessed to reduce overfitting and accuracy). 

The server uses multiprocessing when classifying the spectrograms of a song, to significantly improve performance.
