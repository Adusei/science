import fileinput
import re

with open('ts_questions.txt', 'w') as wr:
  with open('tech_stars_app_raw_html.txt', 'r') as f:
      read_data = f.readlines()
      for line in read_data:
        if "field-block-title " in line:
          strt = line.index('field-block-title ')
          ed = line.index ('/div>')
          #print strt
          strt = strt + 25
          ed = ed - 15
          #print ed 
          #print line
          parsed = line[strt:ed]
          parsed = parsed.replace('<span class="field-red-star"></span> ', '')
          parsed = parsed + '\n'
          wr.write(parsed)
          print parsed
          print '\n'
  f.closed
wr.closed