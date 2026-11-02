# Recria as sequências de frames JPG que o index.html usa (a partir dos MP4 em _frames_src).
# Rode uma vez dentro desta pasta:  python preparar_frames.py   (precisa de ffmpeg no PATH)
import subprocess,os
FR=[('cereja/f_coffee', 30, 75), ('cereja/f_lounge', 30, 66), ('cereja/f_mani', 30, 64), ('cereja/f_wide', 30, 96)]
for fd,fps,n in FR:
    os.makedirs(fd,exist_ok=True)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','_frames_src/'+fd.replace('/','__')+'.mp4','-vsync','0','-q:v','2',fd+'/%03d.jpg'],check=True)
    print(fd,len(os.listdir(fd)),'frames (esperado',n,')')
