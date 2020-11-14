import glob
from dominate import document
from dominate.tags import *

photos = glob.glob('uploads/images.jpg')
text = "tooi la huy"
with document(title='Photos') as doc:
    h1('Photos')
    for path in photos:
        div(img(src=path), _class='photo')
        div(b(text))


with open('gallery.html', 'w') as f:
    f.write(doc.render())