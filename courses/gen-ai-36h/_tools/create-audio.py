from pathlib import Path
import json,subprocess
p=Path(__file__).resolve().parents[1]/'assets';tmp=Path('/tmp/gen36-audio');tmp.mkdir(exist_ok=True)
segments=json.loads((p/'audio-segments.json').read_text());lines=[]
for i,(voice,text) in enumerate(segments):
 f=tmp/f'{i}.txt';f.write_text(text);a=tmp/f'{i}.aiff'
 subprocess.run(['say','-v',voice,'-r','140','-f',str(f),'-o',str(a)],check=True)
 w=tmp/f'{i}.wav';subprocess.run(['ffmpeg','-v','error','-y','-i',str(a),'-ar','44100','-ac','1',str(w)],check=True);lines.append(f"file '{w}'")
(tmp/'concat.txt').write_text('\n'.join(lines));subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(tmp/'concat.txt'),'-codec:a','libmp3lame','-b:a','128k',str(p/'mock-meeting.mp3')],check=True)
subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1',str(p/'mock-meeting.mp3')],check=True)
