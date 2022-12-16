import alsaaudio as aa
import alsaaudio

print(alsaaudio.pcms(pcmtype=aa.PCM_CAPTURE))
print(alsaaudio.pcms(pcmtype=aa.PCM_PLAYBACK))

def test_device(mode, device):
    try:
        streaming = aa.PCM(mode, aa.PCM_NORMAL, device,
                        channels=1)
                        #rate=48000,
                        #format=aa.PCM_FORMAT_S16_LE,
                        #periodsize=2048)
        print(f"{device} WORKED!")

    except Exception as e:
        #print(f"{device} didn't work\n{e}")
        pass

for mode in [aa.PCM_CAPTURE,aa.PCM_PLAYBACK]:
    print(mode)
    for device in ["sysdefault", "MIC", "Mic", "default", "hw", "front", "plughw", 'default:CARD=MIC', "front:CARD=MIC,DEV=0"]:
        test_device(mode,device)

streaming = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, channels=1)
