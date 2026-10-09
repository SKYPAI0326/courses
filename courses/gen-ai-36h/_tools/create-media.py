from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
p=Path(__file__).resolve().parents[1]/'assets'
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf',30)
im=Image.new('RGB',(1500,670),'#f4f5f1');d=ImageDraw.Draw(im);d.text((60,35),'虛構活動會議白板｜2026-10-09',font=font,fill='#34555b')
for i,line in enumerate((p/'mock-whiteboard-text.txt').read_text().splitlines()):d.text((60,125+i*80),line,font=font,fill='#26383b')
im.save(p/'mock-whiteboard.png')
pdfmetrics.registerFont(TTFont('CourseCJK','/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
for name,pages in json.loads((p/'pdf-content.json').read_text()).items():
 c=canvas.Canvas(str(p/(name+'.pdf')),pagesize=A4);c.setTitle(name)
 for i,(title,body) in enumerate(pages,1):
  c.setFont('CourseCJK',21);c.drawString(50,770,title);c.setFont('CourseCJK',14)
  for j,line in enumerate(body.splitlines()):c.drawString(50,700-j*40,line)
  c.setFont('CourseCJK',10);c.drawString(50,45,f'虛構教學資料｜第 {i} 頁，共 3 頁');c.showPage()
 c.save()
print('Created PNG and 3 PDFs')
